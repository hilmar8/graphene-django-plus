import pytest
from graphql_relay import to_global_id
from rest_framework.utils import json


@pytest.mark.django_db()
def test_node_resolver_permission_classes_without_authentication(
    book_factory, graphql_admin_resolver_client
):
    book = book_factory()

    response = graphql_admin_resolver_client.execute(
        """
        query Book($id: ID!) {
            book(id: $id) {
              id
            }
        }""",
        variables={"id": to_global_id("BookType", book.pk)},
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"book": None},
        "errors": [
            {
                "locations": [{"column": 13, "line": 3}],
                "message": "You do not have permission to perform this action.",
                "path": ["book"],
            }
        ],
    }


@pytest.mark.django_db()
def test_node_resolver_permission_classes_without_permission(
    user_factory, book_factory, graphql_admin_resolver_client
):
    user = user_factory()
    book = book_factory()
    graphql_admin_resolver_client.force_authenticate(user)

    response = graphql_admin_resolver_client.execute(
        """
        query Book($id: ID!) {
            book(id: $id) {
              id
            }
        }""",
        variables={"id": to_global_id("BookType", book.pk)},
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"book": None},
        "errors": [
            {
                "locations": [{"column": 13, "line": 3}],
                "message": "You do not have permission to perform this action.",
                "path": ["book"],
            }
        ],
    }


@pytest.mark.django_db()
def test_node_resolver_permission_classes_with_permission(
    user_factory, book_factory, graphql_admin_resolver_client
):
    user = user_factory(is_staff=True)
    book = book_factory()

    graphql_admin_resolver_client.force_authenticate(user)

    response = graphql_admin_resolver_client.execute(
        """
        query Book($id: ID!) {
            book(id: $id) {
              id
            }
        }""",
        variables={"id": to_global_id("BookType", book.pk)},
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"book": {"id": to_global_id("BookType", book.pk)}}
    }
