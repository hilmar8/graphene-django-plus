import pytest
from graphql_relay import to_global_id
from rest_framework.utils import json


@pytest.mark.django_db()
def test_depth_validator_normal_depth(graphql_depth_client):
    response = graphql_depth_client.execute(
        """
        query Book($id: ID!) {
            book(id: $id) {
              id
              title
            }
        }""",
        variables={"id": to_global_id("BookType", 1)},
    )

    assert json.loads(response.content) == {"data": {"book": None}}


@pytest.mark.django_db()
def test_depth_validator_depth_of_two(graphql_depth_client):
    response = graphql_depth_client.execute(
        """
        query Book($id: ID!) {
            book(id: $id) {
              id
              title
              publisher {
                id
                name
                allBooks {
                  id
                  title
                }
              }
            }
        }""",
        variables={"id": to_global_id("BookType", 1)},
    )

    assert json.loads(response.content) == {
        "errors": [
            {"message": 'Operation "Book" exceeds maximum operation depth of 2.'}
        ]
    }


@pytest.mark.django_db()
def test_introspection_validator_schema(graphql_introspection_client):
    response = graphql_introspection_client.execute(
        """
        {
          __schema {
            queryType {
              name
            }
          }
        }""",
    )

    assert json.loads(response.content) == {
        "errors": [
            {
                "message": "GraphQL introspection is not allowed, but the query contained __schema or __type."
            }
        ]
    }


@pytest.mark.django_db()
def test_introspection_validator_type(graphql_introspection_client):
    response = graphql_introspection_client.execute(
        """
        {
          __type(name: "BookType") {
            name
          }
        }""",
    )

    assert json.loads(response.content) == {
        "errors": [
            {
                "message": "GraphQL introspection is not allowed, but the query contained __schema or __type."
            }
        ]
    }
