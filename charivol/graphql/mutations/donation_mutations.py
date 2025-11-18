import graphene
from graphql import GraphQLError
from django.contrib.auth import get_user_model
from charivol.models import Donation, Donor, Volunteer, DonationArea
from charivol.graphql.types import DonationType

class CreateDonation(graphene.Mutation):
    donation = graphene.Field(DonationType)
    message = graphene.String()

    class Arguments:
        donatur_id = graphene.Int(required=True)
        donation_name = graphene.String(required=True)
        description = graphene.String(required=True)
        image_url = graphene.String(required=False)
        volunteer_id = graphene.Int(required=False)
        volunteer_remarks = graphene.String(required=False)

    def mutate(
        self, info,
        donatur_id, donation_name, description,
        image_url=None, volunteer_id=None, volunteer_remarks=None
    ):
        # Validasi donor
        try:
            donor = Donor.objects.get(id=donatur_id,)
        except Donor.DoesNotExist:
            raise GraphQLError(f"Donor with id '{donatur_id,}' does not exist.")

        # Validasi volunteer (jika dikirim)
        volunteer = None
        if volunteer_id:
            try:
                volunteer = Volunteer.objects.get(id=volunteer_id)
            except Volunteer.DoesNotExist:
                raise GraphQLError(f"Volunteer with id '{volunteer_id}' does not exist.")

        # Buat data donasi
        donation = Donation.objects.create(
            donatur=donor,
            donation_name=donation_name,
            description=description,
            image_url=image_url,
            volunteer=volunteer,
            volunteer_remarks=volunteer_remarks
        )

        return CreateDonation(
            donation=donation,
            message="Donation created successfully"
        )

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

class UpdateDonation(graphene.Mutation):
    donation = graphene.Field(DonationType)
    message = graphene.String()

    class Arguments:
        donation_id = graphene.Int(required=True)  # Anda lupa di Arguments → saya tambahkan
        donation_name = graphene.String(required=True)
        image_url = graphene.String(required=False)  # Tidak pakai Upload lagi
        description = graphene.String(required=True)
        volunteer_id = graphene.Int(required=False)  # kembalikan ke Int karena id volunteer biasanya integer
        donation_status = graphene.String(required=False)  # pakai String biasa
        volunteer_remarks = graphene.String(required=False)

    def mutate(
        self, info,
        donation_id, donation_name, image_url, description,
        volunteer_id=None, donation_status=None, volunteer_remarks=None
    ):
        # Validasi donation
        try:
            donation = Donation.objects.get(id=donation_id)
        except Donation.DoesNotExist:
            raise GraphQLError(f"Donation with id {donation_id} does not exist")
        

        # Validasi volunteer (jika dikirim)
        volunteer = None
        if volunteer_id:
            try:
                volunteer = Volunteer.objects.get(id=volunteer_id)
            except Volunteer.DoesNotExist:
                raise GraphQLError(f"Volunteer with id '{volunteer_id}' does not exist.")

        # Validasi donation
        try:
            donation = Donation.objects.get(id=donation_id)
        except Donation.DoesNotExist:
            raise GraphQLError(f"Donation with id {donation_id} does not exist")

        # Update donation fields
        donation.donation_name = donation_name
        if image_url is not None:
            donation.image_url = image_url
        donation.description = description
        if donation_status is not None:
            donation.donation_status = donation_status
        donation.volunteer = volunteer
        donation.volunteer_remarks = volunteer_remarks
        # Simpan perubahan
        donation.save()
        return UpdateDonation(
            message="Donation updated successfully",
            donation=donation,
        )

class DeleteDonation(graphene.Mutation):
    message = graphene.String()
    success = graphene.Boolean()

    class Arguments:
        donation_id = graphene.Int(required=True)

    def mutate(self, info, donation_id):
        try:
            donation = Donation.objects.get(id=donation_id)
            donation.delete()
            return DeleteDonation(message="Donation deleted successfully", success=True)
        except Donation.DoesNotExist:
            return DeleteDonation(message=f"Donation with id {donation_id} not found.", success=False)

class DonationMutations(graphene.ObjectType):
    create_donation = CreateDonation.Field()
    # update_partial_donation = UpdatePartialDonation.Field()
    update_donation = UpdateDonation.Field()
    delete_donation = DeleteDonation.Field()