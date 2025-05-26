import graphene
from auth_app.models import User as CustomUser
from .types import UserType
from django.contrib.auth import authenticate
from graphql import GraphQLError
from graphql_jwt.shortcuts import get_token, create_refresh_token
from graphql_jwt.refresh_token.models import RefreshToken

class RegisterUser(graphene.Mutation):
    user = graphene.Field(UserType)
    message = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        confirm_password = graphene.String(required=True)

    def mutate(self, info, email, first_name, last_name, username, password, confirm_password):
        if CustomUser.objects.filter(email=email).exists():
            raise GraphQLError("Email already exists")
        if CustomUser.objects.filter(username=username).exists():
            raise GraphQLError("Username already exists")
        if password != confirm_password:
            raise GraphQLError("Passwords do not match")
        if len(password) < 8:
            raise GraphQLError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in password):
            raise GraphQLError("Password must contain at least one digit")
        if not any(char.isalpha() for char in password):
            raise GraphQLError("Password must contain at least one letter")
        if not any(char.isupper() for char in password):
            raise GraphQLError("Password must contain at least one uppercase letter")

        user = CustomUser.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password
        )
        
        return RegisterUser(
            user=user,
            message="User created successfully. You can login now."
        )

class LoginUser(graphene.Mutation):
    user = graphene.Field(UserType)
    access = graphene.String()
    refresh = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        user = authenticate(email=email, password=password)
        if user is None:
            raise GraphQLError("Invalid credentials")
        
        access = get_token(user)
        refresh = create_refresh_token(user)
        return LoginUser(user=user, access=access, refresh=refresh.token)

class LogoutUser(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        refresh_token = graphene.String(required=True)

    def mutate(self, info, refresh_token):
        try:
            token = RefreshToken.objects.get(token=refresh_token)
            token.revoke()
            return LogoutUser(success=True)
        except RefreshToken.DoesNotExist:
            raise GraphQLError("Invalid refresh token")

class AuthMutations(graphene.ObjectType):
    register_user = RegisterUser.Field()
    login_user = LoginUser.Field()
    logout_user = LogoutUser.Field()