from rest_framework import serializers
from .models import *

class DonorSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.id', read_only=True)
    class Meta:
        model = Donor
        fields = ['user_id', 'contact', 'address']
        read_only_fields = ['register_date', 'is_verified']

class DonorUpdateSerializer(serializers.ModelSerializer):
    photo_url = serializers.URLField(required=False)

    class Meta:
        model = Donor
        fields = ['photo_url', 'gender', 'province', 'city', 'occupation']

class VolunteerSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.id', read_only=True)
    class Meta:
        model = Volunteer
        fields = ['user_id', 'contact', 'address']
        read_only_fields = ['register_date', 'updation_date']

class VolunteerUpdateSerializer(serializers.ModelSerializer):
    photo_url = serializers.URLField(required=False)
    
    class Meta:
        model = Volunteer
        fields = ['photo_url', 'gender', 'province', 'city', 'about_me']
        read_only_fields = ['updation_date']

class DonationAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationArea
        fields = ['area_name', 'area_province', 'area_city', 'area_address']
        read_only_fields = ['creation_date', 'is_active']

class DonationAreaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationArea
        fields = ['area_postal_code', 'description', 'is_active']
        read_only_fields = ['creation_date']

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['donation_name', 'image_url', 'description', 'donor', 'volunteer', 'donation_area']
        read_only_fields = ['donation_date', 'updation_date']

class DonationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['image_url', 'collection_location', 'status', 'admin_remarks', 'volunteer_remarks', 'updation_date']
        read_only_fields = ['donation_date', 'updation_date']