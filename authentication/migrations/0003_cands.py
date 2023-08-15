# Generated by Django 4.2.4 on 2023-08-15 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_candaccount_delete_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='cands',
            fields=[
                ('cand_status', models.CharField(choices=[('reviewed', 'Reviewed'), ('rejected', 'Rejected'), ('accepted', 'Accepted'), ('on stack', 'On Stack')], default='reviewed', max_length=10)),
                ('CandID', models.AutoField(primary_key=True, serialize=False)),
                ('cv', models.FileField(upload_to='')),
                ('fname', models.CharField(max_length=30)),
                ('age', models.IntegerField()),
                ('phone', models.IntegerField()),
                ('dob', models.DateField()),
                ('address', models.CharField(max_length=255)),
                ('military_status', models.CharField(choices=[('completed', 'Completed'), ('not completed', 'Not Completed'), ('exempted', 'Exempted')], default='not completed', max_length=15)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=6)),
            ],
            options={
                'db_table': 'cands',
            },
        ),
    ]