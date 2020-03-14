import graphene
from graphene_django.fields import DjangoListField

from graphene_django_plus.fields import DjangoPlusListField
from graphene_django_plus.relay.node import PlusNode
from graphene_django_plus.types import DjangoObjectType
from tests.test_app.test_app.app.models import Book, Publisher, Author


class PublisherType(DjangoObjectType):
    all_books = DjangoPlusListField("tests.test_app.test_app.app.types.BookType")

    class Meta:
        model = Publisher
        interfaces = (PlusNode,)
        fields = (
            "name",
            "address",
        )


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        interfaces = (PlusNode,)
        fields = (
            "first_name",
            "last_name",
            "email",
        )


class BookType(DjangoObjectType):
    publisher = graphene.Field(PublisherType)
    all_authors = DjangoPlusListField(AuthorType)

    class Meta:
        model = Book
        interfaces = (PlusNode,)
        fields = ("title",)
