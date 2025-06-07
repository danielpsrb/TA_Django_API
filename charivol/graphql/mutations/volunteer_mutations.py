import graphene
from graphql import GraphQLError
from graphene_file_upload.scalars import Upload
from django.contrib.auth import get_user_model
from charivol.models import Volunteer
from charivol.utils import upload_image
from charivol.graphql.types import VolunteerType

class CreateVolunteer(graphene.Mutation):
    volunteer = graphene.Field(VolunteerType)
    message = graphene.String()

    class Arguments:
        user_id = graphene.UUID(required=True)
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
class UpdateFullVolunteerProfile(graphene.Mutation):
    volunteer = graphene.Field(VolunteerType)
    message = graphene.String()

    class Arguments:
        id = graphene.UUID(required=True)
        contact = graphene.String(required=True)
        address = graphene.String(required=True)
        gender = graphene.String(required=True)
        province = graphene.String(required=True)
        city = graphene.String(required=True)
        about_me = graphene.String(required=True)
        user_photo = Upload(required=False)
    
    def mutate(
        self, info, id, contact, address, gender, province, city, about_me, user_photo=None
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
        volunteer.about_me = about_me
        
        if user_photo:
            success, result = upload_image(user_photo, folder='volunteer')
            if not success:
                raise GraphQLError(f"Failed to upload photo: {result}")
            volunteer.photo_url = result
        
        volunteer.save()
        return UpdateFullVolunteerProfile(
            volunteer=volunteer, 
            message="Volunteer profile updated successfully"
        )

class DeleteVolunteer(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        id = graphene.UUID(required=True)
    
    def mutate(self, info, id):
        try:
            volunteer = Volunteer.objects.get(id=id)
            volunteer.delete()
            return DeleteVolunteer(message="Volunteer deleted successfully")
        except Volunteer.DoesNotExist:
            raise GraphQLError(f"Volunteer with id {id} does not exist")

class VolunteerMutations(graphene.ObjectType):
    create_volunteer = CreateVolunteer.Field()
    # update_partial_volunteer_profile = UpdatePartialVolunteerProfile.Field()
    update_full_volunteer_profile = UpdateFullVolunteerProfile.Field()
    delete_volunteer = DeleteVolunteer.Field()