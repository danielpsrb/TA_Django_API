import graphene
from graphql import GraphQLError
from graphene_file_upload.scalars import Upload
from django.contrib.auth import get_user_model
from charivol.enums import DonationStatusOptions, DonationTypeOptions
from charivol.models import Donation, Donor, Volunteer, DonationArea, DonationTypeItems, DonationStatus
from charivol.utils import upload_image
from charivol.graphql.types import DonationType

class CreateDonation(graphene.Mutation):
    donation = graphene.Field(DonationType)
    message = graphene.String()

    class Arguments:
        donation_name = DonationTypeOptions(required=True)  # Enum untuk jenis donasi
        image = Upload(required=True)  # Kita pakai Upload untuk menerima file gambar
        description = graphene.String(required=True)
        donor_id = graphene.String(required=True)  # CUID → pakai String
        volunteer_id = graphene.String(required=True)  # CUID → pakai String
        donation_area_id = graphene.Int(required=True)  # Auto Increment → pakai Int

    def mutate(
        self, info,
        donation_name, image, description, donor_id, volunteer_id, donation_area_id
    ):
        # Validasi donation_name
        valid_donation_names = [choice[0] for choice in DonationTypeItems.choices]
        if donation_name not in valid_donation_names:
            raise GraphQLError(f"Invalid donation name: {donation_name}. Valid options are: {', '.join(valid_donation_names)}")
            
        # Validasi donor
        try:
            donor = Donor.objects.get(id=donor_id)
        except Donor.DoesNotExist:
            raise GraphQLError(f"Donor with id {donor_id} does not exist")

        # Validasi volunteer
        try:
            volunteer = Volunteer.objects.get(id=volunteer_id)
        except Volunteer.DoesNotExist:
            raise GraphQLError(f"Volunteer with id {volunteer_id} does not exist")

        # Validasi donation_area
        try:
            donation_area = DonationArea.objects.get(id=donation_area_id)
        except DonationArea.DoesNotExist:
            raise GraphQLError(f"Donation Area with id {donation_area_id} does not exist")

        # Upload image ke storage (Supabase, dll.)
        success, result = upload_image(image, folder='donation')
        if not success:
            raise GraphQLError(f"Gagal upload image: {result}")

        # Create Donation
        donation = Donation.objects.create(
            donor=donor,
            donation_name=donation_name,
            image_url=result,  # URL dari image upload
            description=description,
            volunteer=volunteer,
            donation_area=donation_area
            # donation_date otomatis diisi
        )

        return CreateDonation(donation=donation, message="Donation created successfully")


# class UpdatePartialDonation(graphene.Mutation):
#     donation = graphene.Field(DonationType)
#     message = graphene.String()

#     class Arguments:
#         donation_id = graphene.String(required=True)  # CUID → pakai String
#         image = Upload(required=False)  # Kita pakai Upload untuk menerima file gambar
#         collection_location = graphene.String(required=False)
#         donation_status = DonationStatusOptions(required=False)
#         volunteer_remarks = graphene.String(required=False)
    
#     def mutate(
#         self, info, donation_id, image=None, collection_location=None, donation_status=None, volunteer_remarks=None
#     ):
#         # Validasi donation
#         try:
#             donation = Donation.objects.get(id=donation_id)
#         except Donation.DoesNotExist:
#             raise GraphQLError(f"Donation with id {donation_id} does not exist")
        
#         # Validasi donation_status jika dikirim
#         if donation_status is not None:
#             valid_statuses = [choice[0] for choice in DonationStatus.choices]
#             if donation_status not in valid_statuses:
#                 raise GraphQLError(f"Invalid donation status: {donation_status}. Valid options are: {', '.join(valid_statuses)}")

#         # Update fields if provided
#         if image:
#             success, result = upload_image(image, folder='donation')
#             if not success:
#                 raise GraphQLError(f"Gagal upload image: {result}")
#             donation.image_url = result
        
#         if collection_location:
#             donation.collection_location = collection_location
        
#         if donation_status:
#             donation.donation_status = donation_status
        
#         if volunteer_remarks:
#             donation.volunteer_remarks = volunteer_remarks

#         # Save changes
#         donation.save()

#         return UpdatePartialDonation(donation=donation, message="Donation updated successfully")

class UpdateFullDonation(graphene.Mutation):
    donation = graphene.Field(DonationType)
    message = graphene.String()

    class Arguments:
        donation_id = graphene.String(required=True)  # CUID → pakai String
        donation_name = DonationTypeOptions(required=True)  # Enum untuk jenis donasi
        image = Upload(required=True)  # Kita pakai Upload untuk menerima file gambar
        description = graphene.String(required=True)
        volunteer_id = graphene.String(required=False)  # CUID → pakai String
        donation_area_id = graphene.Int(required=False)  # Auto Increment → pakai Int
        donation_status = DonationStatusOptions(required=False)
        volunteer_remarks = graphene.String(required=False)

    def mutate(
        self, info,
        donation_id, donation_name, image, description, donation_status, volunteer_id, donation_area_id, volunteer_remarks=None
    ):
        # Validasi donation_name
        valid_donation_names = [choice[0] for choice in DonationTypeItems.choices]
        if donation_name not in valid_donation_names:
            raise GraphQLError(f"Invalid donation name: {donation_name}. Valid options are: {', '.join(valid_donation_names)}")


        # Validasi volunteer
        try:
            volunteer = Volunteer.objects.get(id=volunteer_id)
        except Volunteer.DoesNotExist:
            raise GraphQLError(f"Volunteer with id {volunteer_id} does not exist")

        # Validasi donation_area
        try:
            donation_area = DonationArea.objects.get(id=donation_area_id)
        except DonationArea.DoesNotExist:
            raise GraphQLError(f"Donation Area with id {donation_area_id} does not exist")

        # Validasi donation
        try:
            donation = Donation.objects.get(id=donation_id)
        except Donation.DoesNotExist:
            raise GraphQLError(f"Donation with id {donation_id} does not exist")

        # Upload image ke storage (Supabase, dll.)
        success, result = upload_image(image, folder='donations')
        if not success:
            raise GraphQLError(f"Gagal upload image: {result}")

        # Update Donation fields
        donation.donation_name = donation_name
        donation.image_url = result
        donation.description = description
        donation.volunteer = volunteer
        donation.donation_area = donation_area
        
        if donation_status is not None:
            valid_statuses = [choice[0] for choice in DonationStatus.choices]
            if donation_status not in valid_statuses:
                raise GraphQLError(f"Invalid donation status: {donation_status}. Valid options are: {', '.join(valid_statuses)}")
            donation.donation_status = donation_status
        
        if volunteer_remarks is not None:
            donation.volunteer_remarks = volunteer_remarks
        # Save changes
        donation.save()
        return UpdateFullDonation(donation=donation, message="Donation updated successfully")

class DeleteDonation(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        donation_id = graphene.String(required=True)  # CUID → pakai String

    def mutate(self, info, donation_id):
        # Validasi donation
        try:
            donation = Donation.objects.get(id=donation_id)
        except Donation.DoesNotExist:
            raise GraphQLError(f"Donation with id {donation_id} does not exist")

        # Hapus Donation
        donation.delete()
        return DeleteDonation(message="Donation deleted successfully")

class Mutation(graphene.ObjectType):
    create_donation = CreateDonation.Field()
    # update_partial_donation = UpdatePartialDonation.Field()
    update_full_donation = UpdateFullDonation.Field()
    delete_donation = DeleteDonation.Field()