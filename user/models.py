from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.sites.models import Site
from django.db import IntegrityError, models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
import logging
from core.models import CoreModel
from core.utils import ExpiringActivationTokenGenerator, send_mail

from .literals import PROFILE_PHOTO_DIRECTORY, SIGNATURE_PHOTO_DIRECTORY
from .managers import UserCustomManager


# Create your models here.
class PasswordResetWhitelist(CoreModel):
    email = models.EmailField()
    token = models.CharField(max_length=255)

    class Meta:
        unique_together = ("email", "token")


class User(AbstractUser, CoreModel):
    class UserType(models.TextChoices):
        PATIENT = "PATIENT", _("patient")
        ADMIN = "ADMIN", _("admin")

    class UserRegion(models.TextChoices):
        AFRICA = "AF", _("Africa")
        ASIA = "AS", _("Asia")
        EUROPE = "EU", _("Europe")
        MIDDLE_EAST = "ME", _("Middle East")
        NORTH_AMERICA = (
            "NA",
            _("North America"),
        )
        SOUTH_AMERICA = "SA", _("South America")

    class Gender(models.TextChoices):
        MALE = "MALE", _("male")
        FEMALE = "FEMALE", _("female")
        OTHER = "OTHER", _("other")
        PREFER_NOT_TO_SAY = "PREFER NOT TO SAY", _("preder not to say")

    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_("email"), unique=True)
    user_type = models.CharField(
        _("user type"),
        max_length=20,
        choices=UserType.choices,
        default=UserType.PATIENT,
    )
    is_verified = models.BooleanField(_("is verified"), default=False)
    user_login_token = models.CharField(max_length=200, blank=True, null=True)
    street = models.CharField(_("street"), max_length=100, blank=True, null=True)
    state = models.CharField(_("state"), max_length=50, blank=True, null=True)
    city = models.CharField(_("city"), max_length=100, blank=True, null=True)
    country = models.CharField(_("country"), max_length=50, default="NG")
    region = models.CharField(
        _("region"),
        max_length=50,
        choices=UserRegion.choices,
        default=UserRegion.AFRICA,
    )
    contact_no = models.CharField(_("contact no"), max_length=20)
    date_of_birth = models.DateField(_("date of birth"), blank=True, null=True)
    gender = models.CharField(
        _("gender"),
        max_length=30,
        choices=Gender.choices,
        default=Gender.PREFER_NOT_TO_SAY,
    )
    image = models.ImageField(
        upload_to=PROFILE_PHOTO_DIRECTORY,
        blank=True,
        null=True,
    )
    username = None
    objects = UserCustomManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return f"{self.email} ({self.user_type}) {self.full_name}"

    def __repr__(self) -> str:
        return self.email

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    @classmethod
    def get_hidden_fields(cls):
        return super().get_hidden_fields() + [
            "date_joined",
            "last_login",
            "is_superuser",
        ]

    def send_password_reset_mail(self) -> None:
        template = "emails/password_reset.html"
        reset_token = ExpiringActivationTokenGenerator().generate_token(text=self.email)
        try:
            _ = PasswordResetWhitelist.objects.create(
                email=self.email, token=reset_token.decode("utf-8")
            )
        except IntegrityError:
            raise ValidationError("Password reset mail is already sent.")

        # account/recovery/reset/:id/
        link = "/".join(
            [
                settings.FRONTEND_URL,
                "account",
                "recovery",
                "reset",
                reset_token.decode("utf-8"),
            ]
        )
        send_mail(
            to_email=self.email,
            subject="Password Reset",
            template_name=template,
            input_context={
                "name": self.full_name,
                "link": link,
                "host_url": Site.objects.get_current().domain,
            },
        )

    @classmethod
    def verify_password_reset(cls, token: str, password: str) -> None:
        user = None
        whitelist_token = None
        try:
            whitelist_token = PasswordResetWhitelist.objects.get(token=token)
        except PasswordResetWhitelist.DoesNotExist as e:
            logging.error(f"Password reset token does not exist. {str(e)}")
            raise ValidationError("Invalid Token. Password Rest Record Doesn't Exists")
        email = ExpiringActivationTokenGenerator().get_token_value(token)
        try:
            user = cls.objects.get(email=email)
        except cls.DoesNotExist as e:
            raise ValidationError(f"Invalid token. {user.email} not found {e}")

        user.set_password(password)
        user.save()
        whitelist_token.delete()

    def send_email_verification_mail(self):
        template = "emails/registration.html"

        confirmation_token = ExpiringActivationTokenGenerator().generate_token(
            text=self.email
        )

        link = (
            "/".join(
                [
                    settings.FRONTEND_URL,
                    "email-verification",
                    confirmation_token.decode("utf-8"),
                ]
            )
            + "?token=this-dont-care"
        )
        send_mail(
            to_email=self.email,
            subject=f"Verify User Account {self.email}",
            template_name=template,
            input_context={
                "name": self.full_name,
                "link": link,
                "host_url": Site.objects.get_current().domain,
            },
        )
