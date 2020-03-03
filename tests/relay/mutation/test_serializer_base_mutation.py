import graphene
import pytest
from graphql_relay import to_global_id
from rest_framework import serializers
from rest_framework.utils import json

from graphene_django_plus.relay.mutation import (
    SerializerClientIDCreateMutation,
    SerializerClientIDUpdateMutation,
)
from graphene_django_plus.relay.node import SpriklNode
from graphene_django_plus.serializers import SerializerRelayIDField
from tests.test_app.test_app.app.models import Book
from tests.test_app.test_app.app.types import BookType


def test_serializer_base_client_id_mutation_without_serializer_class():
    with pytest.raises(Exception) as e:

        class SerializerMutation(SerializerClientIDCreateMutation):
            class Meta:
                pass

    assert (
        e.value.args[0] == "serializer_class is required for SerializerClientIDMutation"
    )


def test_serializer_base_client_id_mutation_with_invalid_node_class():
    with pytest.raises(Exception) as e:

        class SerializerMutation(SerializerClientIDCreateMutation):
            class Meta:
                serializer_class = serializers.Serializer
                node_class = Exception

    assert e.value.args[0] == "node_class must be a subclass of relay.Node"


def test_serializer_base_client_id_mutation_update_without_model_class():
    with pytest.raises(Exception) as e:

        class SerializerMutation(SerializerClientIDUpdateMutation):
            class Meta:
                serializer_class = serializers.Serializer
                node_class = SpriklNode

    assert e.value.args[0] == "model_class is required for SerializerClientIDMutation"


def test_serializer_base_client_id_mutation_update_without_id_field():
    class BookSerializer(serializers.ModelSerializer):
        class Meta:
            model = Book
            fields = ["title"]

    class SerializerMutation(SerializerClientIDUpdateMutation):
        class Meta:
            serializer_class = BookSerializer
            node_class = SpriklNode
            model_class = Book
            id_input_field = None

    class Mutation(graphene.ObjectType):
        serializer_mutation = SerializerMutation.Field()

    schema = graphene.Schema(mutation=Mutation)

    with pytest.warns(UserWarning):  # Should not be called without context
        result = schema.execute(
            """
    mutation SerializerMutation($input: SerializerMutationInput!) {
        serializerMutation(input: $input) {
          title
        }
    }
    """,
            variables={"input": {"title": "new title"}},
        )

    assert (
        result.errors[0].args[0]
        == 'Invalid update operation. Input parameter "None" required.'
    )


@pytest.mark.django_db()
def test_serializer_base_client_id_mutation_skip_field():
    class Field(serializers.CharField):
        def get_attribute(self, instance):
            raise serializers.SkipField()

    class BookSerializer(serializers.ModelSerializer):
        title = Field()

        class Meta:
            model = Book
            fields = ["title"]

    class SerializerMutation(SerializerClientIDCreateMutation):
        class Meta:
            serializer_class = BookSerializer

    class Mutation(graphene.ObjectType):
        serializer_mutation = SerializerMutation.Field()

    schema = graphene.Schema(mutation=Mutation)

    with pytest.warns(UserWarning):  # Should not be called without context
        result = schema.execute(
            """
    mutation SerializerMutation($input: SerializerMutationInput!) {
        serializerMutation(input: $input) {
          title
        }
    }
    """,
            variables={"input": {"title": "new book"}},
            context={},
        )

    assert result.data == {"serializerMutation": {"title": None}}

    assert Book.objects.filter(title="new book").delete()[0] == 1


@pytest.mark.django_db()
def test_serializer_base_client_id_mutation_validation_error_from_dict():
    class BookSerializer(serializers.ModelSerializer):
        extra = serializers.ListField(
            child=serializers.IntegerField(min_value=0, max_value=100)
        )

        class Meta:
            model = Book
            fields = ["title", "extra"]

    class SerializerMutation(SerializerClientIDCreateMutation):
        class Meta:
            serializer_class = BookSerializer

    class Mutation(graphene.ObjectType):
        serializer_mutation = SerializerMutation.Field()

    schema = graphene.Schema(mutation=Mutation)

    with pytest.warns(UserWarning):  # Should not be called without context
        result = schema.execute(
            """
    mutation SerializerMutation($input: SerializerMutationInput!) {
        serializerMutation(input: $input) {
          title
          errors {
            field
            messages
            path
          }
        }
    }
    """,
            variables={"input": {"title": "new book", "extra": [0, -1, 2]}},
            context={},
        )

    assert json.loads(json.dumps(result.data)) == {
        "serializerMutation": {
            "errors": [
                {
                    "field": "extra.1",
                    "messages": ["Ensure this value is greater than or equal to 0."],
                    "path": ["extra", "1"],
                }
            ],
            "title": None,
        }
    }


@pytest.mark.django_db()
def test_serializer_base_client_id_mutation_serializer_relay_id_field_invalid_node_class():

    with pytest.raises(Exception) as e:

        class Serializer(serializers.Serializer):
            id = SerializerRelayIDField(
                BookType, node_class=ValueError, method_name="resolve_id", source="book"
            )
            title = serializers.CharField(read_only=True)

    assert e.value.args[0] == "node_class must be a subclass of relay.Node"


@pytest.mark.django_db()
def test_serializer_base_client_id_mutation_serializer_relay_id_field_invalid_method_name():

    with pytest.raises(Exception) as e:

        class Serializer(serializers.Serializer):
            id = SerializerRelayIDField()
            title = serializers.CharField(read_only=True)

    assert e.value.args[0] == "method_name must be passed if object_type is missing"


@pytest.mark.django_db()
def test_serializer_base_client_id_mutation_serializer_relay_id_field_with_method_name():
    class Serializer(serializers.Serializer):
        id = SerializerRelayIDField(BookType, method_name="resolve_id", source="book")
        title = serializers.CharField(read_only=True)

        @classmethod
        def resolve_id(cls, object_id, **kwargs):
            assert object_id == "2"
            return Book(title="resolved title")

        def create(self, validated_data):
            return validated_data.get("book")

    class SerializerMutation(SerializerClientIDCreateMutation):
        class Meta:
            serializer_class = Serializer

    class Mutation(graphene.ObjectType):
        serializer_mutation = SerializerMutation.Field()

    schema = graphene.Schema(mutation=Mutation, types=[BookType])

    assert (
        str(schema).index(
            """
input SerializerMutationInput {
  id: ID!
  clientMutationId: String
}""".lstrip()
        )
        > -1
    )

    mutation = """
    mutation SerializerMutation($input: SerializerMutationInput!) {
        serializerMutation(input: $input) {
          title
          errors {
            field
            messages
            path
          }
        }
    }
    """

    # Test: Invalid ID
    with pytest.warns(UserWarning):  # Should not be called without context
        result = schema.execute(
            mutation, variables={"input": {"id": "asdf"}}, context={},
        )

    assert json.loads(json.dumps(result.data)) == {
        "serializerMutation": {
            "errors": [
                {"field": "id", "messages": ["Not a valid ID."], "path": ["id"]}
            ],
            "title": None,
        }
    }

    # Test: Invalid Object Type
    with pytest.warns(UserWarning):  # Should not be called without context
        result = schema.execute(
            mutation,
            variables={"input": {"id": to_global_id("AuthorType", 1)}},
            context={},
        )

    assert json.loads(json.dumps(result.data)) == {
        "serializerMutation": {
            "errors": [
                {
                    "field": "id",
                    "messages": ["Must receive a BookType ID."],
                    "path": ["id"],
                }
            ],
            "title": None,
        }
    }

    # Test: Successful
    with pytest.warns(UserWarning):  # Should not be called without context
        result = schema.execute(
            mutation,
            variables={"input": {"id": to_global_id("BookType", 2)}},
            context={},
        )

    assert json.loads(json.dumps(result.data)) == {
        "serializerMutation": {"errors": None, "title": "resolved title"}
    }


@pytest.mark.django_db()
def test_serializer_base_client_id_mutation_serializer_relay_id_field_without_method_name():
    class Serializer(serializers.Serializer):
        id = SerializerRelayIDField(BookType, node_class=SpriklNode, source="book")
        title = serializers.CharField(read_only=True)

        def create(self, validated_data):
            return validated_data.get("book")

    class SerializerMutation(SerializerClientIDCreateMutation):
        class Meta:
            serializer_class = Serializer

    class Mutation(graphene.ObjectType):
        serializer_mutation = SerializerMutation.Field()

    schema = graphene.Schema(mutation=Mutation, types=[BookType])

    mutation = """
    mutation SerializerMutation($input: SerializerMutationInput!) {
        serializerMutation(input: $input) {
          title
          errors {
            field
            messages
            path
          }
        }
    }
    """

    with pytest.warns(UserWarning):  # Should not be called without context
        result = schema.execute(
            mutation,
            variables={"input": {"id": to_global_id("BookType", 2)}},
            context={},
        )

    assert json.loads(json.dumps(result.data)) == {
        "serializerMutation": {
            "errors": [
                {
                    "field": "id",
                    "messages": ["No Book matches the given query."],
                    "path": ["id"],
                }
            ],
            "title": None,
        }
    }


@pytest.mark.django_db()
def test_serializer_base_client_id_mutation_convert_serializer_to_input_type():
    class NestedSerializer(serializers.Serializer):
        value = serializers.CharField()

    class Serializer(serializers.Serializer):
        nested = NestedSerializer(write_only=True)
        value = serializers.CharField(read_only=True)

        def create(self, validated_data):
            return validated_data.get("nested")

    class SerializerMutation(SerializerClientIDCreateMutation):
        class Meta:
            serializer_class = Serializer

    class Mutation(graphene.ObjectType):
        serializer_mutation = SerializerMutation.Field()

    schema = graphene.Schema(mutation=Mutation, types=[BookType])

    mutation = """
    mutation SerializerMutation($input: SerializerMutationInput!) {
        serializerMutation(input: $input) {
          value
          errors {
            field
            messages
            path
          }
        }
    }
    """

    with pytest.warns(UserWarning):  # Should not be called without context
        result = schema.execute(
            mutation, variables={"input": {"nested": {"value": "123"}}}, context={},
        )

    assert json.loads(json.dumps(result.data)) == {
        "serializerMutation": {"errors": None, "value": "123"}
    }
