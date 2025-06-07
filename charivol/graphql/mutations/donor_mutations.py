import graphene
from graphql import GraphQLError
from graphene_file_upload.scalars import Upload
from django.contrib.auth import get_user_model
from charivol.models import Donor
from charivol.utils import upload_image
from charivol.graphql.types import DonorType

class CreateDonor(graphene.Mutation):
    donor = graphene.Field(DonorType)
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

        donor = Donor.objects.create(user=user, contact=contact, address=address)
        return CreateDonor(donor=donor, message="Donor created successfully")

# class UpdatePartialDonorProfile(graphene.Mutation):
#     donor = graphene.Field(DonorType)
#     message = graphene.String()

#     class Arguments:
#         id = graphene.UUID(required=True)
#         gender = graphene.String(required=False)
#         province = graphene.String(required=False)
#         city = graphene.String(required=False)
#         occupation = graphene.String(required=False)
#         photo = Upload(required=False)
    
#     def mutate(self, info, id, gender=None, province=None, city=None, occupation=None, photo=None):
#         try:
#             donor = Donor.objects.get(id=id)
#         except Donor.DoesNotExist:
#             raise GraphQLError(f"Donor with id {id} does not exist")
        
#         if photo:
#             success, result = upload_image(photo, folder='donatur')
#             if not success:
#                 raise GraphQLError(f"Gagal upload foto: {result}")
#             donor.photo_url = result
        
#         donor.gender = gender if gender is not None else donor.gender
#         donor.province = province if province is not None else donor.province
#         donor.city = city if city is not None else donor.city
#         donor.occupation = occupation if occupation is not None else donor.occupation
        
#         donor.save()
#         return UpdatePartialDonorProfile(donor=donor, message="Donor profile updated successfully")

# Update All field of Donor Profile
class UpdateFullDonorProfile(graphene.Mutation):
    donor = graphene.Field(DonorType)
    message = graphene.String()

    class Arguments:
        id = graphene.UUID(required=True)
        contact = graphene.String(required=True)
        address = graphene.String(required=True)
        gender = graphene.String(required=True)
        province = graphene.String(required=True)
        city = graphene.String(required=True)
        occupation = graphene.String(required=True)
        photo = Upload(required=False)  # optional update photo
    
    def mutate(
        self, info, id, contact, address, gender, province, city, occupation, photo=None
    ):
        try:
            donor = Donor.objects.get(id=id)
        except Donor.DoesNotExist:
            raise GraphQLError(f"Donor with id {id} does not exist")
        
        # Update fields
        donor.contact = contact
        donor.address = address
        donor.gender = gender
        donor.province = province
        donor.city = city
        donor.occupation = occupation
        
        if photo:
            success, result = upload_image(photo, folder='donatur')
            if not success:
                raise GraphQLError(f"Failed to upload photo: {result}")
            donor.photo_url = result
        donor.save()
        return UpdateFullDonorProfile(donor=donor, message="Donor profile updated successfully")

class DeleteDonor(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        id = graphene.UUID(required=True)
    
    def mutate(self, info, id):
        try:
            donor = Donor.objects.get(id=id)
            donor.delete()
            return DeleteDonor(message="Donor deleted successfully")
        except Donor.DoesNotExist:
            raise GraphQLError(f"Donor with id {id} does not exist")
        except Exception as e:
            raise GraphQLError(f"An error occurred while deleting the donor: {str(e)}")

class DonorMutations(graphene.ObjectType):
    create_donor = CreateDonor.Field()
    # update_partial_donor_profile = UpdatePartialDonorProfile.Field()
    update_full_donor_profile = UpdateFullDonorProfile.Field()
    delete_donor = DeleteDonor.Field()