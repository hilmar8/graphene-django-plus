import pytest
from graphql_relay import to_global_id
from rest_framework.utils import json


@pytest.mark.django_db()
def test_node_permission_classes_without_authentication(book_factory, graphql_client):
    book = book_factory()

    response = graphql_client.execute(
        """
        query BookAsAdmin($id: ID!) {
            bookAsAdmin(id: $id) {
              id
            }
        }""",
        variables={"id": to_global_id("BookType", book.pk)},
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"bookAsAdmin": None},
        "errors": [
            {
                "locations": [{"column": 13, "line": 3}],
                "message": "You do not have permission to perform this action.",
                "path": ["bookAsAdmin"],
            }
        ],
    }


@pytest.mark.django_db()
def test_node_permission_classes_without_permission(
    user_factory, book_factory, graphql_client
):
    user = user_factory()
    book = book_factory()
    graphql_client.force_authenticate(user)

    response = graphql_client.execute(
        """
        query BookAsAdmin($id: ID!) {
            bookAsAdmin(id: $id) {
              id
            }
        }""",
        variables={"id": to_global_id("BookType", book.pk)},
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"bookAsAdmin": None},
        "errors": [
            {
                "locations": [{"column": 13, "line": 3}],
                "message": "You do not have permission to perform this action.",
                "path": ["bookAsAdmin"],
            }
        ],
    }


@pytest.mark.django_db()
def test_node_permission_classes_with_permission(
    user_factory, book_factory, graphql_client
):
    user = user_factory(is_staff=True)
    book = book_factory()

    graphql_client.force_authenticate(user)

    response = graphql_client.execute(
        """
        query BookAsAdmin($id: ID!) {
            bookAsAdmin(id: $id) {
              id
            }
        }""",
        variables={"id": to_global_id("BookType", book.pk)},
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"bookAsAdmin": {"id": to_global_id("BookType", book.pk)}}
    }
