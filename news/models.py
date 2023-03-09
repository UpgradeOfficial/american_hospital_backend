from django.db import models

from core.models import CoreModel
from user.literals import PROFILE_PHOTO_DIRECTORY

# Create your models here.
class Category(CoreModel):
    name  = models.TextField(help_text='Category Name')

class News(CoreModel):
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news')
    title = models.TextField(help_text='News Title')
    image = models.ImageField(
        upload_to=PROFILE_PHOTO_DIRECTORY,
        blank=True,
        null=True,
    )
    content = models.TextField()
    total_likes = models.IntegerField()
    total_shares = models.IntegerField()
    