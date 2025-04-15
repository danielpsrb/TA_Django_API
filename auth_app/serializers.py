from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from auth_app.models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
import re

class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email')

class RegisterSerializer(serializers.ModelSerializer):
    password     = serializers.CharField(write_only=True, min_length=8)
    confirm_pass = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model= User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'confirm_pass')
    
    # validate first_name min length 2, max length 150, only letters
    def validate_first_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("First name must be at least 2 characters long.")
        if not re.match(r'^[a-zA-Z]+$', value):
            raise serializers.ValidationError("First name must contain only letters.")
        if len(value) > 150:
            raise serializers.ValidationError("First name must be at most 150 characters long.")
        return value
    
    # validate last_name min length 2, max length 150, only letters
    def validate_last_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Last name must be at least 2 characters long.")
        if not re.match(r'^[a-zA-Z]+$', value):
            raise serializers.ValidationError("Last name must contain only letters.")
        if len(value) > 150:
            raise serializers.ValidationError("Last name must be at most 150 characters long.")
        return value
    
    # validate username min length 4, max length 150, only lowercase letters and numbers
    def validate_username(self, value):
        # check if username already exists in the database
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        # check username must be at least 4 characters long
        if len(value) < 4:
            raise serializers.ValidationError("Username must be at least 4 characters long.")
        # check if username contains only lowercase letters and numbers
        if not re.match(r'^[a-z0-9]+$', value):
            raise serializers.ValidationError("Username must contain only lowercase letters and numbers.")
        # check username must be at most 150 characters long
        if len(value) > 150:
            raise serializers.ValidationError("Username must be at most 150 characters long.")
        return value
    
    # validate email format
    def validate_email(self, value):
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
            raise serializers.ValidationError("Invalid email format.")
        # if email is already exists in the database
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        # if len < 1
        if len(value) < 1:
            raise serializers.ValidationError("Email must be at least 1 character long.")
        return value
    
    # validate password
    def validate(self, data):
        password     = data.get('password')
        confirm_pass = data.get('confirm_pass')
        
        if password != confirm_pass:
            raise serializers.ValidationError("Passwords do not match.")
        
        errMsg = []
        
        if len(password) < 8:
            errMsg.append("Password must be at least 8 characters long.")
        
        # check whether the password contains uppercase, lowercase and numbers
        checks = {
            'Password must contain at least one uppercase letter': r'[A-Z]',
            'Password must contain at least one lowercase letter': r'[a-z]',
            'Password must contain at least one number': r'[0-9]',
        }
        
        errMsg.extend([msg for msg, regex in checks.items() if not re.search(regex, password)])
        
        if errMsg:
            raise serializers.ValidationError(errMsg)
        return data
    
    def create(self, validated_data):
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
    
    # def validate(self, data):
    #     user = authenticate(email=data['email'], password=data['password'])
    #     if not user:
    #         raise serializers.ValidationError('Invalid email or password')
    #     return user

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()