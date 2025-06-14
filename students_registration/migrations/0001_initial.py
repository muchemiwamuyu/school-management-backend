# Generated by Django 5.2.1 on 2025-05-22 11:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisterStudents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('parents_email', models.EmailField(max_length=254, unique=True)),
                ('class_name', models.CharField(max_length=100)),
                ('parents_number', models.CharField(max_length=15, unique=True)),
                ('date_of_joining', models.DateField()),
                ('date_of_birth', models.DateField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
