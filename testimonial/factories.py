import factory
from .models import Testimonial
from user.factories import UserFactory


class TestimonialFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Testimonial

    creator = factory.SubFactory(UserFactory)
    content = factory.Faker("sentence")
    name_of_author = factory.Faker("name")
