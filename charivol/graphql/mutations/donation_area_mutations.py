import graphene
from graphql import GraphQLError
from graphene_file_upload.scalars import Upload
from django.contrib.auth import get_user_model
from charivol.models import DonationArea
from charivol.graphql.types import DonationAreaType

class CreateDonationArea(graphene.Mutation):
    donation_area = graphene.Field(DonationAreaType)
    message = graphene.String()

    class Arguments:
        area_name = graphene.String(required=True)
        area_province = graphene.String(required=True)
        area_city = graphene.String(required=True)
        area_address = graphene.String(required=True)
    
    def mutate(
        self, info, area_name, area_province, area_city, area_address=None
    ):
        donation_area = DonationArea.objects.create(
            area_name=area_name,
            area_province=area_province,
            area_city=area_city,
            area_address=area_address,
        )
        return CreateDonationArea(donation_area=donation_area, message="Donation Area created successfully")

# class UpdatePartialDonationArea(graphene.Mutation):
#     donation_area = graphene.Field(DonationAreaType)
#     message = graphene.String()

#     class Arguments:
#         id = graphene.UUID(required=True)
#         area_postal_code = graphene.String(required=False)
#         description = graphene.String(required=False)
#         is_active = graphene.Boolean(required=False)
    
#     def mutate(self, info, id, area_postal_code=None, description=None, is_active=None):
#         try:
#             donation_area = DonationArea.objects.get(id=id)
#         except DonationArea.DoesNotExist:
#             raise GraphQLError(f"Donation Area with id {id} does not exist")
        
#         # Update fields if provided
#         data = {
#             'area_postal_code': area_postal_code,
#             'description': description,
#             'is_active': is_active
#         }

#         for field, value in data.items():
#             if value is not None:
#                 setattr(donation_area, field, value)
        
#         donation_area.save()
#         return UpdatePartialDonationArea(
#             donation_area=donation_area,
#             message="DonationArea updated successfully"
#         )

class UpdateDonationArea(graphene.Mutation):
    donation_area = graphene.Field(DonationAreaType)
    message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)
        area_name = graphene.String(required=True)
        area_province = graphene.String(required=True)
        area_city = graphene.String(required=True)
        area_postal_code = graphene.String(required=False)
        area_address = graphene.String(required=True)
        # Optional fields
        description = graphene.String(required=False)
        
    def mutate(
        self, info, id, area_name, area_province, area_city, area_postal_code=None,
        area_address=None, description=None
    ):
        try:
            donation_area = DonationArea.objects.get(id=id)
        except DonationArea.DoesNotExist:
            raise GraphQLError(f"Donation Area with id {id} does not exist")
        
        # Buat dictionary field yang mau diupdate
        data = {
            'area_name': area_name,
            'area_province': area_province,
            'area_city': area_city,
            'area_postal_code': area_postal_code,
            'area_address': area_address,
            'description': description,
        }
        
        # Update fields if provided
        for field, value in data.items():
            if value is not None:
                setattr(donation_area, field, value)
        
        donation_area.save()
        return UpdateDonationArea(
            donation_area=donation_area,
            message="Donation Area updated successfully"
        )

class DeleteDonationArea(graphene.Mutation):
    message = graphene.String()
    success = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        try:
            donation_area = DonationArea.objects.get(id=id)
            donation_area.delete()
            return DeleteDonationArea(message="Donation Area deleted successfully", success=True)
        except DonationArea.DoesNotExist:
            raise GraphQLError(f"Donation Area with id {id} does not exist", success=False)

class DonationAreaMutations(graphene.ObjectType):
    create_donation_area = CreateDonationArea.Field()
    # update_partial_donation_area = UpdatePartialDonationArea.Field()
    update_donation_area = UpdateDonationArea.Field()
    delete_donation_area = DeleteDonationArea.Field()