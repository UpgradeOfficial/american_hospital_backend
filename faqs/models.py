from django.db import models
from user.models import User

from core.models import CoreModel


class FAQ(CoreModel):
    name = models.CharField(max_length=200, null=False)
    question = models.CharField(max_length=300, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    answer = models.CharField(null=False)