from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register_school/', register_school_staff, name='register_school_staff'),
    path('registerstaff/', Registerstaff, name='registerstaff'),
    path('loginstaff/', LoginStaff, name='login_staff'),
    path('ping/', ping, name='ping'),
]