import pytest
from rest_framework.utils import json


@pytest.mark.django_db()
def test_relay_mutation_create_resolver_throttle_classes(
    graphql_throttle_resolver_four_client, user_factory
):
    user = user_factory()

    graphql_throttle_resolver_four_client.force_authenticate(user)

    mutation = """
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

    # Request one, not throttled
    response = graphql_throttle_resolver_four_client.execute(
        mutation, {"input": {"title": ""}}
    )

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

    # Request two, throttled
    response = graphql_throttle_resolver_four_client.execute(
        mutation, {"input": {"title": ""}}
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"createRelayBook": None},
        "errors": [
            {
                "locations": [{"column": 5, "line": 3}],
                "message": "Request was throttled. Expected available in 86400 seconds.",
                "path": ["createRelayBook"],
            }
        ],
    }
