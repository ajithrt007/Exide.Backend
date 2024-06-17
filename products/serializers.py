from rest_framework import serializers
from .models import Image, Category, Brand

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['link']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'img_id']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name', 'img_id']