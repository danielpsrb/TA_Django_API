from django.urls import path
from . import views

urlpatterns = [
    
    # Donate
    path('charivol/all-donations', views.DonationListView.as_view(), name='donate'),
    path('charivol/donate-now', views.DonateNowView.as_view(), name='donate_now'),
    path('charivol/manage-donate/<str:pk>', views.ManageDonationView.as_view(), name='manage_donate'),
    path('charivol/delete-donate/<str:pk>', views.DonationDeleteView.as_view(), name='delete_donate'),
    
    # Donor
    path('charivol/new-donatur', views.NewDonorView.as_view(), name='create_donor'),
    path('charivol/manage-donatur/<str:pk>', views.ManageDonorView.as_view(), name='manage_donor'),
    
    # Volunteer
    path('charivol/new-volunteer', views.NewVolunteerView.as_view(), name='new_volunteer'),
    path('charivol/manage-volunteers/<str:pk>', views.ManageVolunteerView.as_view(), name='manage_volunteer'),
    
]
