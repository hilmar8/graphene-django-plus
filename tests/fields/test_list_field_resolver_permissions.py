import pytest
from graphql_relay import to_global_id
from rest_framework.utils import json

QUERY = """
query Other {
    other
}"""


@pytest.mark.django_db()
def test_list_field_resolver_permission_classes_without_authentication(
    graphql_admin_resolver_client
):
    response = graphql_admin_resolver_client.execute(QUERY)

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"other": None},
        "errors": [
            {
                "locations": [{"column": 5, "line": 3}],
                "message": "You do not have permission to perform this action.",
                "path": ["other"],
            }
        ],
    }


@pytest.mark.django_db()
def test_list_field_resolver_permission_classes_without_permission(
    user_factory, graphql_admin_resolver_client
):
    user = user_factory()

    graphql_admin_resolver_client.force_authenticate(user)

    response = graphql_admin_resolver_client.execute(QUERY)

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"other": None},
        "errors": [
            {
                "locations": [{"column": 5, "line": 3}],
                "message": "You do not have permission to perform this action.",
                "path": ["other"],
            }
        ],
    }


@pytest.mark.django_db()
def test_list_field_resolver_permission_classes_with_permission(
    user_factory, graphql_admin_resolver_client
):
    user = user_factory(is_staff=True)

    graphql_admin_resolver_client.force_authenticate(user)

    response = graphql_admin_resolver_client.execute(QUERY)

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {
            "other": ['1', '2']
        }
    }
