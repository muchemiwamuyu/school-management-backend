from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class RegisterSchoolStaff(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    id_number = models.IntegerField(unique=True)
    date_of_birth = models.DateField()
    date_of_joining = models.DateField()
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
# this is the one that will link the staff to the school
class School_Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.department}"