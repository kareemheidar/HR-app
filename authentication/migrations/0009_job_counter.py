# Generated by Django 4.2.4 on 2023-08-20 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_alter_job_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='counter',
            field=models.IntegerField(default=0),
        ),
    ]
