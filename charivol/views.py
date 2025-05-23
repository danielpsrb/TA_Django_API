from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
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
        
        response_data = {
            status: 'success',
            'message': 'Volunteer created successfully',
            'data': serializer.data
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)

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
                name='user_photo',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description='User photo',
                required=False
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

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

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
class DonateNowView(generics.CreateAPIView):
    queryset = Donation.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    
    serializer_class = DonationSerializer
    
    @swagger_auto_schema(
        operation_description="Create a new Donation (Requires JWT Access Token)",
        request_body=DonationSerializer,
        responses={
            201: DonationSerializer,
            400: "Bad Request",
            401: "Unauthorized",
        },
        manual_parameters=[
            openapi.Parameter(
                name='donation_photo',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description='User photo',
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        response_data = {
            'status': 'success',
            'message': 'Donation created successfully',
            'data': serializer.data
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)

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
    lookup_field = 'pk'  # atau 'id' jika kamu yakin field PK kamu bernama 'id'

    def get_serializer_class(self):
        if getattr(self, 'swagger_fake_view', False):
            return DonationSerializer  # default serializer untuk dokumentasi

        if self.request.method == 'GET':
            return DonationSerializer
        elif self.request.method in ['PATCH', 'PUT']:
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

class AllDonationsView(generics.ListAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer

class DonationHistoryView(generics.ListAPIView):
    serializer_class = DonationSerializer

    def get_queryset(self):
        donor_id = self.request.query_params.get('donor_id')
        return Donation.objects.filter(donor__id=donor_id)

class PendingDonationView(generics.ListAPIView):
    queryset = Donation.objects.filter(status=DonationStatus.PENDING)
    serializer_class = DonationSerializer

class AcceptedDonationView(generics.ListAPIView):
    queryset = Donation.objects.filter(status=DonationStatus.ACCEPTED)
    serializer_class = DonationSerializer

class RejectedDonationView(generics.ListAPIView):
    queryset = Donation.objects.filter(status=DonationStatus.REJECTED)
    serializer_class = DonationSerializer

class AcceptedDonationDetailView(generics.RetrieveAPIView):
    queryset = Donation.objects.filter(status=DonationStatus.ACCEPTED)
    serializer_class = DonationSerializer
    lookup_field = 'id'

class ViewDonationDetailView(generics.RetrieveAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    lookup_field = 'id'

class DonationDetailDonorView(generics.ListAPIView):
    serializer_class = DonationSerializer

    def get_queryset(self):
        donor_id = self.kwargs['pid']
        return Donation.objects.filter(donor__id=donor_id)

class CollectionRequestView(generics.ListAPIView):
    queryset = Donation.objects.filter(status=DonationStatus.ACCEPTED)
    serializer_class = DonationSerializer

class DonationReceivedVolunteerView(generics.ListAPIView):
    serializer_class = DonationSerializer

    def get_queryset(self):
        return Donation.objects.filter(volunteer__id=self.request.query_params.get('volunteer_id'), status='RECEIVED')

class DonationNotReceivedVolunteerView(generics.ListAPIView):
    serializer_class = DonationSerializer

    def get_queryset(self):
        return Donation.objects.filter(volunteer__id=self.request.query_params.get('volunteer_id')).exclude(status='RECEIVED')

class DonationDeliveredVolunteerView(generics.ListAPIView):
    serializer_class = DonationSerializer

    def get_queryset(self):
        return Donation.objects.filter(volunteer__id=self.request.query_params.get('volunteer_id'), status='DELIVERED')

class DonationReceivedDetailView(generics.RetrieveAPIView):
    serializer_class = DonationSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Donation.objects.filter(status='RECEIVED')

class DonationCollectionDetailView(generics.RetrieveAPIView):
    serializer_class = DonationSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Donation.objects.filter(status='DELIVERED')

# Gallery views
class GalleryView(generics.ListAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer

# Area views
class AddAreaView(generics.CreateAPIView):
    queryset = DonationArea.objects.all()
    serializer_class = DonationAreaSerializer

class EditAreaView(generics.RetrieveUpdateAPIView):
    queryset = DonationArea.objects.all()
    serializer_class = DonationAreaSerializer
    lookup_field = 'id'

class ManageAreaView(generics.ListAPIView):
    queryset = DonationArea.objects.all()
    serializer_class = DonationAreaSerializer