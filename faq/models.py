from django.db import models

from core.models import CoreModel
from user.models import User


class FAQ(CoreModel):
    question = models.CharField(max_length=300)
    answer = models.CharField(max_length=500)
