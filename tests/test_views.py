import pytest
from graphql_relay import to_global_id
from rest_framework.utils import json


@pytest.mark.django_db()
def test_authentication_view_without_authentication(graphql_auth_client):
    response = graphql_auth_client.execute(
        """
        query Book($id: ID!) {
            book(id: $id) {
              id
            }
        }""",
        variables={"id": to_global_id("BookType", 1)},
    )

    assert response.status_code == 401
    assert json.loads(response.content) == {
        "errors": [{"message": "Authentication credentials were not provided."}]
    }


@pytest.mark.django_db()
def test_admin_view_without_permission(graphql_admin_client, django_user_model):
    user = django_user_model.objects.create(username="someone", password="something")

    graphql_admin_client.force_authenticate(user)

    response = graphql_admin_client.execute(
        """
        query Book($id: ID!) {
            book(id: $id) {
              id
            }
        }""",
        variables={"id": to_global_id("BookType", 1)},
    )

    assert response.status_code == 403
    assert json.loads(response.content) == {
        "errors": [{"message": "You do not have permission to perform this action."}]
    }

    user.delete()


@pytest.mark.django_db()
def test_admin_view_with_permission(graphql_admin_client, django_user_model):
    user = django_user_model.objects.create(
        username="someone", password="something", is_staff=True
    )

    graphql_admin_client.force_authenticate(user)

    response = graphql_admin_client.execute(
        """
        query Book($id: ID!) {
            book(id: $id) {
              id
            }
        }""",
        variables={"id": to_global_id("BookType", 1)},
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {"data": {"book": None}}

    user.delete()


@pytest.mark.django_db()
def test_throttle_view(graphql_throttle_client, user_factory):
    user = user_factory()

    graphql_throttle_client.force_authenticate(user)

    query = """
        query Book($id: ID!) {
            book(id: $id) {
              id
            }
        }"""

    # Request one, not throttled
    response = graphql_throttle_client.execute(
        query, variables={"id": to_global_id("BookType", 1)},
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {"data": {"book": None}}

    # Request two, throttled
    response = graphql_throttle_client.execute(
        query, variables={"id": to_global_id("BookType", 1)},
    )

    assert response.status_code == 429
    assert json.loads(response.content) == {
        "errors": [
            {"message": "Request was throttled. Expected available in 86400 seconds."}
        ]
    }
