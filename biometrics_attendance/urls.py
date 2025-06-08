from django.urls import path
from .views import *

# creating the urls for the biometrics attendance

urlpatterns = [
    path('register_face/', register_face, name='register_face'),
    path('check_in/', face_checkin, name='face_checkin'),
]
