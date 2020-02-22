import functools

from graphql.execution.middleware import make_it_promise

from .fields import SpriklFilterConnectionField, SpriklField
from .permissions import check_permission_classes, check_throttle_classes
from .relay.node import SpriklNode


class TestMiddleware(object):
    def resolve(self, next, root, info, **args):
        if root is not None:
            return next(root, info, **args)

        resolver_fn = None
        if isinstance(next, functools.partial):
            resolver_fn = next
            if resolver_fn.func == make_it_promise:
                resolver_fn = resolver_fn.args[0]
        #     if resolver_fn.func == DjangoListField.list_resolver:
        #         resolver_fn = resolver_fn.args[0]
        #     if resolver_fn.func == default_resolver:
        #         resolver_fn = resolver_fn.args[0]

        # SpriklNode
        if hasattr(resolver_fn, "func") and (
            resolver_fn.func == SpriklNode.node_resolver
            or resolver_fn.func == SpriklFilterConnectionField.connection_resolver
            or resolver_fn.func == SpriklField.field_resolver
        ):
            return next(root, info, **args)

        # Permission classes
        if hasattr(resolver_fn, "permission_classes"):
            permission_classes = resolver_fn.permission_classes
        else:
            permission_classes = info.context.get("view").resolver_permission_classes

        check_permission_classes(info, None, permission_classes)

        # Throttle classes
        if hasattr(resolver_fn, "throttle_classes"):
            throttle_classes = resolver_fn.throttle_classes
            check_throttle_classes(info, None, throttle_classes)
        #
        # if permission_classes is not None:
        #     for permission in [p() for p in permission_classes]:
        #         if not permission.has_permission(
        #             info.context.get("request"), info.context.get("view")
        #         ):
        #             raise PermissionDenied(detail=getattr(permission, "message", None))
        #
        return next(root, info, **args)
