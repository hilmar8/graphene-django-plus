import warnings

from rest_framework.exceptions import PermissionDenied, Throttled


def check_permission_classes(info, field, permission_classes):
    if permission_classes is None:
        if hasattr(info, "context") and info.context and info.context.get("view", None):
            permission_classes = info.context.get("view").resolver_permission_classes
        else:
            warnings.warn(
                UserWarning(
                    "{} should not be called without context.".format(field.__name__)
                )
            )

    if permission_classes is not None:
        for permission in [p() for p in permission_classes]:
            if not permission.has_permission(
                info.context.get("request"), info.context.get("view")
            ):
                raise PermissionDenied(detail=getattr(permission, "message", None))


def check_throttle_classes(info, field, throttle_classes):
    if throttle_classes is None:
        if hasattr(info, "context") and info.context and info.context.get("view", None):
            throttle_classes = info.context.get("view").resolver_throttle_classes
        else:
            warnings.warn(
                UserWarning(
                    "{} should not be called without context.".format(field.__name__)
                )
            )

    if throttle_classes is not None:
        for throttle in [t() for t in throttle_classes]:
            if not throttle.allow_request(
                info.context.get("request"), info.context.get("view")
            ):
                raise Throttled(throttle.wait())
