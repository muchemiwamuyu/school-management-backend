from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class FaceRegistration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name='face_registration')
    face_data = models.BinaryField()  # Store the face data as binary
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Face Registration for {self.user.username}"
    
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(auto_now_add=True)
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Attendance for {self.user.username} on {self.date}"