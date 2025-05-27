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

class ManageDonorView(generics.RetrieveUpdateAPIView):
    queryset = Donor.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return DonorUpdateSerializer
        return DonorSerializer

    @swagger_auto_schema(
        operation_description="Retrieve donor detail (Requires JWT Token)",
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
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
    operation_description="Update donor photo and verification (multipart/form-data, Requires JWT Token)",
        manual_parameters=[
            openapi.Parameter(
                name='photo_url',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description='Photo url',
                required=False
            ),
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                description='Bearer JWT Access token',
                type=openapi.TYPE_STRING,
                required=True
            ),
        ]
    )

    def patch(self, request, *args, **kwargs):
        donor = self.get_object()
        data = request.data.copy()
        
        user_photo = request.FILES.get('photo_url')
        if user_photo:
            success, result = upload_image(user_photo, folder='donatur')
            if not success:
                return Response({"error": result}, status=400)
            data['photo_url'] = result  # Inject URL string to serializer input
        serializer = self.get_serializer(donor, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'status': 'success',
            'message': 'Donor updated successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


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

class ManageVolunteerView(generics.RetrieveUpdateAPIView):
    queryset = Volunteer.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return VolunteerUpdateSerializer
        return VolunteerSerializer

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
    operation_description="Update volunteer photo and verification (multipart/form-data, Requires JWT Token)",
        manual_parameters=[
            openapi.Parameter(
                name='photo_url',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description='Photo url',
                required=False
            ),
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                description='Bearer JWT Access token',
                type=openapi.TYPE_STRING,
                required=True
            ),
        ]
    )

    def patch(self, request, *args, **kwargs):
        volunteer = self.get_object()
        data = request.data.copy()
        
        user_photo = request.FILES.get('photo_url')
        if user_photo:
            success, result = upload_image(user_photo, folder='volunteer')
            if not success:
                return Response({"error": result}, status=400)
            data['photo_url'] = result
        serializer = self.get_serializer(volunteer, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'status': 'success',
            'message': 'Volunteer updated successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class AcceptedVolunteerView(generics.ListAPIView):
    queryset = Volunteer.objects.filter(status='ACCEPTED')
    serializer_class = VolunteerSerializer

class RejectedVolunteerView(generics.ListAPIView):
    queryset = Volunteer.objects.filter(status='REJECTED')
    serializer_class = VolunteerSerializer

class AllVolunteerView(generics.ListAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer

class ViewVolunteerDetailView(generics.RetrieveAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    lookup_field = 'id'

# Donation views
class NewDonationView(generics.CreateAPIView):
    queryset = Donation.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = DonationSerializer
    
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
                name='image_url',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description='Donation Picture',
                required=True
            ),
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
        data = request.data.copy()
        donation_picture = request.FILES.get('image_url')
        
        if not donation_picture:
            return Response({"error": "Image file is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        success, result = upload_image(donation_picture, folder='donations')
        if not success:
            return Response({"error": result}, status=status.HTTP_400_BAD_REQUEST)
        
        data['image_url'] = result  # Inject URL string to serializer input
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            'status': 'success',
            'message': 'Donation created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

class DonationListView(generics.ListAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticated]
    
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
        responses={200: DonationSerializer(many=True)}
    )
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'ok',
            'message': 'List of donations',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class ManageDonationView(generics.RetrieveUpdateAPIView):
    queryset = Donation.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if getattr(self, 'swagger_fake_view', False):
            return DonationSerializer  # default serializer untuk dokumentasi

        if self.request.method in ['GET', 'PUT']:
            return DonationSerializer
        elif self.request.method == 'PATCH':
            return DonationUpdateSerializer
        return DonationSerializer  # fallback default

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
        operation_description="Update a donation by ID (partial update - PATCH) (Requires JWT Access Token)",
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
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

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
        return super().put(request, *args, **kwargs)

class DonationDeleteView(generics.DestroyAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    @swagger_auto_schema(
        operation_description="Delete a donation (Requires JWT Access Token)",
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
    serializer_class = DonationAreaSerializer

    @swagger_auto_schema(
        operation_description="Get all active donation areas (is_active=True)",
        responses={200: DonationAreaSerializer(many=True)},
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
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return DonationAreaUpdateSerializer
        return DonationAreaSerializer

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
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a donation area partially (PATCH - Only postal code and description)",
        request_body=DonationAreaUpdateSerializer,
        responses={200: DonationAreaUpdateSerializer},
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
    
    def patch(self, request, *args, **kwargs):
        donation = self.get_object()
        data = request.data.copy()
        
        donation_picture = request.FILES.get('image_url')
        if donation_picture:
            success, result = upload_image(donation_picture, folder='donations')
            if not success:
                return Response({"error": result}, status=400)
            data['image_url'] = result
        serializer = self.get_serializer(donation, data=data, partial=True)
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