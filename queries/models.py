from django.db import models

class Query(models.Model):
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=35)
    ph_no=models.CharField(max_length=15,default="")
    subject=models.CharField(max_length=100)
    msg=models.CharField(max_length=600,default="")
    timestamp=models.DateTimeField()
    answered=models.BooleanField(default=False)