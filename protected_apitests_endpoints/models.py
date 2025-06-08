from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class RegisterMainStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='main_staff')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"