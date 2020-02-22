import pytest
from graphql_relay import to_global_id
from rest_framework.utils import json


@pytest.mark.django_db()
def test_connection_field_esolver_throttle_classes(
    graphql_throttle_resolver_two_client, user_factory
):
    user = user_factory()

    graphql_throttle_resolver_two_client.force_authenticate(user)

    query = """
        query Books {
            books {
              totalCount
              edges {
                node {
                  id
                }
              }
            }
        }"""

    # Request one, not throttled
    response = graphql_throttle_resolver_two_client.execute(
        query, variables={"id": to_global_id("BookType", 1)},
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {'data': {'books': {'edges': [], 'totalCount': 0}}}

    # Request two, throttled
    response = graphql_throttle_resolver_two_client.execute(
        query, variables={"id": to_global_id("BookType", 1)},
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"books": None},
        "errors": [
            {
                "locations": [{"column": 13, "line": 3}],
                "message": "Request was throttled. Expected available in 86400 seconds.",
                "path": ["books"],
            }
        ],
    }
