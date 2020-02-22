import pytest
from graphql_relay import to_global_id
from rest_framework.utils import json

QUERY = """
query BooksFilteredAsAdmin {
    booksFilteredAsAdmin {
      totalCount
      edges {
        node {
          id
        }
      }
    }
}"""


@pytest.mark.django_db()
def test_filter_connection_field_permission_classes_without_authentication(
    book_factory, graphql_client
):
    book_factory()

    response = graphql_client.execute(QUERY)

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"booksFilteredAsAdmin": None},
        "errors": [
            {
                "locations": [{"column": 5, "line": 3}],
                "message": "You do not have permission to perform this action.",
                "path": ["booksFilteredAsAdmin"],
            }
        ],
    }


@pytest.mark.django_db()
def test_filter_connection_field_permission_classes_without_permission(
    user_factory, book_factory, graphql_client
):
    user = user_factory()
    book_factory()
    graphql_client.force_authenticate(user)

    response = graphql_client.execute(QUERY)

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"booksFilteredAsAdmin": None},
        "errors": [
            {
                "locations": [{"column": 5, "line": 3}],
                "message": "You do not have permission to perform this action.",
                "path": ["booksFilteredAsAdmin"],
            }
        ],
    }


@pytest.mark.django_db()
def test_filter_connection_field_permission_classes_with_permission(
    user_factory, book_factory, graphql_client
):
    user = user_factory(is_staff=True)
    book = book_factory()

    graphql_client.force_authenticate(user)

    response = graphql_client.execute(QUERY)

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {
            "booksFilteredAsAdmin": {
                "edges": [{"node": {"id": to_global_id("BookType", book.pk)}}],
                "totalCount": 1,
            }
        }
    }
