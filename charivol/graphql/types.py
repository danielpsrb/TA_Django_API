import graphene
from graphene_django import DjangoObjectType
from charivol.models import Donor
from charivol.models import Volunteer
from charivol.models import DonationArea
from charivol.models import Donation

class DonorType(DjangoObjectType):
    class Meta:
        model = Donor
        fields = '__all__'
        read_only_fields = ['register_date', 'is_verified']

class VolunteerType(DjangoObjectType):
    class Meta:
        model = Volunteer
        fields = '__all__'
        read_only_fields = ['register_date']

class DonationAreaType(DjangoObjectType):
    class Meta:
        model = DonationArea
        fields = '__all__'
        read_only_fields = ['creation_date', 'is_active']

class DonationType(DjangoObjectType):
    volunteer_id = graphene.Int()
    
    donaturId = graphene.Int()

    class Meta:
        model = Donation
        fields = (
            "id",
            "donation_name",
            "description",
            "image_url",
            "donation_date",
            "donation_status",
            "volunteer",
            "volunteer_remarks"
        )

    def resolve_volunteer_id(self, info):
        return self.volunteer.id if self.volunteer else None
    
    def resolve_donaturId(self, info):
        return self.donatur.id if self.donatur else None
