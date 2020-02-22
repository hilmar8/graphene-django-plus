import pytest
from graphql_relay import to_global_id
from rest_framework.utils import json


@pytest.mark.django_db()
def test_django_connection_total_count(django_assert_num_queries, book_factory, graphql_client):
    book_1 = book_factory()
    book_2 = book_factory()

    with django_assert_num_queries(2):
        # TODO: Is it possble to make this query without selecting all books? (queries: 1, only count)
        response = graphql_client.execute(
            """
            query Books {
                books {
                  totalCount
                }
            }"""
        )

        assert json.loads(response.content) == {
            "data": {
                "books": {
                    "totalCount": 2
                }
            }
        }
