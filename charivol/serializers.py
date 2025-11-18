from rest_framework import serializers
from .models import *

class DonorSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.id', read_only=True)
    class Meta:
        model = Donor
        fields = ['user_id', 'contact', 'address']
        read_only_fields = ['register_date']

class DonorUpdateSerializer(serializers.ModelSerializer):
    photo_url = serializers.URLField(required=False)

    class Meta:
        model = Donor
        fields = ['user_id', 'contact', 'address', 'photo_url', 'gender', 'province', 'city', 'occupation']

class VolunteerSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.id', read_only=True)
    class Meta:
        model = Volunteer
        fields = ['user_id', 'contact', 'address']
        read_only_fields = ['register_date']

class VolunteerUpdateSerializer(serializers.ModelSerializer):
    photo_url = serializers.URLField(required=False)
    
    class Meta:
        model = Volunteer
        fields = ['user_id', 'contact', 'address', 'photo_url', 'gender', 'province', 'city']
        read_only_fields = ['register_date']

class DonationAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationArea
        fields = ['area_name', 'area_province', 'area_city', 'area_address']
        read_only_fields = ['id', 'creation_date', 'is_active']

class DonationAreaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationArea
        fields = ['area_name', 'area_province', 'area_city', 'area_postal_code', 'area_address', 'description', 'is_active', 'creation_date']
        read_only_fields = ['id','creation_date', 'is_active']

class DonationSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(required=False)
    
    class Meta:
        model = Donation
        fields = ['donation_name', 'donatur', 'image_url', 'description']
        read_only_fields = ['donation_date']

class DonationUpdateSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(required=False)

    class Meta:
        model = Donation
        fields = [
            'donatur_id',
            'donation_name',
            'image_url',
            'description',
            'volunteer',           # pastikan ini FK atau sesuai field
            'volunteer_remarks',      # tambahkan field ini
            'donation_status'
        ]
        read_only_fields = ['donation_date']


class AllDonationSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(required=False)
    volunteer = VolunteerSerializer(read_only=True)

    class Meta:
        model = Donation
        fields = ['id', 'donation_name', 'image_url', 'description', 'donation_date', 'volunteer', 'donation_status']
        read_only_fields = ['donation_date']