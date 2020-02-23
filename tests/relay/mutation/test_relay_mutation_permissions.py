import pytest
from graphql_relay import to_global_id
from rest_framework.utils import json

CREATE_MUTATION = """
  mutation CreateRelayBookAdmin($input: CreateRelayBookInput!) {
    createRelayBookAdmin(input: $input) {
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

UPDATE_MUTATION = """
  mutation UpdateRelayBookAdmin($input: UpdateRelayBookInput!) {
    updateRelayBookAdmin(input: $input) {
      errors {
        field
        messages
      }
    }
  }
"""


@pytest.mark.django_db()
def test_relay_mutation_create_permission_classes_without_authentication(
    graphql_client,
):
    response = graphql_client.execute(CREATE_MUTATION, {"input": {"title": "new book"}})

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"createRelayBookAdmin": None},
        "errors": [
            {
                "locations": [{"column": 5, "line": 3}],
                "message": "You do not have permission to perform this action.",
                "path": ["createRelayBookAdmin"],
            }
        ],
    }


@pytest.mark.django_db()
def test_relay_mutation_create_permission_classes_without_permission(
    user_factory, graphql_client
):
    user = user_factory()
    graphql_client.force_authenticate(user)

    response = graphql_client.execute(CREATE_MUTATION, {"input": {"title": "new book"}})

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"createRelayBookAdmin": None},
        "errors": [
            {
                "locations": [{"column": 5, "line": 3}],
                "message": "You do not have permission to perform this action.",
                "path": ["createRelayBookAdmin"],
            }
        ],
    }


@pytest.mark.django_db()
def test_relay_mutation_create_permission_classes_with_permission(
    user_factory, graphql_client
):
    user = user_factory(is_staff=True)

    graphql_client.force_authenticate(user)

    response = graphql_client.execute(CREATE_MUTATION, {"input": {"title": ""}})

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {
            "createRelayBookAdmin": {
                "errors": [
                    {"field": "title", "messages": ["This field may not be blank."]}
                ],
                "book": None,
            }
        }
    }


@pytest.mark.django_db()
def test_relay_mutation_update_permission_classes_without_authentication(
    graphql_client,
):
    response = graphql_client.execute(
        UPDATE_MUTATION,
        {"input": {"id": to_global_id("BookType", 1), "title": "new title"}},
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"updateRelayBookAdmin": None},
        "errors": [
            {
                "locations": [{"column": 5, "line": 3}],
                "message": "You do not have permission to perform this action.",
                "path": ["updateRelayBookAdmin"],
            }
        ],
    }


@pytest.mark.django_db()
def test_relay_mutation_update_permission_classes_without_permission(
    user_factory, graphql_client
):
    user = user_factory()
    graphql_client.force_authenticate(user)

    response = graphql_client.execute(
        UPDATE_MUTATION,
        {"input": {"id": to_global_id("BookType", 1), "title": "new title"}},
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"updateRelayBookAdmin": None},
        "errors": [
            {
                "locations": [{"column": 5, "line": 3}],
                "message": "You do not have permission to perform this action.",
                "path": ["updateRelayBookAdmin"],
            }
        ],
    }


@pytest.mark.django_db()
def test_relay_mutation_update_permission_classes_with_permission(
    user_factory, graphql_client
):
    user = user_factory(is_staff=True)

    graphql_client.force_authenticate(user)

    response = graphql_client.execute(
        UPDATE_MUTATION,
        {"input": {"id": to_global_id("BookType", 1), "title": "new title"}},
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"updateRelayBookAdmin": None},
        "errors": [
            {
                "locations": [{"column": 5, "line": 3}],
                "message": "No Book matches the given query.",
                "path": ["updateRelayBookAdmin"],
            }
        ],
    }
