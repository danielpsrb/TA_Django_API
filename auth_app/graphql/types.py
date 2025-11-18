import graphene
from auth_app.models import User as CustomUser
from graphene_django import DjangoObjectType

class UserType(DjangoObjectType):
    
    class Meta:
        model = CustomUser
        fields = ("id", "email", "first_name", "last_name", "username")
    
    def resolve_id(self, info):
        return str(self.id)
    
    def resolve_email(self, info):
        return self.email if self.email else None
    
    def resolve_first_name(self, info):
        return self.first_name if self.first_name else None
    
    def resolve_last_name(self, info):
        return self.last_name if self.last_name else None
    
    def resolve_username(self, info):
        return self.username if self.username else None