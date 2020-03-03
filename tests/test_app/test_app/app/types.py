import graphene
from graphene_django.fields import DjangoListField

from graphene_django_plus.fields import SpriklListField
from graphene_django_plus.relay.node import SpriklNode
from graphene_django_plus.types import DjangoObjectType
from tests.test_app.test_app.app.models import Book, Publisher, Author


class PublisherType(DjangoObjectType):
    all_books = SpriklListField("tests.test_app.test_app.app.types.BookType")

    class Meta:
        model = Publisher
        interfaces = (SpriklNode,)
        fields = (
            "name",
            "address",
        )


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        interfaces = (SpriklNode,)
        fields = (
            "first_name",
            "last_name",
            "email",
        )


class BookType(DjangoObjectType):
    publisher = graphene.Field(PublisherType)
    all_authors = SpriklListField(AuthorType)

    class Meta:
        model = Book
        interfaces = (SpriklNode,)
        fields = ("title",)
