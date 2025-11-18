from django.urls import path, re_path
from . import views

urlpatterns = [
    path('auth/login', views.login, name='login'),
    path('auth/register', views.register, name='register'),
    # path('auth/logout', views.logout, name='logout'),
    path('auth/profile', views.get_auth_user, name='get_auth_user'),
]