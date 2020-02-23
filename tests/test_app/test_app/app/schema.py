from rest_framework.permissions import IsAdminUser

from graphene_django_hilmarh.routers import TestRouter
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
from tests.test_app.test_app.throttles import ThrottleEight, ThrottleEleven

test_router = TestRouter()

test_router.register("book", BookRelayTypeSet)
test_router.register("book_admin", BookRelayAdminTypeSet)
test_router.register("book_throttle", BookRelayThrottleTypeSet)
test_router.register("book_filtered", BookRelayFilteredTypeSet)
test_router.register("book_filtered_admin", BookRelayFilteredAdminTypeSet)
test_router.register("book_filtered_throttle", BookRelayFilteredThrottleTypeSet)

query = test_router.query()


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
