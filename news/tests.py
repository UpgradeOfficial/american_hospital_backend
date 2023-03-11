from django.test import TestCase
from django.urls import reverse

from administrator.factories import AdministratorFactory
from news.models import Category, News
from patient.factories import PatientFactory

from .factories import CategoryFactory, NewsFactory


class TestCategory(TestCase):
    def test_list_news(self):
        news = NewsFactory.create_batch(4)
        url = reverse("news:news_list")
        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data["results"]), len(news))

    def test_create_news_by_admin_user(self):
        administator = AdministratorFactory()
        categories = CategoryFactory.create_batch(4)
        self.client.force_login(administator.user)
        url = reverse("news:news_create")
        data = {
            "categories": categories,
            "title": "Effect of Covid19",
            "content": "This is a test content for the covid 19 article",
        }
        response = self.client.post(url, data=data)
        response_data = response.json()
        news = News.objects.filter()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data["id"], str(news.first().id))
        self.assertEqual(response_data["content"], news.first().content)
        self.assertEqual(news.count(), 1)

    def test_create_news_by_patient_user(self):
        patient = PatientFactory()
        self.client.force_login(patient.user)
        url = reverse("news:news_create")
        data = {
            "title": "Effect of Covid19",
            "content": "This is a test content for the covid 19 article",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 403)

    def test_update_news_as_patient(self):
        patient = PatientFactory()
        self.client.force_login(patient.user)
        news1 = NewsFactory()
        url = reverse("news:news_detail", kwargs={"pk": str(news1.id)})
        data = {"title": "new name"}
        response = self.client.patch(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_retrieve_news_as_patient(self):
        patient = PatientFactory()
        self.client.force_login(patient.user)
        newss = NewsFactory.create_batch(2)
        news2 = newss[1]
        url = reverse("news:news_detail", kwargs={"pk": str(news2.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_delete_news_as_patient(self):
        patient = PatientFactory()
        self.client.force_login(patient.user)
        news = NewsFactory.create_batch(2)
        news2 = news[1]
        self.assertEqual(News.objects.all().count(), 2)
        url = reverse("news:news_detail", kwargs={"pk": str(news2.id)})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_update_news_as_admin(self):
        administator = AdministratorFactory()
        self.client.force_login(administator.user)
        news1 = NewsFactory()
        url = reverse("news:news_detail", kwargs={"pk": str(news1.id)})
        data = {"title": "new name"}
        response = self.client.patch(url, data=data, content_type="application/json")
        news1_after_update = News.objects.get(id=news1.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(news1_after_update.title, data["title"])

    def test_retrieve_news_as_admin(self):
        administator = AdministratorFactory()
        self.client.force_login(administator.user)
        newss = NewsFactory.create_batch(2)
        news2 = newss[1]
        url = reverse("news:news_detail", kwargs={"pk": str(news2.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], news2.title)

    def test_delete_news_as_admin(self):
        administator = AdministratorFactory()
        self.client.force_login(administator.user)
        newss = NewsFactory.create_batch(2)
        news2 = newss[1]
        self.assertEqual(News.objects.all().count(), 2)
        url = reverse("news:news_detail", kwargs={"pk": str(news2.id)})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        news2_after_delete = News.objects.all().filter(id=news2.id).count()
        self.assertEqual(news2_after_delete, 0)
        self.assertEqual(News.objects.all().count(), 1)


class TestCatory(TestCase):
    def test_list_category(self):
        categories = CategoryFactory.create_batch(4)
        url = reverse("news:category-list")
        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data["results"]), len(categories))

    def test_create_category_by_admin_user(self):
        administator = AdministratorFactory()
        self.client.force_login(administator.user)
        url = reverse("news:create_category")
        data = {
            "name": "Covid",
        }
        response = self.client.post(url, data=data)
        response_data = response.json()
        categories = Category.objects.filter()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data["id"], str(categories.first().id))
        self.assertEqual(response_data["name"], categories.first().name)
        self.assertEqual(categories.count(), 1)

    def test_create_category_by_patient_user(self):
        patient = PatientFactory()
        self.client.force_login(patient.user)
        url = reverse("news:create_category")
        data = {
            "name": "Covid",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 403)

    def test_update_category_as_patient(self):
        patient = PatientFactory()
        self.client.force_login(patient.user)
        category1 = CategoryFactory()
        url = reverse("news:category-detail", kwargs={"pk": str(category1.id)})
        data = {"name": "new name"}
        response = self.client.patch(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_retrieve_category_as_patient(self):
        patient = PatientFactory()
        self.client.force_login(patient.user)
        categorys = CategoryFactory.create_batch(2)
        category2 = categorys[1]
        url = reverse("news:category-detail", kwargs={"pk": str(category2.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_delete_category_as_patient(self):
        patient = PatientFactory()
        self.client.force_login(patient.user)
        categorys = CategoryFactory.create_batch(2)
        category2 = categorys[1]
        self.assertEqual(Category.objects.all().count(), 2)
        url = reverse("news:category-detail", kwargs={"pk": str(category2.id)})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_update_category_as_admin(self):
        administator = AdministratorFactory()
        self.client.force_login(administator.user)
        category1 = CategoryFactory()
        url = reverse("news:category-detail", kwargs={"pk": str(category1.id)})
        data = {"name": "new name"}
        response = self.client.patch(url, data=data, content_type="application/json")
        category1_after_update = Category.objects.get(id=category1.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(category1_after_update.name, data["name"])

    def test_retrieve_category_as_admin(self):
        administator = AdministratorFactory()
        self.client.force_login(administator.user)
        categorys = CategoryFactory.create_batch(2)
        category2 = categorys[1]
        url = reverse("news:category-detail", kwargs={"pk": str(category2.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], category2.name)

    def test_delete_category_as_admin(self):
        administator = AdministratorFactory()
        self.client.force_login(administator.user)
        categorys = CategoryFactory.create_batch(2)
        category2 = categorys[1]
        self.assertEqual(Category.objects.all().count(), 2)
        url = reverse("news:category-detail", kwargs={"pk": str(category2.id)})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        category2_after_delete = Category.objects.all().filter(id=category2.id).count()
        self.assertEqual(category2_after_delete, 0)
        self.assertEqual(Category.objects.all().count(), 1)
