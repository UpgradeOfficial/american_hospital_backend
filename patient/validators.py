from .disposable_mails import disposable_mails
from rest_framework.exceptions import ValidationError


def verify_valid_mail(email):
    server = email.split("@")[-1]
    if server in disposable_mails:
        raise ValidationError("Invalid mail.")
    return email
