# Generated by Django 5.2.1 on 2025-06-18 13:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_registerschoolstaff_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='event_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
