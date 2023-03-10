from django.test import TestCase
from django.urls import reverse
from .models import FAQ
from .factories import FAQFactory
from administrator.factories import AdministratorFactory
from patient.factories import PatientFactory

# Create your tests here.


class TestFAQCreate(TestCase):
    def test_create_faq_as_admin_user(self):
        administator = AdministratorFactory()
        self.client.force_login(administator.user)
        data = {
            "question": "Does Pharmacy accept insurance?",
            "answer": "Yes we do",
        }
        url = reverse("faq:create")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(FAQ.objects.count(), 1)

    def test_create_faq_without_question(self):
        administator = AdministratorFactory()
        self.client.force_login(administator.user)
        data = {
            "answer": "Yes we do",
        }
        url = reverse("faq:create")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(FAQ.objects.count(), 0)

    def test_create_faq_without_answer(self):
        administator = AdministratorFactory()
        self.client.force_login(administator.user)
        data = {
            "question": "Yes we do",
        }
        url = reverse("faq:create")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(FAQ.objects.count(), 0)

    def test_create_faq_as_patient_user(self):
        patient = PatientFactory()
        self.client.force_login(patient.user)
        data = {
            "question": "Does Pharmacy accept insurance?",
            "answer": "Yes we do",
        }
        url = reverse("faq:create")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 403)


class TestFAQList(TestCase):
    def test_list_faq(self):
        faqs = FAQFactory.create_batch(2)
        url = reverse("faq:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), len(faqs))


class TestFAQUpdateRetrieveDelete(TestCase):
    def test_update_faq_as_patient(self):
        patient = PatientFactory()
        self.client.force_login(patient.user)
        faq1 = FAQFactory()
        url = reverse("faq:retrieve-update-delete", kwargs={"pk": str(faq1.id)})
        data = {"answer": "no"}
        response = self.client.patch(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_retrieve_faq_as_patient(self):
        patient = PatientFactory()
        self.client.force_login(patient.user)
        faqs = FAQFactory.create_batch(2)
        faq2 = faqs[1]
        url = reverse("faq:retrieve-update-delete", kwargs={"pk": str(faq2.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_delete_faq_as_patient(self):
        patient = PatientFactory()
        self.client.force_login(patient.user)
        faqs = FAQFactory.create_batch(2)
        faq2 = faqs[1]
        self.assertEqual(FAQ.objects.all().count(), 2)
        url = reverse("faq:retrieve-update-delete", kwargs={"pk": str(faq2.id)})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_update_faq_as_admin(self):
        administator = AdministratorFactory()
        self.client.force_login(administator.user)
        faq1 = FAQFactory()
        url = reverse("faq:retrieve-update-delete", kwargs={"pk": str(faq1.id)})
        data = {"answer": "no"}
        response = self.client.patch(url, data=data, content_type="application/json")
        faq1_after_update = FAQ.objects.get(id=faq1.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(faq1_after_update.answer, data["answer"])

    def test_retrieve_faqas_admin(self):
        administator = AdministratorFactory()
        self.client.force_login(administator.user)
        faqs = FAQFactory.create_batch(2)
        faq2 = faqs[1]
        url = reverse("faq:retrieve-update-delete", kwargs={"pk": str(faq2.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["question"], faq2.question)

    def test_delete_faqas_admin(self):
        administator = AdministratorFactory()
        self.client.force_login(administator.user)
        faqs = FAQFactory.create_batch(2)
        faq2 = faqs[1]
        self.assertEqual(FAQ.objects.all().count(), 2)
        url = reverse("faq:retrieve-update-delete", kwargs={"pk": str(faq2.id)})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        faq2_after_delete = FAQ.objects.all().filter(id=faq2.id).count()
        self.assertEqual(faq2_after_delete, 0)
        self.assertEqual(FAQ.objects.all().count(), 1)
