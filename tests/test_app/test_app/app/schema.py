import graphene
from rest_framework.permissions import IsAdminUser

from graphene_django_plus.fields import PlusListField
from graphene_django_plus.routers import TestRouter
from tests.test_app.test_app.app.mutations import (
    CreateRelayBookMutation,
    UpdateRelayBookMutation,
    UpdateRelayBookPartialMutation,
)
from tests.test_app.test_app.app.typesets import (
    BookRelayTypeSet,
    BookRelayAdminTypeSet,
    BookRelayThrottleTypeSet,
    BookRelayFilteredTypeSet,
    BookRelayFilteredAdminTypeSet,
    BookRelayFilteredThrottleTypeSet,
)
from tests.test_app.test_app.throttles import (
    ThrottleEight,
    ThrottleEleven,
    ThrottleThirteen,
)

test_router = TestRouter()

test_router.register("book", BookRelayTypeSet)
test_router.register("book_admin", BookRelayAdminTypeSet)
test_router.register("book_throttle", BookRelayThrottleTypeSet)
test_router.register("book_filtered", BookRelayFilteredTypeSet)
test_router.register("book_filtered_admin", BookRelayFilteredAdminTypeSet)
test_router.register("book_filtered_throttle", BookRelayFilteredThrottleTypeSet)

_query = test_router.query()


class Query(_query):
    other = PlusListField(graphene.String)
    other_as_admin = PlusListField(graphene.String, permission_classes=[IsAdminUser])
    other_throttle = PlusListField(
        graphene.String, throttle_classes=[ThrottleThirteen]
    )

    def resolve_other(self, info):
        return ["1", "2"]

    def resolve_other_as_admin(self, info):
        return ["1", "2"]

    def resolve_other_throttle(self, info):
        return ["1", "2"]


class Mutation:
    create_relay_book = CreateRelayBookMutation.Field()
    create_relay_book_admin = CreateRelayBookMutation.Field(
        permission_classes=[IsAdminUser]
    )
    create_relay_book_throttle = CreateRelayBookMutation.Field(
        throttle_classes=[ThrottleEight]
    )

    update_relay_book = UpdateRelayBookMutation.Field()
    update_relay_book_admin = UpdateRelayBookMutation.Field(
        permission_classes=[IsAdminUser]
    )
    update_relay_book_throttle = UpdateRelayBookMutation.Field(
        throttle_classes=[ThrottleEleven]
    )

    update_relay_book_partial = UpdateRelayBookPartialMutation.Field()
