from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'contact', 'province', 'city' 'address', 'donation_date')

admin.site.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'contact', 'province', 'city' 'address', 'donation_date')

admin.site.register(DonationArea)
class DonationAreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'area_name', 'description', 'creation_date')

admin.site.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('id', 'donor', 'volunteer', 'donation_area', 'donation_name')

admin.site.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'donation', 'delivery_picture', 'creation_date')