import graphene
import graphql_jwt

from auth_app.graphql.mutations import AuthMutations
from auth_app.graphql.queries import Query as AuthQueries

class Query(AuthQueries, graphene.ObjectType):
    pass

class Mutation(AuthMutations, graphene.ObjectType):
    # JWT Auth mutations
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()

# Main Schema
schema = graphene.Schema(query=Query, mutation=Mutation)