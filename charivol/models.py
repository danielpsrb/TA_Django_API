from django.conf import settings
from django.db import models
import cuid

# Create your models here.

def generate_unique_id():
    return cuid.cuid()

class GenderType(models.TextChoices):
    MALE = 'Male', 'Laki-laki'
    FEMALE = 'Female', 'Perempuan'

class Donor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='donatur')
    id = models.CharField(
        primary_key=True,
        max_length=25,
        unique=True,
        default=generate_unique_id,
        editable=False
    )
    contact = models.CharField(max_length=20, null=False)
    province = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    address = models.TextField(max_length=255, null=False)
    gender = models.CharField(
        max_length=10,
        choices=GenderType.choices,
        null=True,
        blank=True,
    )
    #Work
    occupation = models.CharField(max_length=40, blank=True, null=True)
    photo_url = models.URLField(blank=True, null=True) # Store Supabase image URL
    register_date = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)  # Verifikasi admin
    
    def __str__ (self):
        return self.user.username
    
    class Meta:
        db_table = 'charivol_donaturs'
        verbose_name = 'Donatur'


class Volunteer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id = models.CharField(
        primary_key=True,
        max_length=25,
        unique=True,
        default=generate_unique_id,
        editable=False
    )
    province = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    contact = models.CharField(max_length=20, blank=False, null=False)
    address = models.TextField(blank=False, null=False)
    gender = models.CharField(
        max_length=10,
        choices=GenderType.choices,
        null=True,
        blank=True,
    )
    photo_url = models.URLField(blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)  # Status volunteer
    register_date = models.DateTimeField(auto_now_add=True)
    admin_remarks = models.CharField(max_length=255, blank=True, null=True)  # Catatan admin
    updation_date = models.DateField(null=True)  # Tanggal terakhir diupdate
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = 'charivol_volunteers'
        verbose_name = 'Volunteer'


class DonationArea(models.Model):
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

class DonationType(models.TextChoices):
    CLOTHING = 'CLOTHING', 'Pakaian'
    FOOD = 'FOOD', 'Makanan'
    STATIONERY = 'STATIONERY', 'Alat Tulis'
    BOOK = 'BOOK', 'Buku'
    TOY = 'TOY', 'Mainan'
    FOOTWEAR = 'FOOTWEAR', 'Sepatu'
    FURNITURE = 'FURNITURE', 'Perabotan'
    OTHER = 'OTHER', 'Lainnya'

class DonationStatus(models.TextChoices):
    PENDING = 'PENDING', 'Menunggu Konfirmasi'
    ACCEPTED = 'ACCEPTED', 'Diterima'
    REJECTED = 'REJECTED', 'Ditolak'

class Donation(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    id = models.CharField(
        primary_key=True,
        max_length=25,
        unique=True,
        default=generate_unique_id,
        editable=False
    )
    donation_name = models.CharField(
        max_length=40,
        choices=DonationType.choices,
        default=DonationType.FOOD,
        null=False,
        blank=False
    )
    image_url = models.URLField()  # Store Supabase image URL
    collection_location = models.TextField(blank=True, null=True)
    description = models.TextField(blank=False, null=False)
    status = models.CharField(
        max_length=20,
        choices=DonationStatus.choices,
        default=DonationStatus.PENDING,
        blank=False,
        null=False
    )
    donation_date = models.DateField(auto_now_add=True)
    admin_remarks = models.CharField(max_length=100, blank=True, null=True)  # Catatan admin
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, blank=True, null=True)  # Relasi ke volunteer
    donation_area = models.ForeignKey(DonationArea, on_delete=models.CASCADE, blank=True, null=True)  # Relasi ke area donasi
    volunteer_remarks = models.CharField(max_length=100, blank=True, null=True)  # Catatan volunteer
    updation_date = models.DateField(null=True)  # Tanggal terakhir diupdate
    
    def __str__(self):
        return self.id
    
    class Meta:
        db_table = 'charivol_donations'
        verbose_name = 'Donation'

class Gallery(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    delivery_picture_url = models.URLField(blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.id
    
    class Meta:
        db_table = 'charivol_gallery'
        verbose_name = 'Gallery'