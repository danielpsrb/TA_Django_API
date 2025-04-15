from auth_app.models import CustomUser
from graphene_django import DjangoObjectType

class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "first_name", "last_name", "username", "date_joined")