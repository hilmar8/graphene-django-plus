from collections import OrderedDict

import graphene
from graphene.types.objecttype import ObjectTypeOptions
from rest_framework import routers

from .app import schema as app_schema
from .app.types import BookType

router = routers.SimpleRouter()
#
#
# class TestRouter:
#     def __init__(self):
#         self.registry = []
#
#     def register(self, field_name, field_type):
#         self.registry.append((field_name, field_type))
#
#     def bloobloo(self):
#         this = self
#
#         class Blabla(graphene.ObjectType):
#             @classmethod
#             def __init_subclass_with_meta__(
#                 cls,
#                 interfaces=(),
#                 possible_types=(),
#                 default_resolver=None,
#                 _meta=None,
#                 **options
#             ):
#                 _meta = ObjectTypeOptions(cls)
#
#                 _meta.fields = OrderedDict()
#
#                 for lele in this.registry:
#                     _meta.fields[lele[0]] = lele[1]
#
#                 super().__init_subclass_with_meta__(
#                     interfaces, possible_types, default_resolver, _meta, **options
#                 )
#
#         return Blabla
#
#
# test_router = TestRouter()
#
# test_router.register("book", SpriklNode.Field(BookType))


class Query(app_schema.query, graphene.ObjectType):
    pass


# class Mutation(graphene.ObjectType):
#     pass


schema = graphene.Schema(query=Query)  # , mutation=Mutation)
