# Generated by Django 4.2.4 on 2023-08-15 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('cl', models.CharField(db_column='class', max_length=10)),
                ('mark', models.IntegerField()),
                ('gender', models.CharField(max_length=6)),
            ],
            options={
                'db_table': 'student',
            },
        ),
    ]
