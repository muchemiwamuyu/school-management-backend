from django.urls import path
from .views import *

urlpatterns = [
    path('request/', requestForm, name='request_form'),
]
