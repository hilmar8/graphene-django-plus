import pytest
from rest_framework.utils import json


@pytest.mark.django_db()
def test_relay_mutation_create_throttle_classes(
    graphql_client, user_factory
):
    user = user_factory()

    graphql_client.force_authenticate(user)

    mutation = """
  mutation CreateRelayBookThrottle($input: CreateRelayBookInput!) {
    createRelayBookThrottle(input: $input) {
      title
      errors {
        field
        messages
      }
    }
  }
"""

    # Request one, not throttled
    response = graphql_client.execute(
        mutation, {"input": {"title": ""}}
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {
            "createRelayBookThrottle": {
                "errors": [
                    {"field": "title", "messages": ["This field may not be blank."]}
                ],
                "title": None,
            }
        }
    }

    # Request two, throttled
    response = graphql_client.execute(
        mutation, {"input": {"title": ""}}
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"createRelayBookThrottle": None},
        "errors": [
            {
                "locations": [{"column": 5, "line": 3}],
                "message": "Request was throttled. Expected available in 86400 seconds.",
                "path": ["createRelayBookThrottle"],
            }
        ],
    }
