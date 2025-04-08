from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, LogoutSerializer


@swagger_auto_schema(
    method='get',
    operation_description="Get authenticated user's details",
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            #JWT TOKEN
            description="Bearer {JWT Token}",
            type=openapi.TYPE_STRING,
            required=True
        ),
    ],
    responses={
        200: UserSerializer,
        401: openapi.Response(description="Unauthorized"),
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_auth_user(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response({
        'status': 'ok',
        'data': serializer.data
    }, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    operation_description="User login with email and password",
    request_body=LoginSerializer,
    responses={
        200: openapi.Response(
            description="Successful login",
            examples={
                "application/json": {
                    "access": "your_access_token",
                    "refresh": "your_refresh_token",
                    "user": {
                        "id": 1,
                        "email": "user@example.com",
                        "first_name": "John",
                        "last_name": "Doe"
                    }
                }
            }
        ),
        401: openapi.Response(description="Invalid credentials"),
        400: openapi.Response(description="Bad request"),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(email=email, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    operation_description="User registration",
    request_body=RegisterSerializer,
    responses={
        201: openapi.Response(
            description="User created successfully",
            examples={
                "application/json": {
                    "access": "your_access_token",
                    "refresh": "your_refresh_token",
                    "user": {
                        "id": 1,
                        "email": "newuser@example.com",
                        "first_name": "Jane",
                        "last_name": "Doe"
                    }
                }
            }
        ),
        400: openapi.Response(description="Bad request"),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # refresh = RefreshToken.for_user(user)
        
        return Response({
            'status': 'success',
            'message': 'User created succesfully, You can login now',
            'data': {
                'user': UserSerializer(user).data
            }
        }, status=status.HTTP_201_CREATED)
    return Response({
        'status': 'error',
        'message': 'Validasi gagal',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    operation_description="User logout",
    request_body=LogoutSerializer,
    responses={
        205: openapi.Response(description="Logout successful"),
        400: openapi.Response(description="Invalid refresh token"),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])  # BUKAN IsAuthenticated
def logout(request):
    try:
        refresh_token = request.data.get("refresh")  # Gunakan .get() untuk menghindari KeyError
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

