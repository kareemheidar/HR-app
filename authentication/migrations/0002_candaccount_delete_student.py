# Generated by Django 4.2.4 on 2023-08-15 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='candAccount',
            fields=[
                ('candID', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'candAccount',
            },
        ),
        migrations.DeleteModel(
            name='student',
        ),
    ]
