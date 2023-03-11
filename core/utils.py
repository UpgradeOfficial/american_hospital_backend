import logging
from datetime import datetime, timedelta

from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError


class ExpiringActivationTokenGenerator:
    FERNET_KEY = settings.FERNET_KEY
    fernet = Fernet(FERNET_KEY)

    DATE_FORMAT = "%Y-%m-%d %H-%M-%S"
    EXPIRATION_DAYS = 3

    def _get_time(self):
        """Returns a string with the current UTC time"""
        return datetime.utcnow().strftime(self.DATE_FORMAT)

    def _parse_time(self, d):
        """Parses a string produced by _get_time and returns a datetime object"""
        return datetime.strptime(d, self.DATE_FORMAT)

    def generate_token(self, text):
        """Generates an encrypted token"""
        full_text = text + "|" + self._get_time()
        token = self.fernet.encrypt(bytes(full_text, encoding="utf-8"))
        return token

    def get_token_value(self, token):
        """Gets a value from an encrypted token.
        Returns None if the token is invalid or has expired.
        """
        try:
            value = self.fernet.decrypt(bytes(token, encoding="utf-8")).decode("utf-8")
            separator_pos = value.rfind("|")

            text = value[:separator_pos]
            token_time = self._parse_time(value[separator_pos + 1 :])

            if token_time + timedelta(self.EXPIRATION_DAYS) < datetime.utcnow():
                raise InvalidToken("Token expired.")
        except InvalidToken as e:
            logging.error(f"Invalid Token{e}")
            raise ValidationError("Invalid token.")
        return text


def send_mail(
    subject,
    to_email,
    input_context,
    template_name,
    file=None,
    cc_list=[],
    bcc_list=[],
    is_info_mail=True,
):
    """
    Send Activation Email To User
    """
    # base_url = input_context.get("host_url", Site.objects.get_current().domain)
    try:
        context = {
            "site": "dokto",
            "MEDIA_URL": settings.STATIC_URL[:-1],
            **input_context,
        }

        # render email text
        email_html_message = render_to_string(template_name, context)

        msg = EmailMultiAlternatives(
            subject=subject,
            body=email_html_message,
            from_email=settings.INFO_EMAIL if is_info_mail else settings.SUPPORT_EMAIL,
            to=[to_email],
        )
        msg.attach_alternative(email_html_message, "text/html")
        if file is not None:
            msg.attach("attached_file.png", file, "image/png")
        msg.send()
    except Exception as e:
        logging.error(f"{str(e)} ==> Failed to send email to {to_email}")
