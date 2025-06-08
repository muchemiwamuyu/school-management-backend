from django.urls import path
from .views import *

# creating urls for the students registration
urlpatterns = [
    path('register_student/', register_student, name='register_student'),
    path('students/', get_students, name='get_students'),
    path('student/<int:student_id>/', update_student, name='update_student'),
    path('student/<int:student_id>/delete/', delete_student, name='delete_student'),
]
