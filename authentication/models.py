from django.db import models

# Create your models here.
class candAccount(models.Model):
    candID = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    class Meta:
        db_table = 'candAccount'




