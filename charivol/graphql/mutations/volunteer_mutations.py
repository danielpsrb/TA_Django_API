import graphene
from graphql import GraphQLError
from django.contrib.auth import get_user_model
from charivol.models import Volunteer
from charivol.graphql.types import VolunteerType

class CreateVolunteer(graphene.Mutation):
    volunteer = graphene.Field(VolunteerType)
    message = graphene.String()

    class Arguments:
        user_id = graphene.Int(required=True)
        contact = graphene.String(required=True)
        address = graphene.String(required=True)
    
    def mutate(self, info, user_id, contact, address):
        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise GraphQLError(f"User with id {user_id} does not exist")

        volunteer = Volunteer.objects.create(user=user, contact=contact, address=address)
        return CreateVolunteer(volunteer=volunteer, message="Volunteer created successfully")

# class UpdatePartialVolunteerProfile(graphene.Mutation):
#     volunteer = graphene.Field(VolunteerType)
#     message = graphene.String()

#     class Arguments:
#         id = graphene.UUID(required=True)
#         gender = graphene.String(required=False)
#         province = graphene.String(required=False)
#         city = graphene.String(required=False)
#         about_me = graphene.String(required=False)
#         user_photo = Upload(required=False)
    
#     def mutate(self, info, id, gender=None, province=None, city=None, about_me=None, user_photo=None):
#         try:
#             volunteer = Volunteer.objects.get(id=id)
#         except Volunteer.DoesNotExist:
#             raise GraphQLError(f"Volunteer with id {id} does not exist")
        
#         # Prepare mapping between argument names and model field names
#         arg_to_field = {
#             'gender': gender,
#             'province': province,
#             'city': city,
#             'about_me': about_me
#         }
        
#         # Dynamic update fields that are not None
#         for arg, value in arg_to_field.items():
#             if value is not None:
#                 setattr(volunteer, arg, value)
        
#         # Handle user_photo upload separately
#         if user_photo:
#             success, result = upload_image(user_photo, folder='volunteer')
#             if not success:
#                 raise GraphQLError(f"Failed to upload photo: {result}")
#             volunteer.photo_url = result
        
#         volunteer.save()
#         return UpdatePartialVolunteerProfile(
#             volunteer=volunteer,
#             message="Volunteer profile updated successfully"
#         )

# Update All field of Volunteer Profile
class UpdateVolunteerProfile(graphene.Mutation):
    volunteer = graphene.Field(VolunteerType)
    message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)
        contact = graphene.String(required=True)
        address = graphene.String(required=True)
        gender = graphene.String(required=True)
        province = graphene.String(required=True)
        city = graphene.String(required=True)
        photo_url = graphene.String(required=False)

    
    def mutate(
        self, info, id, contact, address, gender, province, city, photo_url=None
    ):
        try:
            volunteer = Volunteer.objects.get(id=id)
        except Volunteer.DoesNotExist:
            raise GraphQLError(f"Volunteer with id {id} does not exist")
        
        # Update fields
        volunteer.contact = contact
        volunteer.address = address
        volunteer.gender = gender
        volunteer.province = province
        volunteer.city = city
        
        if photo_url:
            volunteer.photo_url = photo_url
        
        volunteer.save()
        return UpdateVolunteerProfile(
            volunteer=volunteer, 
            message="Volunteer profile updated successfully"
        )

class DeleteVolunteer(graphene.Mutation):
    message = graphene.String()
    success = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)
    
    def mutate(self, info, id):
        try:
            volunteer = Volunteer.objects.get(id=id)
            volunteer.delete()
            return DeleteVolunteer(message="Volunteer deleted successfully", success=True)
        except Volunteer.DoesNotExist:
            raise GraphQLError(f"Volunteer with id {id} does not exist" , success=False)

class VolunteerMutations(graphene.ObjectType):
    create_volunteer = CreateVolunteer.Field()
    # update_partial_volunteer_profile = UpdatePartialVolunteerProfile.Field()
    update_volunteer_profile = UpdateVolunteerProfile.Field()
    delete_volunteer = DeleteVolunteer.Field()