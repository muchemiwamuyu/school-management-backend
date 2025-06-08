from django.db import models

# Create your models here.

class ClassRegistration(models.Model):
    CLASS_CAPACITY_CHOICES = [
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
    ]

    class_name = models.CharField(max_length=100)
    class_capacity = models.CharField(max_length=10, choices=CLASS_CAPACITY_CHOICES)
    class_teacher = models.CharField(max_length=100)

    def __str__(self):
        return self.class_name


