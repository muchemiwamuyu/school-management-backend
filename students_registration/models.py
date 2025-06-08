from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class RegisterStudents(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name='student')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    parents_email = models.EmailField(unique=True)
    class_name = models.CharField(max_length=100)
    parents_number = models.CharField(max_length=15, unique=True)
    date_of_joining = models.DateField()
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"