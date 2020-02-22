from rest_framework import serializers

from tests.test_app.test_app.app.models import Book


class CreateRelayBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title"]
