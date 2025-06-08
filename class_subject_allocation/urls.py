from django.urls import path
from .views import *

# creating the urls for the class subject allocation 
urlpatterns = [
    path('add_class/', register_class, name='register_class'),
    path('classes/', get_classes, name='get_classes'),
    path('class/<int:class_id>/', update_class, name='update_class'),
    path('class/<int:class_id>/delete/', delete_class, name='delete_class'),
    ]
