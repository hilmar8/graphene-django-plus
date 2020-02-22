from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from graphene_django_hilmarh.typesets import RelayTypeSet
from tests.test_app.test_app.app.types import BookType
from tests.test_app.test_app.throttles import ThrottleThree


class BookRelayTypeSet(RelayTypeSet):
    object_type = BookType

    operations = {
        "get": "book",
        "list": "books",
    }


class BookRelayAdminTypeSet(RelayTypeSet):
    object_type = BookType

    permission_classes = [IsAdminUser]

    operations = {
        "get": "book_as_admin",
        "list": "books_as_admin",
    }


class BookRelayThrottleTypeSet(RelayTypeSet):
    object_type = BookType

    throttle_classes = [ThrottleThree]

    operations = {
        "get": "book_throttled",
        "list": "books_throttled",
    }
