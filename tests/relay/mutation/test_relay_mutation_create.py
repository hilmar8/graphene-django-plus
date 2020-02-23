import pytest
from graphql_relay import to_global_id
from rest_framework.utils import json

from tests.test_app.test_app.app.models import Book


@pytest.mark.django_db()
def test_relay_mutation_create_without_any_input_at_all(graphql_client,):
    response = graphql_client.execute(
        """
  mutation CreateRelayBook {
    createRelayBook {
      book {
        title
      }
      errors {
        field
        messages
      }
    }
  }
"""
    )

    assert response.status_code == 400
    assert json.loads(response.content) == {
        "errors": [
            {
                "locations": [{"column": 5, "line": 3}],
                "message": 'Field "createRelayBook" argument "input" of type '
                '"CreateRelayBookInput!" is required but not '
                "provided.",
            }
        ]
    }


@pytest.mark.django_db()
def test_relay_mutation_create_without_any_input_to_call(graphql_client,):
    response = graphql_client.execute(
        """
  mutation CreateRelayBook($input: CreateRelayBookInput!) {
    createRelayBook(input: $input) {
      book {
        title
      }
      errors {
        field
        messages
      }
    }
  }
"""
    )

    assert response.status_code == 400
    assert json.loads(response.content) == {
        "errors": [
            {
                "locations": [{"column": 28, "line": 2}],
                "message": 'Variable "$input" of required type '
                '"CreateRelayBookInput!" was not provided.',
            }
        ]
    }


@pytest.mark.django_db()
def test_relay_mutation_create_serializer_validation(graphql_client,):
    response = graphql_client.execute(
        """
  mutation CreateRelayBook($input: CreateRelayBookInput!) {
    createRelayBook(input: $input) {
      book {
        title
      }
      errors {
        field
        messages
      }
    }
  }
""",
        {"input": {"title": ""}},
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {
            "createRelayBook": {
                "errors": [
                    {"field": "title", "messages": ["This field may not be " "blank."]}
                ],
                "book": None,
            }
        }
    }


@pytest.mark.django_db()
def test_relay_mutation_create_serializer_successful(graphql_client,):
    response = graphql_client.execute(
        """
  mutation CreateRelayBook($input: CreateRelayBookInput!) {
    createRelayBook(input: $input) {
      book {
        id
        title
      }
      errors {
        field
        messages
      }
    }
  }
""",
        {"input": {"title": "new book"}},
    )

    created = Book.objects.get(title="new book")

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"createRelayBook": {"errors": None, "book": {
            "id": to_global_id("BookType", created.pk),
            "title": "new book",
        }}}
    }

    assert created.delete()
