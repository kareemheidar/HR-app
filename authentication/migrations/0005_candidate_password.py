# Generated by Django 4.2.4 on 2023-08-20 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_candidate_candidate_account_department_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='password',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
