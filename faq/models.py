from django.db import models
from user.models import User

from core.models import CoreModel


class FAQ(CoreModel):
    name = models.CharField(max_length=200, null=True)
    question = models.CharField(max_length=300, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    answer = models.CharField(max_length = 500, null=True)