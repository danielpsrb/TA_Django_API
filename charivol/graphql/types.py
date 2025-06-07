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
    class Meta:
        model = Donation
        fields = '__all__'
        read_only_fields = ['donation_date']