from django.db import models
from core.models import CoreModel
from user.models import User

# Create your models here.


class Administrator(CoreModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
