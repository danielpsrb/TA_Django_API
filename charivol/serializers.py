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
    class Meta:
        model = Volunteer
        fields = ['user_id', 'contact', 'address']
        read_only_fields = ['register_date', 'updation_date']

class VolunteerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = ['photo_url', 'gender', 'province', 'city', 'about_me']
        read_only_fields = ['updation_date']

    def validate_user_photo(self, value):
        return self.validate_image_file(value, field_name='photo_url')

    def validate_image_file(self, file, field_name):
        allowed_extensions = ['jpg', 'jpeg', 'png']
        max_size = 5 * 1024 * 1024
        file_extension = file.name.split('.')[-1].lower()
        
        if file_extension not in allowed_extensions:
            raise serializers.ValidationError(
                f"{field_name.replace('_', ' ').title()} must be a JPG, JPEG, or PNG file."
            )
        
        if file.size > max_size:
            raise serializers.ValidationError(
                f"{field_name.replace('_', ' ').title()} size must be less than 5MB."
            )
        
        return file

class DonationAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationArea
        exclude = ['id']
        read_only_fields = ['creation_date']

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['donation_name', 'image_url', 'description', 'status', 'donor', 'volunteer', 'donation_area']
        read_only_fields = ['donation_date', 'updation_date']

class DonationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['image_url','collection_location', 'admin_remarks', 'volunteer_remarks', 'updation_date']
        read_only_fields = ['donation_date']

    def validate_donation_photo(self, value):
        return self.validate_image_file(value, field_name='donation_photo')

    def validate_image_file(self, file, field_name):
        allowed_extensions = ['jpg', 'jpeg', 'png']
        max_size = 5 * 1024 * 1024
        file_extension = file.name.split('.')[-1].lower()

        if file_extension not in allowed_extensions:
            raise serializers.ValidationError(
                f"{field_name.replace('_', ' ').title()} must be a JPG, JPEG, or PNG file."
            )

        if file.size > max_size:
            raise serializers.ValidationError(
                f"{field_name.replace('_', ' ').title()} size must be less than 5MB."
            )

        return file

class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        exclude = ['id']
        read_only_fields = ['creation_date']