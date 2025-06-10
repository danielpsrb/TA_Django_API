from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import *
from .serializers import *
from .utils import upload_image

# Donor views
class NewDonorView(generics.CreateAPIView):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
    
    @swagger_auto_schema(
        operation_description="Create a new Donatur (Requires JWT Access token)",
        request_body=DonorSerializer,
        responses={
            201: DonorSerializer,
            400: "Bad Request",
            401: "Unauthorized",
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                in_=openapi.IN_HEADER,
                description="Bearer JWT Access Token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({
            'status': 'success',
            'message': 'Donatur created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

class ManageDonorView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Donor.objects.all()
    serializer_class = DonorUpdateSerializer
    lookup_field = 'id'
    http_method_names = ['get', 'put', 'delete']
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve donor detail by ID (Requires JWT Token)",
        responses={200: DonorSerializer},
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                in_=openapi.IN_HEADER,
                description="Bearer JWT token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        donor = self.get_object()
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update donor info (Requires JWT Token, accepts JSON)",
        request_body=DonorUpdateSerializer,
        responses={200: DonorUpdateSerializer},
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                description='Bearer JWT token',
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def put(self, request, *args, **kwargs):
        donor = self.get_object()
        serializer = self.get_serializer(donor, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'status': 'success',
            'message': 'Donor updated successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete donor by ID (Requires JWT Token)",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                in_=openapi.IN_HEADER,
                description='Bearer JWT token',
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={204: "No Content"}
    )
    def delete(self, request, *args, **kwargs):
        donor = self.get_object()
        self.perform_destroy(donor)
        return Response(status=status.HTTP_204_NO_CONTENT)

# Volunteer views
class NewVolunteerView(generics.CreateAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    
    @swagger_auto_schema(
        operation_description="Create a new Volunteer (Requires JWT Token)",
        request_body=VolunteerSerializer,
        responses={
            201: VolunteerSerializer,
            400: "Bad Request",
            401: "Unauthorized",
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                in_=openapi.IN_HEADER,
                description="Bearer JWT Access Token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        
        return Response({
            'status': 'success',
            'message': 'Volunteer created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

class ManageVolunteerView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerUpdateSerializer
    lookup_field = 'id'
    http_method_names = ['get', 'put', 'delete']
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve volunteer detail (Requires JWT Token)",
        responses={200: VolunteerSerializer},
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                in_=openapi.IN_HEADER,
                description="Bearer JWT Access token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update volunteer info (Requires JWT Token, accepts JSON only)",
        request_body=VolunteerUpdateSerializer,
        responses={200: VolunteerUpdateSerializer},
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                description='Bearer JWT Access Token',
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def put(self, request, *args, **kwargs):
        volunteer = self.get_object()
        serializer = self.get_serializer(volunteer, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'status': 'success',
            'message': 'Volunteer updated successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete a Volunteer by ID (Requires JWT Access Token)",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                in_=openapi.IN_HEADER,
                description='Bearer JWT Access Token',
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={204: "No Content"}
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

# Donation views
class NewDonationView(generics.CreateAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    #permission_classes = [IsAuthenticated]  # Optional: kalau kamu pakai JWT

    @swagger_auto_schema(
        operation_description="Create New Donation (Requires JWT Access Token)",
        request_body=DonationSerializer,
        responses={
            201: DonationSerializer,
            400: "Bad Request",
            401: "Unauthorized",
        },
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                description='Bearer JWT token',
                type=openapi.TYPE_STRING,
                required=True
            ),
        ]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            'status': 'success',
            'message': 'Donation created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

class DonationListView(generics.ListAPIView):
    queryset = Donation.objects.all()
    serializer_class = AllDonationSerializer
    # permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Retrieve all donations (Requires JWT Access Token)",
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                description='Bearer <JWT Access Token>',
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: AllDonationSerializer(many=True)}
    )
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'ok',
            'message': 'List of All Donations',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class ManageDonationView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationUpdateSerializer
    lookup_field = 'id'
    http_method_names = ['get', 'put', 'delete']
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a donation detail by ID (Requires JWT Access Token)",
        responses={200: DonationSerializer},
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                description='Bearer <JWT Access Token>',
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a donation by ID (full update - PUT) (Requires JWT Access Token)",
        request_body=DonationUpdateSerializer,
        responses={200: DonationUpdateSerializer},
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                description='Bearer <JWT Access Token>',
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def put(self, request, *args, **kwargs):
        donation = self.get_object()
        serializer = self.get_serializer(donation, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'status': 'success',
            'message': 'Donation updated successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete a donation by ID (Requires JWT Access Token)",
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                description='Bearer <JWT Access Token>',
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={204: "No Content"}
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ListActiveDonationAreaView(generics.ListAPIView):
    queryset = DonationArea.objects.filter(is_active=True)
    serializer_class = DonationAreaUpdateSerializer

    @swagger_auto_schema(
        operation_description="Get all active donation areas (is_active=True)",
        responses={200: DonationAreaUpdateSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                in_=openapi.IN_HEADER,
                description='Bearer JWT Access Token',
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'success',
            'message': 'List of active donation areas retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class NewDonationAreaView(generics.CreateAPIView):
    queryset = DonationArea.objects.all()
    serializer_class = DonationAreaSerializer

    @swagger_auto_schema(
        operation_description="Create a new Donation Area (Requires JWT Access Token)",
        request_body=DonationAreaSerializer,
        responses={
            201: DonationAreaSerializer,
            400: "Bad Request",
            401: "Unauthorized",
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                in_=openapi.IN_HEADER,
                description="Bearer JWT Access Token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'status': 'success',
            'message': 'Donation Area created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

class ManageDonationAreaView(generics.RetrieveUpdateAPIView):
    queryset = DonationArea.objects.all()
    serializer_class = DonationAreaUpdateSerializer  # Required for schema generation
    lookup_field = 'id'
    http_method_names = ['get', 'put']  # Only allow GET and PUT methods

    def get_serializer_class(self):
        return DonationAreaSerializer  # Always return this

    @swagger_auto_schema(
        operation_description="Retrieve a donation area detail (Requires JWT Access Token)",
        responses={200: DonationAreaSerializer},
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                in_=openapi.IN_HEADER,
                description='Bearer JWT Access Token',
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a donation area fully (PUT - Requires JWT Access Token)",
        request_body=DonationAreaSerializer,
        responses={200: DonationAreaSerializer},
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                in_=openapi.IN_HEADER,
                description='Bearer JWT Access Token',
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def put(self, request, *args, **kwargs):
        donation_area = self.get_object()
        serializer = self.get_serializer(donation_area, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'status': 'success',
            'message': 'Donation Area updated successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class SoftDeleteDonationAreaView(APIView):
    @swagger_auto_schema(
        operation_description="Soft delete a donation area by setting is_active=False (Requires JWT Access Token)",
        responses={204: 'No Content', 400: 'Bad Request'},
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                in_=openapi.IN_HEADER,
                description='Bearer JWT Access Token',
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'id',
                in_=openapi.IN_PATH,
                description='ID dari Donation Area yang ingin di-nonaktifkan',
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    def delete(self, request, id):
        try:
            donation_area = DonationArea.objects.get(id=id)
            donation_area.is_active = False
            donation_area.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except DonationArea.DoesNotExist:
            return Response({'detail': 'Donation Area tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)