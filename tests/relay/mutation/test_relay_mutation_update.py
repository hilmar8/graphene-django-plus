import pytest
from graphql_relay import to_global_id
from rest_framework.utils import json

from tests.test_app.test_app.app.models import Book


@pytest.mark.django_db()
def test_relay_mutation_update_without_any_input_at_all(graphql_client,):
    response = graphql_client.execute(
        """
  mutation UpdateRelayBook {
    updateRelayBook {
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
                "message": 'Field "updateRelayBook" argument "input" of type '
                '"UpdateRelayBookInput!" is required but not '
                "provided.",
            }
        ]
    }


@pytest.mark.django_db()
def test_relay_mutation_update_without_any_input_to_call(graphql_client,):
    response = graphql_client.execute(
        """
  mutation UpdateRelayBook($input: UpdateRelayBookInput!) {
    updateRelayBook(input: $input) {
      title
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
                '"UpdateRelayBookInput!" was not provided.',
            }
        ]
    }


@pytest.mark.django_db()
def test_relay_mutation_update_invalid_id(graphql_client,):
    response = graphql_client.execute(
        """
  mutation UpdateRelayBook($input: UpdateRelayBookInput!) {
    updateRelayBook(input: $input) {
      title
      errors {
        field
        messages
      }
    }
  }
""",
        {"input": {"id": "123", "title": ""}},
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"updateRelayBook": None},
        "errors": [
            {
                "locations": [{"column": 5, "line": 3}],
                "message": "No Book matches the given query.",
                "path": ["updateRelayBook"],
            }
        ],
    }


@pytest.mark.django_db()
def test_relay_mutation_update_invalid_input_type(graphql_client,):
    response = graphql_client.execute(
        """
  mutation UpdateRelayBook($input: UpdateRelayBookInput!) {
    updateRelayBook(input: $input) {
      title
      errors {
        field
        messages
      }
    }
  }
""",
        {"input": {"id": to_global_id("NotBookType", 1), "title": ""}},
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"updateRelayBook": None},
        "errors": [
            {
                "locations": [{"column": 5, "line": 3}],
                "message": "No Book matches the given query.",
                "path": ["updateRelayBook"],
            }
        ],
    }


@pytest.mark.django_db()
def test_relay_mutation_update_object_does_not_exist(graphql_client,):
    response = graphql_client.execute(
        """
  mutation UpdateRelayBook($input: UpdateRelayBookInput!) {
    updateRelayBook(input: $input) {
      title
      errors {
        field
        messages
      }
    }
  }
""",
        {"input": {"id": to_global_id("BookType", 1), "title": ""}},
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"updateRelayBook": None},
        "errors": [
            {
                "locations": [{"column": 5, "line": 3}],
                "message": "No Book matches the given query.",
                "path": ["updateRelayBook"],
            }
        ],
    }


@pytest.mark.django_db()
def test_relay_mutation_update_serializer_validation(graphql_client, book_factory):
    book = book_factory()

    response = graphql_client.execute(
        """
  mutation UpdateRelayBook($input: UpdateRelayBookInput!) {
    updateRelayBook(input: $input) {
      title
      errors {
        field
        messages
      }
    }
  }
""",
        {"input": {"id": to_global_id("BookType", book.pk), "title": ""}},
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {
            "updateRelayBook": {
                "errors": [
                    {"field": "title", "messages": ["This field may not be " "blank."]}
                ],
                "title": None,
            }
        }
    }


@pytest.mark.django_db()
def test_relay_mutation_update_serializer_successful(graphql_client, book_factory):
    book = book_factory()

    response = graphql_client.execute(
        """
  mutation UpdateRelayBook($input: UpdateRelayBookInput!) {
    updateRelayBook(input: $input) {
      title
      errors {
        field
        messages
      }
    }
  }
""",
        {"input": {"id": to_global_id("BookType", book.pk), "title": "new title"}},
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"updateRelayBook": {"errors": None, "title": "new title"}}
    }

    book.refresh_from_db()

    assert book.title == "new title"


@pytest.mark.django_db()
def test_relay_mutation_update_serializer_partial_without_input(
    graphql_client, book_factory
):
    book = book_factory()

    response = graphql_client.execute(
        """
  mutation UpdateRelayBookPartial($input: UpdateRelayBookPartialInput!) {
    updateRelayBookPartial(input: $input) {
      title
      errors {
        field
        messages
      }
    }
  }
""",
        {"input": {"id": to_global_id("BookType", book.pk)}},
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"updateRelayBookPartial": {"errors": None, "title": "book title"}}
    }


@pytest.mark.django_db()
def test_relay_mutation_update_serializer_partial_with_input(
    graphql_client, book_factory
):
    book = book_factory()

    response = graphql_client.execute(
        """
  mutation UpdateRelayBookPartial($input: UpdateRelayBookPartialInput!) {
    updateRelayBookPartial(input: $input) {
      title
      errors {
        field
        messages
      }
    }
  }
""",
        {"input": {"id": to_global_id("BookType", book.pk), "title": "new title"}},
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"updateRelayBookPartial": {"errors": None, "title": "new title"}}
    }

    book.refresh_from_db()

    assert book.title == "new title"
