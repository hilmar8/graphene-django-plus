import pytest
from rest_framework.utils import json

MUTATION = """
  mutation CreateRelayBookAdmin($input: CreateRelayBookInput!) {
    createRelayBookAdmin(input: $input) {
      title
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
    response = graphql_client.execute(MUTATION, {"input": {"title": "new book"}})

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

    response = graphql_client.execute(MUTATION, {"input": {"title": "new book"}})

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

    response = graphql_client.execute(MUTATION, {"input": {"title": ""}})

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {
            "createRelayBookAdmin": {
                "errors": [
                    {"field": "title", "messages": ["This field may not be blank."]}
                ],
                "title": None,
            }
        }
    }
