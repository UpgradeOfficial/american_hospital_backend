from django.db import models
from core.models import CoreModel
from user.models import User

# Create your models here.


class Patient(CoreModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
