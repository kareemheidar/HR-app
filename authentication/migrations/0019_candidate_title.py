# Generated by Django 4.2.4 on 2023-08-24 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0018_remove_candidate_jobtitle'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='title',
            field=models.CharField(default='none', max_length=100),
        ),
    ]
