from core.tasks import my_shared_task
from user.models import User


@my_shared_task
def send_email_verification_mail_async(user_id):
    user = User.objects.get(id=user_id)
    user.send_email_verification_mail()


@my_shared_task
def send_password_reset_mail_async(user_id):
    user = User.objects.get(id=user_id)
    user.send_password_reset_mail()
