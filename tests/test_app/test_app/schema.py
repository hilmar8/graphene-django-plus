import graphene

from .app import schema as app_schema


class Query(app_schema.Query, graphene.ObjectType):
    pass


class Mutation(app_schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
