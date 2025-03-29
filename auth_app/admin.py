from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

    # Form Edit User di Admin
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("username", "first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
    )

    # Form Add New User di Admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
            "email", "username", "first_name", "last_name", "password1", "password2", "is_staff", "is_active",
            "is_superuser"),
        }),
    )

# Mendaftarkan model ke Django Admin
admin.site.register(User, CustomUserAdmin)



# Register your models here.
