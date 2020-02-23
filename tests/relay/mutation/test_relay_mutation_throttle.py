import pytest
from graphql_relay import to_global_id
from rest_framework.utils import json


@pytest.mark.django_db()
def test_relay_mutation_create_throttle_classes(graphql_client, user_factory):
    user = user_factory()

    graphql_client.force_authenticate(user)

    mutation = """
  mutation CreateRelayBookThrottle($input: CreateRelayBookInput!) {
    createRelayBookThrottle(input: $input) {
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

    # Request one, not throttled
    response = graphql_client.execute(mutation, {"input": {"title": ""}})

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {
            "createRelayBookThrottle": {
                "errors": [
                    {"field": "title", "messages": ["This field may not be blank."]}
                ],
                "book": None,
            }
        }
    }

    # Request two, throttled
    response = graphql_client.execute(mutation, {"input": {"title": ""}})

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


@pytest.mark.django_db()
def test_relay_mutation_update_throttle_classes(graphql_client, user_factory):
    user = user_factory()

    graphql_client.force_authenticate(user)

    mutation = """
  mutation UpdateRelayBookThrottle($input: UpdateRelayBookInput!) {
    updateRelayBookThrottle(input: $input) {
      errors {
        field
        messages
      }
    }
  }
"""

    # Request one, not throttled
    response = graphql_client.execute(
        mutation, {"input": {"id": to_global_id("BookType", 1), "title": ""}}
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"updateRelayBookThrottle": None},
        "errors": [
            {
                "locations": [{"column": 5, "line": 3}],
                "message": "No Book matches the given query.",
                "path": ["updateRelayBookThrottle"],
            }
        ],
    }

    # Request two, throttled
    response = graphql_client.execute(
        mutation, {"input": {"id": to_global_id("BookType", 1), "title": ""}}
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"updateRelayBookThrottle": None},
        "errors": [
            {
                "locations": [{"column": 5, "line": 3}],
                "message": "Request was throttled. Expected available in 86400 seconds.",
                "path": ["updateRelayBookThrottle"],
            }
        ],
    }
