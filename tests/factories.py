import factory
from django.contrib.auth.models import User
from django.utils import timezone

from tests.test_app.test_app.app.models import Book


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.sequence(lambda n: f"user{n}")


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = "book title"
    publication_date = factory.lazy_attribute(lambda o: timezone.now())
