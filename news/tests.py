import datetime
from django.test import TestCase
from django.urls import reverse
from administrator.factories import AdministratorFactory
from .models import Category


class TestNews(TestCase):
        
    def test_create_category_by_admin_user(self):
        administator = AdministratorFactory()
        self.client.force_login(administator.user)
        url = reverse("category:create")
        data = {
            "name": "Covid",
        }
        response = self.client.post(url, data=data)
        response_data = response.json()
        categories = Category.objects.filter()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(categories.count(), 1)
