from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.db import transaction

from user.models import User
from user.tasks import (
    send_password_reset_mail_async,
    send_email_verification_mail_async,
)
from user.factories import UserFactory


@transaction.atomic
class Command(BaseCommand):
    help = "Send Test Emails To See The Templates Meet The Expected Standards"

    def add_arguments(self, parser):
        parser.add_argument(
            "-t",
            "--to",
            type=str,
            help="Indicates the email address the emails are to be sent to ",
        )

    def handle(self, *args, **kwargs):
        to = kwargs.get("to")
        if to is None:
            to = "thinkalpha21@gmail.com"
        user, created = User.objects.get_or_create(
            email=to,
            defaults={
                "password": make_password("aaaaaaaaaa"),
                "user_type": User.UserType.PATIENT,
                "country": "Nigeria",
                "first_name": "test user",
            },
        )
        send_email_verification_mail_async(user_id=user.id)
        # send_password_reset_mail_async(user_id=user.id)
        self.stdout.write(self.style.SUCCESS(f"All emails send successfully to {to}"))
