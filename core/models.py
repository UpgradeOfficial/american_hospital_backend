import uuid

from django.db import models
from django.utils import timezone

from core.managers import CustomManager


# Create your models here.
class CoreModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    all_objects = models.Manager()
    objects = CustomManager()

    def __str__(self) -> str:
        return str(self.id)

    def __repr__(self) -> str:
        return self.__str__()

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.is_deleted = True
        self.save()

    @classmethod
    def get_hidden_fields(cls):
        return ["created_at", "updated_at", "is_deleted", "deleted_at"]

    class Meta:
        abstract = True
