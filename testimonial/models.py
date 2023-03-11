from django.db import models

from core.models import CoreModel
from user.models import User

# Create your models here.


class Testimonial(CoreModel):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name_of_author = models.CharField(max_length=100)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
