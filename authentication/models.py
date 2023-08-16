from django.db import models
from datetime import datetime

# Create your models here.

class candidate(models.Model):
    candID = models.AutoField(primary_key=True)

    STATUS_CHOICES = [
        ('reviewed', 'Reviewed'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
        ('on stack', 'On Stack'),
    ]

    MILITARY_STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('not completed', 'Not Completed'),
        ('exempted', 'Exempted'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    cand_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='reviewed'
    )
    
    military_status = models.CharField(
        max_length=15,
        choices=MILITARY_STATUS_CHOICES,
        default='not completed'
    )
    
    gender = models.CharField(
        max_length=6,
        choices=GENDER_CHOICES,
        default='male'
    )

    cv = models.FileField(upload_to='cvs/%Y-%m-%d/')
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    phone = models.IntegerField()
    dob= models.DateField()
    address = models.CharField(max_length=255)
    email = models.EmailField()
    jobID = models.ForeignKey('job', on_delete=models.CASCADE)    
    
    def age(self):
        return int((datetime.now().date() - self.dob).days / 365.25)   

    class Meta:
        db_table = 'candidate'

class candidate_account(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    candID = models.ForeignKey('candidate', on_delete=models.CASCADE)

    class Meta:
        db_table = 'candidate_account'


class human_resources(models.Model):
    HR_code = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    class Meta:
        db_table = 'human_resources'


class department(models.Model):
    depID = models.AutoField(primary_key=True)
    depName = models.CharField(max_length=30)

    class Meta:
        db_table = 'department'


class job(models.Model):
    jobID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
    depID = models.ForeignKey('department', on_delete=models.CASCADE)
    HR_code = models.ForeignKey('human_resources', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'job'