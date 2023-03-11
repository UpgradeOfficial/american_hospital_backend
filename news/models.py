from django.db import models

from core.models import CoreModel

from .literals import NEWS_IMAGE_DIRECTORY


# Create your models here.
class Category(CoreModel):
    name = models.TextField(help_text="Category Name")


class News(CoreModel):
    categories = models.ManyToManyField(Category, related_name="news")
    title = models.TextField(help_text="News Title")
    image = models.ImageField(
        upload_to=NEWS_IMAGE_DIRECTORY,
        blank=True,
        null=True,
    )
    content = models.TextField()
