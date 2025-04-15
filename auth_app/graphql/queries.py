import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from .types import UserType

class Query(graphene.ObjectType):
    current_user = graphene.Field(UserType)

    @login_required
    def resolve_current_user(self, info):
        user = info.context.user
        
        if user is None or not user.is_authenticated:
            raise GraphQLError("User is not authenticated")
        return user