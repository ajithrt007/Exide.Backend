from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import os
from django.conf import settings
from .serializers import ImageSerializer, CategorySerializer, BrandSerializer, ProductSerializer, DatasheetSerializer, ProductImageSerializer, BannerSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Brand, Product
from .helpers import remove_special_characters

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

    filtered_category_name=remove_special_characters(category_name)
    image_name='_'.join(filtered_category_name.split(' ')) + '.' + image.name.split('.')[-1]

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
        'img': image_instance.id
    }

    print(category_data)

    category_serializer = CategorySerializer(data=category_data)

    if category_serializer.is_valid():
        category_serializer.save()
        return Response({'message': 'Category created successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    filtered_brand_name=remove_special_characters(brand_name)
    image_name='_'.join(filtered_brand_name.split(' ')) + '.' + image.name.split('.')[-1]

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
        'img': image_instance.id
    }

    brand_serializer = BrandSerializer(data=brand_data)

    if brand_serializer.is_valid():
        brand_serializer.save()
        return Response({'message': 'Brand created successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response(brand_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addProduct(request):
    product_name=request.data.get('product_name')
    product_features=request.data.get('product_features')
    quantity=int(request.data.get('product_quantity'))
    top_featured= True if request.data.get('top_featured') == 'true' else False
    category_id=int(request.data.get('product_category_id'))
    brand_id=int(request.data.get('product_brand_id'))
    datasheet=request.data.get('product_datasheet')
    images = request.FILES.getlist('product_images')

    if Product.objects.filter(name=product_name).exists():
        return Response("Product with same name already exists in database", status=status.HTTP_400_BAD_REQUEST)

    if not datasheet:
        return Response("Datasheet is empty.",status=status.HTTP_400_BAD_REQUEST)
    
    filtered_product_name=remove_special_characters(product_name)
    pdf_name=f"{'_'.join(filtered_product_name.split(' '))}.pdf"

    datasheets_dir=os.path.join(settings.MEDIA_ROOT,'datasheets')
    if not os.path.exists(datasheets_dir):
        os.makedirs(datasheets_dir)    

    with open(os.path.join(datasheets_dir,pdf_name),'wb+') as destination:
        for chunk in datasheet.chunks():
            destination.write(chunk)

    datasheet_serializer = DatasheetSerializer(data={'link': pdf_name})

    if not datasheet_serializer.is_valid():
        return Response(datasheet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    datasheet_instance=datasheet_serializer.save()
    datasheet_id=datasheet_instance.id

    product_data={
        "name": product_name,
        "features": product_features,
        "brand": brand_id,
        "category": category_id,
        "quantity": quantity,
        "top_featured": top_featured,
        "datasheet": datasheet_id
    }

    product_serialzier=ProductSerializer(data=product_data)

    if not images:
        return Response("Images are empty.",status=status.HTTP_400_BAD_REQUEST)
    
    if not product_serialzier.is_valid():
        return Response(product_serialzier.errors, status=status.HTTP_400_BAD_REQUEST)

    product_instance=product_serialzier.save()
    product_id=product_instance.id

    slugValue=product_instance.slug

    products_dir=os.path.join(settings.MEDIA_ROOT,'products')
    if not os.path.exists(products_dir):
        os.makedirs(products_dir)    

    i=0
    for image in images:
        print(image.name,image.size,image.content_type)
        image_name=f"{slugValue}_{i}.{image.name.split('.')[-1]}"

        with open(os.path.join(products_dir,image_name),'wb+') as destination:
            for chunk in datasheet.chunks():
                destination.write(chunk)

        image_serializer = ImageSerializer(data={'link': image_name})

        if not image_serializer.is_valid():
            return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        image_instance = image_serializer.save()

        product_image_serializer=ProductImageSerializer(data={
            'product': product_id,
            'img': image_instance.id
        })

        if not product_image_serializer.is_valid():
            return Response(product_image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        product_image_serializer.save()
        i+=1    
    
    return Response({'message': 'Product created successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addBanner(request):
    image = request.data.get('banner_image')
    product_id=int(request.data.get('product_id'))

    if not image:
        return Response("Image not found", status=status.HTTP_400_BAD_REQUEST)

    banner_dir= os.path.join(settings.MEDIA_ROOT,'banners')
    if not os.path.exists(banner_dir):
        os.makedirs(banner_dir)
    
    image_name= f"{product_id}Banner.{image.name.split('.')[-1]}"

    with open(os.path.join(banner_dir,image_name), 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)

    image_serializer = ImageSerializer(data={'link': image_name})

    if image_serializer.is_valid():
        image_instance = image_serializer.save()
    else:
        return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    banner_data = {
        'product': product_id,
        'img': image_instance.id
    }

    banner_serializer = BannerSerializer(data=banner_data)

    if banner_serializer.is_valid():
        banner_serializer.save()
        return Response({'message': 'Brand created successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response(banner_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCategories(request):
    categories=list(Category.objects.values())
    return Response(categories, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBrands(request):
    brands=list(Brand.objects.values())
    return Response(brands, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProductsNames(request):
    products=list(Product.objects.values('id','name'))
    return Response(products, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProducts(request):
    products=list(Product.objects.values('id','name'))
    return Response(products, status=status.HTTP_200_OK)
    
        