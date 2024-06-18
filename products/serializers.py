from rest_framework import serializers
from .models import Image, Category, Brand, Product, Datasheet, ProductImage, Banner

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['link']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'img']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name', 'img']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude=["slug"]

class DatasheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datasheet
        fields = ['link']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['product','img']

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['product','img']