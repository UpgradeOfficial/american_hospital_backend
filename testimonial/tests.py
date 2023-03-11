from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from administrator.factories import AdministratorFactory
from patient.factories import PatientFactory

from .factories import TestimonialFactory
from .models import Testimonial


class TestTestimonial(TestCase):
    def test_delete_testimonial_by_patient_user(self):
        patient = PatientFactory()
        testimonial = TestimonialFactory()
        self.client.force_login(patient.user)
        url = reverse("testimonial:detail", kwargs={"pk": str(testimonial.id)})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_retrieve_testimonial_by_patient_user(self):
        patient = PatientFactory()
        testimonial = TestimonialFactory()
        self.client.force_login(patient.user)
        url = reverse("testimonial:detail", kwargs={"pk": str(testimonial.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_updated_testimonial_by_patient_user(self):
        patient = PatientFactory()
        testimonial = TestimonialFactory()
        self.client.force_login(patient.user)
        url = reverse("testimonial:detail", kwargs={"pk": str(testimonial.id)})
        data = {
            "name_of_author": "Mr Daniel dede",
            "content": "I love the american hospital and it services",
            "date_created": datetime.now(),
        }
        response = self.client.patch(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_delete_testimonial_by_admin_user(self):
        administator = AdministratorFactory()
        testimonial = TestimonialFactory()
        self.client.force_login(administator.user)
        url = reverse("testimonial:detail", kwargs={"pk": str(testimonial.id)})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        testimonials = Testimonial.objects.filter()
        all_testimonials = Testimonial.all_objects.filter()
        self.assertEqual(testimonials.count(), 0)
        self.assertEqual(all_testimonials.count(), 1)
        self.assertTrue(all_testimonials.first().is_deleted)

    def test_retrieve_testimonial_by_admin_user(self):
        administator = AdministratorFactory()
        testimonial = TestimonialFactory()
        self.client.force_login(administator.user)
        url = reverse("testimonial:detail", kwargs={"pk": str(testimonial.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data["content"], testimonial.content)
        self.assertTrue(response_data["name_of_author"], testimonial.name_of_author)
        self.assertTrue(response_data["creator"], testimonial.creator)

    def test_updated_testimonial_by_admin_user(self):
        administator = AdministratorFactory()
        testimonial = TestimonialFactory()
        self.client.force_login(administator.user)
        url = reverse("testimonial:detail", kwargs={"pk": str(testimonial.id)})
        data = {
            "name_of_author": "Mr Daniel dede",
            "content": "I love the american hospital and it services",
            "date_created": datetime.now(),
        }
        response = self.client.patch(url, data=data, content_type="application/json")
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        new_testimonial = Testimonial.objects.get(id=testimonial.id)
        self.assertEqual(new_testimonial.id, testimonial.id)
        self.assertNotEqual(new_testimonial.name_of_author, testimonial.name_of_author)
        self.assertNotEqual(new_testimonial.content, testimonial.content)
        self.assertEqual(response_data["content"], new_testimonial.content)

    def test_create_testimonial_by_admin_user(self):
        administator = AdministratorFactory()
        self.client.force_login(administator.user)
        url = reverse("testimonial:create")
        data = {
            "name_of_author": "Mr Daniel dede",
            "content": "I love the american hospital and it services",
            "date_created": datetime.now(),
        }
        response = self.client.post(url, data=data)
        response_data = response.json()
        testimonials = Testimonial.objects.filter()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data["name_of_author"], data.get("name_of_author"))
        self.assertEqual(response_data["content"], data.get("content"))
        self.assertEqual(response_data["creator"], str(administator.user_id))
        self.assertEqual(testimonials.count(), 1)

    def test_create_testimonial_by_patient_user(self):
        patient = PatientFactory()
        self.client.force_login(patient.user)
        url = reverse("testimonial:create")
        data = {
            "name_of_author": "Mr Daniel dede",
            "content": "I love the american hospital and it services",
            "date_created": datetime.now(),
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 403)

    def test_list_testimonial(self):
        testimonials = TestimonialFactory.create_batch(3)
        url = reverse("testimonial:list")
        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data["results"]), len(testimonials))
