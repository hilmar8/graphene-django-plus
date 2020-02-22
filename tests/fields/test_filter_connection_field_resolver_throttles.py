import pytest
from graphql_relay import to_global_id
from rest_framework.utils import json


@pytest.mark.django_db()
def test_filter_connection_field_resolver_throttle_classes(
    graphql_throttle_resolver_three_client, user_factory
):
    user = user_factory()

    graphql_throttle_resolver_three_client.force_authenticate(user)

    query = """
        query BooksFiltered {
            booksFiltered {
              totalCount
              edges {
                node {
                  id
                }
              }
            }
        }"""

    # Request one, not throttled
    response = graphql_throttle_resolver_three_client.execute(
        query, variables={"id": to_global_id("BookType", 1)},
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {'data': {'booksFiltered': {'edges': [], 'totalCount': 0}}}

    # Request two, throttled
    response = graphql_throttle_resolver_three_client.execute(
        query, variables={"id": to_global_id("BookType", 1)},
    )

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"booksFiltered": None},
        "errors": [
            {
                "locations": [{"column": 13, "line": 3}],
                "message": "Request was throttled. Expected available in 86400 seconds.",
                "path": ["booksFiltered"],
            }
        ],
    }
