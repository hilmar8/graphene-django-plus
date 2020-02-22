import pytest
from rest_framework.utils import json

MUTATION = """
  mutation CreateRelayBook($input: CreateRelayBookInput!) {
    createRelayBook(input: $input) {
      title
      errors {
        field
        messages
      }
    }
  }
"""


@pytest.mark.django_db()
def test_relay_mutation_create_resolver_permission_classes_without_authentication(
    graphql_admin_resolver_client,
):
    response = graphql_admin_resolver_client.execute(
        MUTATION, {"input": {"title": "new book"}}
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"createRelayBook": None},
        "errors": [
            {
                "locations": [{"column": 5, "line": 3}],
                "message": "You do not have permission to perform this action.",
                "path": ["createRelayBook"],
            }
        ],
    }


@pytest.mark.django_db()
def test_relay_mutation_create_resolver_permission_classes_without_permission(
    user_factory, book_factory, graphql_admin_resolver_client
):
    user = user_factory()
    graphql_admin_resolver_client.force_authenticate(user)

    response = graphql_admin_resolver_client.execute(
        MUTATION, {"input": {"title": "new book"}}
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"createRelayBook": None},
        "errors": [
            {
                "locations": [{"column": 5, "line": 3}],
                "message": "You do not have permission to perform this action.",
                "path": ["createRelayBook"],
            }
        ],
    }


@pytest.mark.django_db()
def test_relay_mutation_create_resolver_permission_classes_with_permission(
    user_factory, graphql_admin_resolver_client
):
    user = user_factory(is_staff=True)

    graphql_admin_resolver_client.force_authenticate(user)

    response = graphql_admin_resolver_client.execute(MUTATION, {"input": {"title": ""}})

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {
            "createRelayBook": {
                "errors": [
                    {"field": "title", "messages": ["This field may not be blank."]}
                ],
                "title": None,
            }
        }
    }
