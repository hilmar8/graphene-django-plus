from rest_framework import serializers

from graphene_django_plus.serializers import SerializerDjangoObjectTypeField
from tests.test_app.test_app.app.models import Book
from tests.test_app.test_app.app.types import BookType


class CreateRelayBookSerializer(serializers.ModelSerializer):
    book = SerializerDjangoObjectTypeField(BookType)

    class Meta:
        model = Book
        fields = ["book", "title"]
        extra_kwargs = {"title": {"write_only": True}}


class UpdateRelayBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title"]

