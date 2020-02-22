from graphene_django_hilmarh.relay.node import SpriklNode
from tests.test_app.test_app.app.types import BookType


class Query:
    book = SpriklNode.Field(BookType)
