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
        default='none'
    )

    cv = models.FileField(upload_to='cvs/%Y-%m-%d/')
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    phone = models.IntegerField()
    dob= models.DateField()
    address = models.CharField(max_length=255)
    email = models.EmailField()
    jobID = models.ForeignKey('job', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='none')
    username = models.CharField(max_length=30, null=True, blank=True)
    password = models.CharField(max_length=30, null=True, blank=True) 
    age = models.IntegerField(default=0) 
    Note = models.TextField(null=True, blank=True) 
    To_Candidate = models.TextField(null=True, blank=True)
    
    """def title():
        ID= candidate.jobID
        JOB=job.objects.get(jobID=ID)
        """
    
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
    LEVEL_CHOICES = [
        ('Entry', 'Entry'),
        ('Mid', 'Mid'),
        ('Senior', 'Senior'),
    ]
    
    WORK_ARRANGEMENT_CHOICES = [
        ('Office', 'Office'),
        ('Hybrid', 'Hybrid'),
        ('Remote', 'Remote'),
    ]
    
    LOCATION_CHOICES = [
        ('Cairo', 'Cairo'),
        ('Giza', 'Giza'),
        ('Alexandria', 'Alexandria'),
    ]
    jobID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    depName = models.CharField(max_length=100, null=True, blank=True)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='Entry')
    description = models.TextField(null=True, blank=True)
    applicants_count = models.PositiveIntegerField(default=0)
    years_of_experience = models.PositiveIntegerField(default=0)
    work_arrangement = models.CharField(max_length=10, choices=WORK_ARRANGEMENT_CHOICES, default='Office')
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES, default='Cairo')
    salary = models.PositiveIntegerField(null=True, blank=True)
    depID = models.ForeignKey('department', on_delete=models.CASCADE)
    HR_code = models.ForeignKey('human_resources', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=datetime.now, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'job'



class background_images(models.Model):
    homepage = models.URLField(max_length=255,  null=True, blank=True)
    jobs = models.URLField(max_length=255,  null=True, blank=True)
    application = models.URLField(max_length=255,  null=True, blank=True)
    thank_you = models.URLField(max_length=255,  null=True, blank=True)
    logout = models.URLField(max_length=255,  null=True, blank=True)
    login = models.URLField(max_length=255,  null=True, blank=True)
    account = models.URLField(max_length=255,  null=True, blank=True)

    class Meta:
        db_table = 'background_images'
        

class resume(models.Model):
    University= models.TextField()
    Major= models.TextField()
    Education =models.TextField()
    LinkedIn=models.URLField()
    Work_Experience=models.TextField()
    SoftSkill=models.TextField()
    TechSkill=models.TextField()
    AddNote=models.TextField()
    pdf_file=models.URLField()
    ExtraCurricular=models.TextField(default='none')
    
    """def __str__(self):
        return self.full_name"""
    
    class Meta:
        db_table = 'resume'
    
    
    
    