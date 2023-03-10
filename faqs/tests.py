from django.test import TestCase
from django.urls import reverse
from .models import FAQ
import json
import datetime
from administrator.factories import AdministratorFactory

# Create your tests here.

class TestFAQCreate(TestCase):

    def test_create_faq(self):
        administator = AdministratorFactory()
        self.client.force_login(administator.user)
        data = {
             "name":"Daniel Obaoluwa", "question":"Does Pharmacy accept insurance?", "answer":"Yes we do",
        }
        url = reverse("faqs:create")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(FAQ.objects.all().count(), 1)

class TestFAQList(TestCase):
    def test_list_faq(self):
        FAQ.objects.create(name="Test1", question = "Question1", answer="yes")
        FAQ.objects.create(name="Test2", question= "Question2", answer="no")
        url = reverse("faqs:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 2)

class TestFAQUpdateRetrieveDelete(TestCase):
    def test_update_faq(self):
        administator = AdministratorFactory()
        self.client.force_login(administator.user)
        faq1 = FAQ.objects.create(name="Test4", question = "Question4", answer="yes")
        faq2 = FAQ.objects.create(name="Test5", question= "Question5", answer="no")
        url = reverse("faqs:retrieve-update-delete", kwargs={'pk': str(faq1.id)})
        data = {"answer":"no"}
        response = self.client.patch(url, data=data, content_type="application/json")
        faq1_after_update = FAQ.objects.get(id=faq1.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(faq1_after_update.answer, data["answer"])

    def test_retrieve_faq(self):
        administator = AdministratorFactory()
        self.client.force_login(administator.user)
        faq1 = FAQ.objects.create(name="Retrieve1", question = "RetieveQA1", answer="This is retrieve")
        faq2 = FAQ.objects.create(name="Retrieve2", question="RetreiveQA2", answer="This is retrieve qa2")
        url = reverse("faqs:retrieve-update-delete", kwargs={'pk': str(faq2.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], faq2.name)
    
    def test_delete_faq(self):
        administator = AdministratorFactory()
        self.client.force_login(administator.user)
        faq1 = FAQ.objects.create(name="Retrieve1", question = "RetieveQA1", answer="This is retrieve")
        faq2 = FAQ.objects.create(name="Retrieve2", question="RetreiveQA2", answer="This is retrieve qa2")
        self.assertEqual(FAQ.objects.all().count(), 2)
        url = reverse("faqs:retrieve-update-delete", kwargs={'pk': str(faq2.id)})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        faq2_after_delete = FAQ.objects.all().filter(id =faq2.id).count()
        self.assertEqual(faq2_after_delete, 0)
        self.assertEqual(FAQ.objects.all().count(), 1)

    
        