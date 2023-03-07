from rest_framework.exceptions import ValidationError

from .constants import ALLOWED_MAIL_PROVIDER


def verify_valid_mail(email):
    server = email.split("@")[-1]
    if server not in ALLOWED_MAIL_PROVIDER:
        raise ValidationError(
            f"Invalid mail {email}, It must be any of this providers {ALLOWED_MAIL_PROVIDER}"
        )
    return email
