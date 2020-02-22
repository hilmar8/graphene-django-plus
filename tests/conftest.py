import pytest
from django.urls import reverse
from graphql_relay import to_global_id
from rest_framework.test import APIClient


class GraphQLClient(APIClient):
    def __init__(self, schema_reverse, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.schema = reverse(schema_reverse)

    def execute(self, query, variables=None, operation_name=None, **extra):
        return self.post(
            self.schema,
            data={
                "query": query,
                "operationName": operation_name,
                "variables": variables,
            },
            format="json",
            **extra
        )


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture()
def graphql_client():
    return GraphQLClient("graphql")


@pytest.fixture()
def graphql_depth_client():
    return GraphQLClient("graphql-depth")


@pytest.fixture()
def graphql_introspection_client():
    return GraphQLClient("graphql-introspection")
