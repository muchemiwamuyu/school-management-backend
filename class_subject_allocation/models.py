from django.db import models

# Create your models here.

class ClassRegistration(models.Model):
    CLASS_CAPACITY_CHOICES = [
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
    ]

    GRADE_LEVEL_CHOICES = [
        ('Grade 1', 'Grade 1'),
        ('Grade 2', 'Grade 2'),
        ('Grade 3', 'Grade 3'),
        ('Grade 4', 'Grade 4'),
        ('Grade 5', 'Grade 5'),
        ('Grade 6', 'Grade 6'),
    ]

    class_name = models.CharField(max_length=100)
    class_capacity = models.CharField(max_length=10, choices=CLASS_CAPACITY_CHOICES)
    class_teacher = models.CharField(max_length=100)
    total_subjects = models.IntegerField(default=0)
    grade_level = models.CharField(max_length=10, default='Grade 1', choices=GRADE_LEVEL_CHOICES)


    def __str__(self):
        return self.class_name
    

class Departments(models.Model):

    department_name = models.CharField(max_length=100)
    department_role = models.CharField(max_length=100)
    dean = models.CharField(max_length=100)

    def __str__(self):
        return self.department_name

