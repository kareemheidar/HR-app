from django.db import models

# Create your models here.
class candAccount(models.Model):
    candID = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    class Meta:
        db_table = 'candAccount'



class cands(models.Model):
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
    
    CandID = models.AutoField(primary_key=True)
    cv = models.FileField(upload_to='cvs/%Y-%m-%d/')
    fname = models.CharField(max_length=30)
    phone = models.IntegerField()
    dob= models.DateField()
    address = models.CharField(max_length=255)
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
   # JobID = models.ForeignKey('Job', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'cands'
