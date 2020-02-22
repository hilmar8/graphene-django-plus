import graphene

from .app import schema


class Query(schema.Query, graphene.ObjectType):
    pass


# class Mutation(graphene.ObjectType):
#     pass


schema = graphene.Schema(query=Query)#, mutation=Mutation)
