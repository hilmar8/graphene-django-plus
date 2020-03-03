import pytest
from graphql_relay import to_global_id
from rest_framework.utils import json

QUERY = """
query OtherAsAdmin {
    otherAsAdmin
}"""


def test_list_field_permission_classes_without_authentication(graphql_client):
    response = graphql_client.execute(QUERY)

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"otherAsAdmin": None},
        "errors": [
            {
                "locations": [{"column": 5, "line": 3}],
                "message": "You do not have permission to perform this action.",
                "path": ["otherAsAdmin"],
            }
        ],
    }


@pytest.mark.django_db()
def test_list_field_permission_classes_without_permission(user_factory, graphql_client):
    user = user_factory()

    graphql_client.force_authenticate(user)

    response = graphql_client.execute(QUERY)

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "data": {"otherAsAdmin": None},
        "errors": [
            {
                "locations": [{"column": 5, "line": 3}],
                "message": "You do not have permission to perform this action.",
                "path": ["otherAsAdmin"],
            }
        ],
    }


@pytest.mark.django_db()
def test_list_field_permission_classes_with_permission(user_factory, graphql_client):
    user = user_factory(is_staff=True)

    graphql_client.force_authenticate(user)

    response = graphql_client.execute(QUERY)

    assert response.status_code == 200
    assert json.loads(response.content) == {"data": {"otherAsAdmin": ["1", "2"]}}
