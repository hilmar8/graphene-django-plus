from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from graphene_django_hilmarh.typesets import RelayTypeSet
from tests.test_app.test_app.app.filters import BookFilter
from tests.test_app.test_app.app.types import BookType
from tests.test_app.test_app.throttles import ThrottleThree, ThrottleFour, ThrottleSix


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

    operations = {
        "get": "book_throttled",
        "list": "books_throttled",
    }

    @classmethod
    def get_throttles(cls, operation):
        if operation == "get":
            return [ThrottleThree]
        if operation == "list":
            return [ThrottleFour]


class BookRelayFilteredTypeSet(RelayTypeSet):
    object_type = BookType
    filterset_class = BookFilter

    operations = {
        "list": "books_filtered",
    }


class BookRelayFilteredAdminTypeSet(RelayTypeSet):
    object_type = BookType
    filterset_class = BookFilter
    permission_classes = [IsAdminUser]

    operations = {
        "list": "books_filtered_as_admin",
    }


class BookRelayFilteredThrottleTypeSet(RelayTypeSet):
    object_type = BookType
    filterset_class = BookFilter
    throttle_classes = [ThrottleSix]

    operations = {
        "list": "books_filtered_throttled",
    }
