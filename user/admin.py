from django.contrib import admin

from .models import User

models = [User]
# Register your models here.
for model in models:
    admin.site.register(model)
