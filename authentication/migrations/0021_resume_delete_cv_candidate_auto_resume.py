# Generated by Django 4.2.4 on 2023-09-09 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0020_merge_20230909_1223'),
    ]

    operations = [
        migrations.CreateModel(
            name='resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('University', models.TextField()),
                ('Major', models.TextField()),
                ('Education', models.TextField()),
                ('LinkedIn', models.URLField()),
                ('Work_Experience', models.TextField()),
                ('SoftSkill', models.TextField()),
                ('TechSkill', models.TextField()),
                ('AddNote', models.TextField()),
                ('pdf_file', models.URLField()),
                ('ExtraCurricular', models.TextField(default='none')),
            ],
            options={
                'db_table': 'resume',
            },
        ),
        migrations.DeleteModel(
            name='CV',
        ),
        migrations.AddField(
            model_name='candidate',
            name='auto_resume',
            field=models.FileField(blank=True, null=True, upload_to='resumes/%Y-%m-%d/'),
        ),
    ]
