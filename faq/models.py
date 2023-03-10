from django.db import models
from user.models import User

from core.models import CoreModel


class FAQ(CoreModel):
    question = models.CharField(max_length=300)
    answer = models.CharField(max_length=500)
