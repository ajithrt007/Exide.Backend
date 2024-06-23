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

class ProductsQuerySerializer(serializers.Serializer):
    brand=serializers.CharField(required=False)
    category=serializers.CharField(required=False)
    product_name=serializers.CharField(required=False)
    page_size=serializers.IntegerField(required=False, default=20, max_value=50)
    page_no=serializers.IntegerField(required=False,default=0)


class ProductOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"