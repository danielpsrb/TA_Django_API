from django.urls import path
from . import views
from .views import SoftDeleteDonationAreaView, ListActiveDonationAreaView
urlpatterns = [
    
    # Donate
    path('charivol/all-donations', views.DonationListView.as_view(), name='donate'),
    path('charivol/donations', views.NewDonationView.as_view(), name='new_donate'),
    path('charivol/donations/<str:pk>', views.ManageDonationView.as_view(), name='manage_donate'),
    # path('charivol/delete-donate/<str:pk>', views.DonationDeleteView.as_view(), name='delete_donate'),
    
    # Donor
    path('charivol/donaturs', views.NewDonorView.as_view(), name='create_donor'),
    path('charivol/donaturs/<str:pk>', views.ManageDonorView.as_view(), name='manage_donor'),
    
    # Volunteer
    path('charivol/volunteers', views.NewVolunteerView.as_view(), name='new_volunteer'),
    path('charivol/volunteers/<str:pk>', views.ManageVolunteerView.as_view(), name='manage_volunteer'),
    
    # Donation Area
    path('charivol/all-donation-areas', ListActiveDonationAreaView.as_view(), name='list-active-donation-areas'),
    path('charivol/donation-areas', views.NewDonationAreaView.as_view(), name='new_donation_area'),
    path('charivol/donation-areas/<int:id>', views.ManageDonationAreaView.as_view(), name='manage_donation_area'),
    path('charivol/donation-areas/wipe/<int:id>', SoftDeleteDonationAreaView.as_view(), name='soft-delete-donation-area'),
]
