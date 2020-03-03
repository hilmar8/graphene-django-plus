from functools import partial

import graphene
from graphene import Field, List, NonNull
from graphene.types.utils import get_type
from graphene_django import DjangoConnectionField
from graphene_django.fields import DjangoListField
from graphene_django.filter import DjangoFilterConnectionField

from .permissions import check_permission_classes, check_throttle_classes


class SpriklConnectionField(DjangoConnectionField):
    def __init__(self, *args, **kwargs):
        self.permission_classes = kwargs.pop("permission_classes", None)
        self.throttle_classes = kwargs.pop("throttle_classes", None)

        super().__init__(*args, **kwargs)

    @classmethod
    def resolve_connection(cls, connection, args, iterable):
        connection = super().resolve_connection(connection, args, iterable)
        connection.total_count = connection.length
        return connection

    @classmethod
    def connection_resolver(
        cls,
        resolver,
        connection,
        default_manager,
        queryset_resolver,
        max_limit,
        enforce_first_or_last,
        permission_classes,
        throttle_classes,
        root,
        info,
        **args
    ):
        check_permission_classes(info, cls, permission_classes)
        check_throttle_classes(info, cls, throttle_classes)

        return super().connection_resolver(
            resolver,
            connection,
            default_manager,
            queryset_resolver,
            max_limit,
            enforce_first_or_last,
            root,
            info,
            **args
        )

    def get_resolver(self, parent_resolver):
        return partial(
            self.connection_resolver,
            parent_resolver,
            self.connection_type,
            self.get_manager(),
            self.get_queryset_resolver(),
            self.max_limit,
            self.enforce_first_or_last,
            self.permission_classes,
            self.throttle_classes,
        )


class SpriklFilterConnectionField(DjangoFilterConnectionField):
    def __init__(
        self,
        type,
        fields=None,
        order_by=None,
        extra_filter_meta=None,
        filterset_class=None,
        *args,
        **kwargs
    ):
        self.permission_classes = kwargs.pop("permission_classes", None)
        self.throttle_classes = kwargs.pop("throttle_classes", None)

        super().__init__(
            type, fields, order_by, extra_filter_meta, filterset_class, *args, **kwargs
        )

    @classmethod
    def resolve_connection(cls, connection, args, iterable):
        connection = super().resolve_connection(connection, args, iterable)

        connection.total_count = connection.length
        return connection

    @classmethod
    def connection_resolver(
        cls,
        resolver,
        connection,
        default_manager,
        queryset_resolver,
        max_limit,
        enforce_first_or_last,
        permission_classes,
        throttle_classes,
        root,
        info,
        **args
    ):
        check_permission_classes(info, cls, permission_classes)
        check_throttle_classes(info, cls, throttle_classes)

        return super().connection_resolver(
            resolver,
            connection,
            default_manager,
            queryset_resolver,
            max_limit,
            enforce_first_or_last,
            root,
            info,
            **args
        )

    def get_resolver(self, parent_resolver):
        return partial(
            self.connection_resolver,
            parent_resolver,
            self.connection_type,
            self.get_manager(),
            self.get_queryset_resolver(),
            self.max_limit,
            self.enforce_first_or_last,
            self.permission_classes,
            self.throttle_classes,
        )


class SpriklField(graphene.Field):
    def __init__(self, *args, **kwargs):
        self.permission_classes = kwargs.pop("permission_classes", None)
        self.throttle_classes = kwargs.pop("throttle_classes", None)
        super(SpriklField, self).__init__(*args, **kwargs)

    @classmethod
    def field_resolver(
        cls,
        resolver,
        root,
        info,
        permission_classes=None,
        throttle_classes=None,
        *args,
        **kwargs
    ):
        check_permission_classes(info, cls, permission_classes)
        check_throttle_classes(info, cls, throttle_classes)

        return resolver(root, info, *args, **kwargs)

    def get_resolver(self, parent_resolver):
        return partial(
            self.field_resolver,
            self.resolver or parent_resolver,
            permission_classes=self.permission_classes,
            throttle_classes=self.throttle_classes,
        )


class SpriklDjangoListField(DjangoListField):
    def __init__(self, _type, *args, **kwargs):
        super(DjangoListField, self).__init__(List(NonNull(_type)), *args, **kwargs)


class SpriklListField(Field):
    def __init__(self, _type, *args, **kwargs):
        self.permission_classes = kwargs.pop("permission_classes", None)
        self.throttle_classes = kwargs.pop("throttle_classes", None)

        if isinstance(_type, NonNull):
            _type = _type.of_type

        super(SpriklListField, self).__init__(List(_type), *args, **kwargs)

    @classmethod
    def list_resolver(
        cls,
        resolver,
        root,
        info,
        permission_classes=None,
        throttle_classes=None,
        *args,
        **kwargs
    ):
        check_permission_classes(info, cls, permission_classes)
        check_throttle_classes(info, cls, throttle_classes)

        return resolver(root, info, *args, **kwargs)

    def get_resolver(self, parent_resolver):
        return partial(
            self.list_resolver,
            self.resolver or parent_resolver,
            permission_classes=self.permission_classes,
            throttle_classes=self.throttle_classes,
        )
