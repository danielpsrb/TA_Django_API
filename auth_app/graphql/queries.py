import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from .types import UserType
from auth_app.models import User

class Query(graphene.ObjectType):
    current_user = graphene.Field(UserType)
    user = graphene.Field(UserType, id=graphene.Int(required=True))

    @login_required
    def resolve_current_user(self, info):
        user = info.context.user
        
        if user is None or not user.is_authenticated:
            raise GraphQLError("User is not authenticated")
        return user
    
    def resolve_user(self, info, id):
        user = User.objects.filter(id=id).first()
        
        if user is None:
            raise GraphQLError("User not found")
        return user