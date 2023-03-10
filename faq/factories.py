import factory
from .models import FAQ


class FAQFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FAQ

    question = factory.Faker("sentence")
    answer = factory.Faker("sentence")
