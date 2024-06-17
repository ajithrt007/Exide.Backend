from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import os
from django.conf import settings
from .serializers import ImageSerializer, CategorySerializer, BrandSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Brand

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addCategory(request):
    image = request.data.get('category_image')
    category_name=request.data.get('category_name')

    if Category.objects.filter(name=category_name).exists():
        return Response("Category with same name already exists in database", status=status.HTTP_400_BAD_REQUEST)

    if not image:
        return Response("Image not found", status=status.HTTP_400_BAD_REQUEST)

    brand_dir= os.path.join(settings.MEDIA_ROOT,'category')
    if not os.path.exists(brand_dir):
        os.makedirs(brand_dir)

    image_name='_'.join(category_name.split(' ')) + '.' + image.name.split('.')[1]

    with open(os.path.join(brand_dir,image_name), 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)

    image_serializer = ImageSerializer(data={'link': image_name})

    if image_serializer.is_valid():
        image_instance = image_serializer.save()
    else:
        return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    category_data = {
        'name': category_name,
        'img_id': image_instance.id
    }

    brand_serializer = CategorySerializer(data=category_data)

    if brand_serializer.is_valid():
        brand_serializer.save()
        return Response({'message': 'Category created successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response(brand_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addBrand(request):
    image = request.data.get('brand_image')
    brand_name=request.data.get('brand_name')

    if Brand.objects.filter(name=brand_name).exists():
        return Response("Brand with same name already exists in database", status=status.HTTP_400_BAD_REQUEST)

    if not image:
        return Response("Image not found", status=status.HTTP_400_BAD_REQUEST)

    brand_dir= os.path.join(settings.MEDIA_ROOT,'brand')
    if not os.path.exists(brand_dir):
        os.makedirs(brand_dir)

    image_name='_'.join(brand_name.split(' ')) + '.' + image.name.split('.')[1]

    with open(os.path.join(brand_dir,image_name), 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)

    image_serializer = ImageSerializer(data={'link': image_name})

    if image_serializer.is_valid():
        image_instance = image_serializer.save()
    else:
        return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    brand_data = {
        'name': brand_name,
        'img_id': image_instance.id
    }

    brand_serializer = BrandSerializer(data=brand_data)

    if brand_serializer.is_valid():
        brand_serializer.save()
        return Response({'message': 'Brand created successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response(brand_serializer.errors, status=status.HTTP_400_BAD_REQUEST)