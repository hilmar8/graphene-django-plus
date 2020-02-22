import pytest
from graphql_relay import to_global_id
from rest_framework.utils import json

QUERY = """
query BooksFiltered {
    booksFiltered {
      totalCount
      edges {
        node {
          id
        }
      }
    }
}"""


@pytest.mark.django_db()
def test_filter_connection_field_resolver_permission_classes_without_authentication(
    book_factory, graphql_admin_resolver_client
):
    book_factory()

    response = graphql_admin_resolver_client.execute(QUERY)

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"booksFiltered": None},
        "errors": [
            {
                "locations": [{"column": 5, "line": 3}],
                "message": "You do not have permission to perform this action.",
                "path": ["booksFiltered"],
            }
        ],
    }


@pytest.mark.django_db()
def test_filter_connection_field_resolver_permission_classes_without_permission(
    user_factory, book_factory, graphql_admin_resolver_client
):
    user = user_factory()
    book_factory()
    graphql_admin_resolver_client.force_authenticate(user)

    response = graphql_admin_resolver_client.execute(QUERY)

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"booksFiltered": None},
        "errors": [
            {
                "locations": [{"column": 5, "line": 3}],
                "message": "You do not have permission to perform this action.",
                "path": ["booksFiltered"],
            }
        ],
    }


@pytest.mark.django_db()
def test_filter_connection_field_resolver_permission_classes_with_permission(
    user_factory, book_factory, graphql_admin_resolver_client
):
    user = user_factory(is_staff=True)
    book = book_factory()

    graphql_admin_resolver_client.force_authenticate(user)

    response = graphql_admin_resolver_client.execute(QUERY)

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {
            "booksFiltered": {
                "edges": [{"node": {"id": to_global_id("BookType", book.pk)}}],
                "totalCount": 1,
            }
        }
    }
