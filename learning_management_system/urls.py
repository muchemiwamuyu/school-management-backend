from django.urls import path
from .views import *

# creating the url patterns

urlpatterns = [
    path('learning/', register_sys_admin, name='register_sys_admin')
]
