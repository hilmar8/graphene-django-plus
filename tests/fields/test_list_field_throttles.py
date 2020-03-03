import pytest
from graphql_relay import to_global_id
from rest_framework.utils import json


@pytest.mark.django_db()
def test_list_field_throttle_classes(graphql_client, user_factory):
    user = user_factory()

    graphql_client.force_authenticate(user)

    query = """
        query OtherThrottle {
            otherThrottle
        }"""

    # Request one, not throttled
    response = graphql_client.execute(query)

    assert response.status_code == 200
    assert json.loads(response.content) == {"data": {"otherThrottle": ["1", "2"]}}

    # Request two, throttled
    response = graphql_client.execute(query)

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"otherThrottle": None},
        "errors": [
            {
                "locations": [{"column": 13, "line": 3}],
                "message": "Request was throttled. Expected available in 86400 seconds.",
                "path": ["otherThrottle"],
            }
        ],
    }
