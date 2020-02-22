import pytest
from graphql_relay import to_global_id
from rest_framework.utils import json


@pytest.mark.django_db()
def test_connection_field_resolver_permission_classes_without_authentication(
    book_factory, graphql_admin_resolver_client
):
    book_factory()

    response = graphql_admin_resolver_client.execute(
        """
        query Books {
            books {
              totalCount
              edges {
                node {
                  id
                }
              }
            }
        }""",
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"books": None},
        "errors": [
            {
                "locations": [{"column": 13, "line": 3}],
                "message": "You do not have permission to perform this action.",
                "path": ["books"],
            }
        ],
    }


@pytest.mark.django_db()
def test_connection_field_resolver_permission_classes_without_permission(
    user_factory, book_factory, graphql_admin_resolver_client
):
    user = user_factory()
    book_factory()
    graphql_admin_resolver_client.force_authenticate(user)

    response = graphql_admin_resolver_client.execute(
        """
        query Books {
            books {
              totalCount
              edges {
                node {
                  id
                }
              }
            }
        }""",
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"books": None},
        "errors": [
            {
                "locations": [{"column": 13, "line": 3}],
                "message": "You do not have permission to perform this action.",
                "path": ["books"],
            }
        ],
    }


@pytest.mark.django_db()
def test_connection_field_resolver_permission_classes_with_permission(
    user_factory, book_factory, graphql_admin_resolver_client
):
    user = user_factory(is_staff=True)
    book = book_factory()

    graphql_admin_resolver_client.force_authenticate(user)

    response = graphql_admin_resolver_client.execute(
        """
        query Books {
            books {
              totalCount
              edges {
                node {
                  id
                }
              }
            }
        }""",
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {
            "books": {
                "edges": [{"node": {"id": to_global_id("BookType", book.pk)}}],
                "totalCount": 1,
            }
        }
    }
