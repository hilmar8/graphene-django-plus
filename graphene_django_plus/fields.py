from functools import partial

import graphene
from graphene import Field, List, NonNull, ConnectionField, Connection
from graphene.types.utils import get_type
from graphene_django import DjangoConnectionField
from graphene_django.fields import DjangoListField
from graphene_django.filter import DjangoFilterConnectionField

from .permissions import check_permission_classes, check_throttle_classes


class PlusConnectionField(DjangoConnectionField):
    def __init__(self, *args, **kwargs):
        self.permission_classes = kwargs.pop("permission_classes", None)
        self.throttle_classes = kwargs.pop("throttle_classes", None)

        super().__init__(*args, **kwargs)

    @property
    def type(self):
        from .types import DjangoObjectType

        _type = super(ConnectionField, self).type
        non_null = False
        if isinstance(_type, NonNull):
            _type = _type.of_type
            non_null = True

        if issubclass(_type, Connection):
            connection_type = _type
        else:
            assert issubclass(
                _type, DjangoObjectType
            ), "PlusConnectionField only accepts DjangoObjectType and Connection types"
            assert _type._meta.connection, "The type {} doesn't have a connection".format(
                _type.__name__
            )
            connection_type = _type._meta.connection
        if non_null:
            return NonNull(connection_type)
        return connection_type

    @property
    def model(self):
        return getattr(self.node_type._meta, 'model', None)

    def get_manager(self):
        if self.model is None:
            return None
        elif self.on:
            return getattr(self.model, self.on)
        else:
            return self.model._default_manager

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


class PlusFilterConnectionField(DjangoFilterConnectionField):
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


class PlusField(graphene.Field):
    def __init__(self, *args, **kwargs):
        self.permission_classes = kwargs.pop("permission_classes", None)
        self.throttle_classes = kwargs.pop("throttle_classes", None)
        super(PlusField, self).__init__(*args, **kwargs)

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


class DjangoPlusListField(DjangoListField):
    def __init__(self, _type, *args, **kwargs):
        self.permission_classes = kwargs.pop("permission_classes", None)
        self.throttle_classes = kwargs.pop("throttle_classes", None)

        super(DjangoListField, self).__init__(List(NonNull(_type)), *args, **kwargs)

    @classmethod
    def list_resolver(
        cls,
        django_object_type,
        resolver,
        root,
        info,
        permission_classes=None,
        throttle_classes=None,
        **args
    ):
        check_permission_classes(info, cls, permission_classes)
        check_throttle_classes(info, cls, throttle_classes)

        return super().list_resolver(django_object_type, resolver, root, info, **args)

    def get_resolver(self, parent_resolver):
        _type = self.type
        if isinstance(_type, NonNull):
            _type = _type.of_type
        django_object_type = _type.of_type.of_type

        return partial(
            self.list_resolver,
            django_object_type,
            parent_resolver,
            permission_classes=self.permission_classes,
            throttle_classes=self.throttle_classes,
        )


class PlusListField(Field):
    def __init__(self, _type, *args, **kwargs):
        self.permission_classes = kwargs.pop("permission_classes", None)
        self.throttle_classes = kwargs.pop("throttle_classes", None)

        if isinstance(_type, NonNull):
            _type = _type.of_type

        super(PlusListField, self).__init__(List(_type), *args, **kwargs)

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
