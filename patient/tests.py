import datetime

from django.test import TestCase
from django.urls import reverse

from administrator.factories import AdministratorFactory
from user.models import User

from .factories import PatientFactory
from .models import Patient


class TestPatientRegistration(TestCase):
    def test_register_new_patient(self):
        url = reverse("patient:register")
        data = {
            "password": "passworder",
            "email": "user@gmail.com",
            "contact_no": "07068448786",
            "first_name": "first",
            "last_name": "last",
        }
        response = self.client.post(url, data=data)
        patient = Patient.objects.first()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(patient.user.user_type, User.UserType.PATIENT)
        self.assertEqual(patient.user.email, data.get("email"))
        self.assertEqual(patient.user.contact_no, data.get("contact_no"))
        self.assertEqual(patient.user.first_name, data.get("first_name"))
        self.assertEqual(patient.user.last_name, data.get("last_name"))


class PatientProfileTest(TestCase):
    def setUp(self):
        self.patients = PatientFactory.create_batch(3)

    def test_fetch_profile(self):
        patient = self.patients[0]
        self.client.force_login(patient.user)
        url = reverse("patient:profile")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(patient.user.email, data["email"])

    def test_update_profile(self):
        patient = self.patients[0]
        self.client.force_login(patient.user)
        url = reverse("patient:profile")
        data = {
            "email": "i@gmail.com",
            "password": "philip1234@i)",
            "first_name": "increase",
            "last_name": "odeyemi",
            "middle_name": "Ayobami",
            "street": "No 17 Adegbemileke street Afromed",
            "state": "Lagos",
            "city": "Ojo",
            "region": "EU",
            "country": "GH",
            "contact_no": "070780079",
            "date_of_birth": "1999-07-08",
            "gender": "MALE",
        }
        res = self.client.patch(
            url,
            data=data,
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        patient = Patient.objects.get(id=patient.id)
        user = patient.user
        self.assertEqual(user.first_name, data.get("first_name"))
        self.assertEqual(user.last_name, data.get("last_name"))
        self.assertEqual(user.street, data.get("street"))
        self.assertEqual(user.city, data.get("city"))
        self.assertEqual(user.region, data.get("region"))
        self.assertEqual(user.country, data.get("country"))
        self.assertEqual(str(user.date_of_birth), data.get("date_of_birth"))
        self.assertEqual(user.gender, data.get("gender"))

    def test_patient_list(self):
        administator = AdministratorFactory()
        self.client.force_login(administator.user)
        url = reverse("patient:listpatients")  # get url for listpatients
        response = self.client.get(url)  # get reponse
        self.assertEqual(response.status_code, 200)  # success message
        self.assertEqual(len(response.json()["results"]), 3)
