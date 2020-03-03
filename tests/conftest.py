import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from graphql_relay import to_global_id
from rest_framework.test import APIClient

from tests import factories
from tests.test_app.test_app.app.models import Book


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


@pytest.fixture()
def graphql_auth_client():
    return GraphQLClient("graphql-auth")


@pytest.fixture()
def graphql_admin_client():
    return GraphQLClient("graphql-admin")


@pytest.fixture()
def graphql_admin_resolver_client():
    return GraphQLClient("graphql-admin-resolver")


@pytest.fixture()
def graphql_throttle_client():
    return GraphQLClient("graphql-throttle")


@pytest.fixture()
def graphql_throttle_resolver_client():
    return GraphQLClient("graphql-throttle-resolver")


@pytest.fixture()
def graphql_throttle_resolver_two_client():
    return GraphQLClient("graphql-throttle-resolver-2")


@pytest.fixture()
def graphql_throttle_resolver_three_client():
    return GraphQLClient("graphql-throttle-resolver-3")


@pytest.fixture()
def graphql_throttle_resolver_four_client():
    return GraphQLClient("graphql-throttle-resolver-4")


@pytest.fixture()
def graphql_throttle_resolver_five_client():
    return GraphQLClient("graphql-throttle-resolver-5")


@pytest.fixture()
def graphql_throttle_resolver_six_client():
    return GraphQLClient("graphql-throttle-resolver-6")


# Model Factories


def _factory(cls, fct, request):
    created_list = []

    def create(*args, **kwargs) -> cls:
        created = fct.create(*args, **kwargs)
        created_list.append(created)
        return created

    def cleanup():
        for c in created_list:
            c.delete()

    request.addfinalizer(cleanup)
    return create


@pytest.fixture()
def book_factory(request):
    return _factory(Book, factories.BookFactory, request)


@pytest.fixture()
def user_factory(request):
    return _factory(User, factories.UserFactory, request)
