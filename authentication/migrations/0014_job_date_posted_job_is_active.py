# Generated by Django 4.2.4 on 2023-08-21 06:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0013_job_depname_job_level_job_location_job_salary_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='date_posted',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='job',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]