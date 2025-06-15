from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class RegisterSchoolStaff(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='staff_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    id_number = models.IntegerField(unique=True)
    date_of_birth = models.DateField()
    date_of_joining = models.DateField()
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='created_staff_members')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
# this is the one that will link the staff to the school
class School_Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.department}"
    
class DutyRoaster(models.Model):
    staff = models.ForeignKey(RegisterSchoolStaff, on_delete=models.CASCADE)
    duty = models.CharField(max_length=100)
    date = models.DateField()
    time  = models.TimeField()

    def __str__(self):
        return f"{self.staff.first_name} - {self.duty} on {self.date} at {self.time}"
    

class Meeting(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=200)
    agenda = models.TextField()
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.title} on {self.date}"