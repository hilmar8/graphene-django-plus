from textwrap import dedent

import graphene
import graphene_django.types
from graphene.types.unmountedtype import UnmountedType
from graphene_django.utils import camelize
from graphene_django.settings import graphene_settings

from .registry import get_global_registry
from .relay.connection import DjangoConnection


class DjangoObjectTypeOptions(graphene_django.types.DjangoObjectTypeOptions):
    id_field = None  # type: str


class DjangoObjectType(graphene_django.types.DjangoObjectType):
    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        model=None,
        id_field=None,
        registry=None,
        skip_registry=False,
        only_fields=(),
        fields=(),
        exclude_fields=(),
        exclude=(),
        filter_fields=None,
        filterset_class=None,
        connection=None,
        connection_class=None,
        use_connection=None,
        interfaces=(),
        convert_choices_to_enum=True,
        _meta=None,
        **options
    ):
        if not id_field:
            id_field = "pk"

        if not _meta:
            _meta = DjangoObjectTypeOptions(cls)

        if not connection_class:
            connection_class = DjangoConnection

        if not registry:
            registry = get_global_registry()

        _meta.id_field = id_field

        return super().__init_subclass_with_meta__(
            model,
            registry,
            skip_registry,
            only_fields,
            fields,
            exclude_fields,
            exclude,
            filter_fields,
            filterset_class,
            connection,
            connection_class,
            use_connection,
            interfaces,
            convert_choices_to_enum,
            _meta,
            **options
        )

    def resolve_id(self, info):
        return getattr(self, info.parent_type.graphene_type._meta.id_field)

    @classmethod
    def get_node(cls, info, id):
        queryset = cls.get_queryset(cls._meta.model.objects, info)
        try:
            return queryset.get(**{cls._meta.id_field: id})
        except cls._meta.model.DoesNotExist:
            return None


# from textwrap import dedent
#
# import graphene
# from graphene.types.unmountedtype import UnmountedType
#
# from graphene_django import types as graphene_django_types
# from graphene_django.settings import graphene_settings
# from graphene_django.utils import camelize
#
# from .relay.connection import DjangoConnection
#
#
# class DjangoObjectTypeOptions(graphene_django_types.DjangoObjectTypeOptions):
#     id_field = None
#
#
# class DjangoObjectType(graphene_django_types.DjangoObjectType):
#     @classmethod
#     def __init_subclass_with_meta__(
#         cls,
#         model=None,
#         id_field=None,
#         registry=None,
#         skip_registry=False,
#         only_fields=(),
#         fields=(),
#         exclude_fields=(),
#         exclude=(),
#         filter_fields=None,
#         filterset_class=None,
#         connection=None,
#         connection_class=None,
#         use_connection=None,
#         interfaces=(),
#         convert_choices_to_enum=True,
#         _meta=None,
#         **options
#     ):
#         if not _meta:
#             _meta = DjangoObjectTypeOptions(cls)
#
#         if use_connection and not connection:
#             # We create the connection automatically
#             if not connection_class:
#                 connection_class = DjangoConnection
#
#             connection = connection_class.create_type(
#                 "{}Connection".format(cls.__name__), node=cls
#             )
#
#         if connection is not None:
#             assert issubclass(connection, DjangoConnection), (
#                 "The connection must be a DjangoConnection. Received {}"
#             ).format(connection.__name__)
#
#         if not id_field:
#             id_field = "pk"
#
#         _meta.id_field = id_field
#
#         return super().__init_subclass_with_meta__(
#             model,
#             registry,
#             skip_registry,
#             only_fields,
#             fields,
#             exclude_fields,
#             exclude,
#             filter_fields,
#             filterset_class,
#             connection,
#             connection_class,
#             use_connection,
#             interfaces,
#             convert_choices_to_enum,
#             _meta,
#             **options
#         )
#
#     def resolve_id(self, info):
#         return getattr(self, info.parent_type.graphene_type._meta.id_field)
#
#     @classmethod
#     def get_node(cls, info, id):
#         # TODO: maybe_queryset
#         queryset = cls.get_queryset(cls._meta.model.objects, info)
#         try:
#             return queryset.get(**{cls._meta.id_field: id})
#         except cls._meta.model.DoesNotExist:
#             return None
#
#
class ErrorType(graphene.ObjectType):
    field = graphene.String(
        description=dedent(
            """Name of a field that caused the error. A value of
        `null` indicates that the error isn't associated with a particular
        field."""
        ),
        required=False,
    )
    messages = graphene.List(
        graphene.NonNull(graphene.String),
        description="The error messages.",
        required=True,
    )
    path = graphene.List(
        graphene.NonNull(graphene.String),
        description="""Path to the name of a field that caused the error.
        A value of `null` indicates that the error isn't associated with a
        particular field.""",
        required=False,
    )

    @classmethod
    def from_errors(cls, errors):
        data = camelize(errors) if graphene_settings.CAMELCASE_ERRORS else errors
        return [cls(field=key, messages=value) for key, value in data.items()]


class DictType(UnmountedType):
    key = graphene.String()
    value = graphene.String()
