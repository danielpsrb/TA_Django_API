from django.conf import settings
from django.db import models

class Donor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contact = models.CharField(max_length=20, null=False)
    province = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    address = models.TextField(max_length=255, null=False)
    photo_url = models.URLField(blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        null=True,
        blank=True,
    )
    occupation = models.CharField(max_length=50, blank=True, null=True)
    register_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = 'charivol_donaturs'
        verbose_name = 'Donatur'

class Volunteer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    province = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    contact = models.CharField(max_length=20, blank=False, null=False)
    address = models.TextField(blank=False, null=False)
    photo_url = models.URLField(blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        null=True,
        blank=True,
    )
    register_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = 'charivol_volunteers'
        verbose_name = 'Volunteer'

class Donation(models.Model):
    donatur = models.ForeignKey(Donor, on_delete=models.CASCADE)
    donation_name = models.CharField(max_length=40)
    description = models.TextField(blank=False, null=False)
    image_url = models.URLField(blank=True, null=True)
    donation_status = models.CharField(max_length=20, default='PENDING')
    volunteer = models.ForeignKey(Volunteer, on_delete=models.SET_NULL, blank=True, null=True)
    donation_date = models.DateField(auto_now_add=True)
    volunteer_remarks = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.id
    
    class Meta:
        db_table = 'charivol_donations'
        verbose_name = 'Donation'

class DonationArea(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.SET_NULL, blank=True, null=True)
    area_name = models.CharField(max_length=100, blank=False, null=False)
    area_province = models.CharField(max_length=50, blank=False, null=False)
    area_city = models.CharField(max_length=50, blank=False, null=False)
    area_postal_code = models.CharField(max_length=10, blank=True, null=True)
    area_address = models.TextField(blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.area_name
    
    class Meta:
        db_table = 'charivol_donation_areas'
        verbose_name = 'Donation Area'