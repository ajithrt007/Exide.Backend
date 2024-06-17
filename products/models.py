from django.db import models
from django_extensions.db.fields import AutoSlugField

class Image(models.Model):
    link=models.CharField(max_length=50)

class Brand(models.Model):
    slug = AutoSlugField(populate_from=['name'],max_length=50)
    name = models.CharField(max_length=35)
    img=models.ForeignKey(Image,on_delete=models.CASCADE)
    
class Category(models.Model):
    name = models.CharField(max_length=35)
    img=models.ForeignKey(Image,on_delete=models.CASCADE)

class Product(models.Model):
    slug = AutoSlugField(populate_from=['name'],max_length=50)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    features=models.CharField(max_length=500)
    name = models.CharField(max_length=35)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    top_featured=models.BooleanField()
    datasheet=models.CharField(max_length=50)

class Banner(models.Model):
    product=models.ForeignKey(Product,models.SET_NULL,blank=True,null=True)
    img=models.ForeignKey(Image,on_delete=models.CASCADE)

class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    img=models.ForeignKey(Image,on_delete=models.CASCADE)