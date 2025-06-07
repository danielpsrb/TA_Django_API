import graphene
from charivol.models import Donor, Volunteer, DonationArea, Donation
from .types import DonorType, VolunteerType, DonationAreaType, DonationType
from graphql import GraphQLError

class DonorQuery(graphene.ObjectType):
    donor = graphene.Field(DonorType, id=graphene.UUID(required=True))
    donor_by_user_id = graphene.Field(DonorType, user_id=graphene.UUID(required=True))
    
    def resolve_donor(self, info, id):
        try:
            return Donor.objects.get(id=id)
        except Donor.DoesNotExist:
            raise GraphQLError(f"Donor dengan id {id} tidak ditemukan")
    
    def resolve_donor_by_user_id(self, info, user_id):
        try:
            return Donor.objects.get(user_id=user_id)
        except Donor.DoesNotExist:
            raise GraphQLError(f"Donor dengan user_id {user_id} tidak ditemukan")

class VolunteerQuery(graphene.ObjectType):
    volunteer = graphene.Field(VolunteerType, id=graphene.UUID(required=True))
    volunteer_by_user_id = graphene.Field(VolunteerType, user_id=graphene.UUID(required=True))
    
    def resolve_volunteer(self, info, id):
        try:
            return Volunteer.objects.get(id=id)
        except Volunteer.DoesNotExist:
            raise GraphQLError(f"Volunteer dengan id {id} tidak ditemukan")
    
    def resolve_volunteer_by_user_id(self, info, user_id):
        try:
            return Volunteer.objects.get(user_id=user_id)
        except Volunteer.DoesNotExist:
            raise GraphQLError(f"Volunteer dengan user_id {user_id} tidak ditemukan")

class DonationAreaQuery(graphene.ObjectType):
    donation_area = graphene.Field(DonationAreaType, id=graphene.Int(required=True))
    
    def resolve_donation_area(self, info, id):
        try:
            return DonationArea.objects.get(id=id)
        except DonationArea.DoesNotExist:
            raise GraphQLError(f"Donation Area dengan id {id} tidak ditemukan")

class DonationQuery(graphene.ObjectType):
    donation = graphene.Field(DonationType, id=graphene.Int(required=True))
    
    def resolve_donation(self, info, id):
        try:
            return Donation.objects.get(id=id)
        except Donation.DoesNotExist:
            raise GraphQLError(f"Donation dengan id {id} tidak ditemukan")