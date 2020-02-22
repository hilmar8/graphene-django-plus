from graphene_django_hilmarh.routers import TestRouter
from tests.test_app.test_app.app.typesets import (
    BookRelayTypeSet,
    BookRelayAdminTypeSet,
    BookRelayThrottleTypeSet,
)

test_router = TestRouter()

test_router.register("book", BookRelayTypeSet)
test_router.register("book_admin", BookRelayAdminTypeSet)
test_router.register("book_admin", BookRelayThrottleTypeSet)

query = test_router.query()
