from rest_framework import serializers
from auth_app.models import User
from django.contrib.auth import authenticate
import re

class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email')

class RegisterSerializer(serializers.ModelSerializer):
    password     = serializers.CharField(write_only=True)
    confirm_pass = serializers.CharField(write_only=True)
    
    class Meta:
        model= User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'confirm_pass')
    
    def validate(self, data):
        password     = data.get('password')
        confirm_pass = data.get('confirm_pass')
        
        if password != confirm_pass:
            raise serializers.ValidationError("Password and confirm password do not match")
        
        return data
    
    def validate_email(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError("Invalid email format")
        return value
    
    def create(self, validated_data):
        validated_data.pop('confirm_pass', None)
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if not user:
                raise serializers.ValidationError("Invalid email or password.")

            data['user'] = user
            return data

        raise serializers.ValidationError("Both email and password are required.")

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
    def validate(self, attrs):
        refresh = attrs.get('refresh')
        if not refresh:
            raise serializers.ValidationError("Refresh token is required.")