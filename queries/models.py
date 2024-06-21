from django.db import models

class Query(models.Model):
    name=models.CharField(max_length=75)
    email=models.CharField(max_length=50)
    ph_no=models.CharField(max_length=15,default="")
    subject=models.CharField(max_length=150)
    msg=models.CharField(max_length=1000,default="")
    timestamp=models.DateTimeField()
    answered=models.BooleanField(default=False)