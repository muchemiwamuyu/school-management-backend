from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Learning_Admin(models.Model):
    LEARNING_GROUP_CHOICES=[
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name='teachers')
    learners_capacity = models.CharField(max_length=10, choices=LEARNING_GROUP_CHOICES)
    
    

