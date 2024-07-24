from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import os
from django.conf import settings
from .serializers import ImageSerializer, CategorySerializer, BrandSerializer, ProductSerializer, DatasheetSerializer, ProductImageSerializer, BannerSerializer, ProductsQuerySerializer,ProductOutputSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Brand, Product, Banner, Image, ProductImage
from .helpers import custom_slugify
from django.db.models import Q
import json


def handle_uploaded_file(file , output):
    with open(output, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

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

    filtered_category_name=custom_slugify(category_name)
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

    filtered_brand_name=custom_slugify(brand_name)
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
    
    filtered_product_name=custom_slugify(product_name)
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
            for chunk in image.chunks():
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

@api_view(['GET'])
def getProductsAll(request):
    products_query_serializer=ProductsQuerySerializer(data=request.query_params)
    if not products_query_serializer.is_valid():
        return Response(products_query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    brand_name=products_query_serializer.validated_data.get('brand')
    if brand_name is not None:
        brand=list(Brand.objects.filter(name=brand_name).values('id'))
        brand_id=brand['id']
        query=Q(brand=brand_id)

    category_name=products_query_serializer.validated_data.get('category')
    if category_name is not None:
        category=list(Category.objects.filter(name=category_name).values('id'))
        category_id=category['id']
        query&=Q(category=category_id)

    search_string=products_query_serializer.validated_data.get('product_name')
    if search_string is not None:
        query&=Q(name__istartswith=search_string)

    try:
        filtered_queryset=Product.objects.filter(query)
    except Exception as  e:
        return Response({'error': str(e)})
    
    page_size=products_query_serializer.validated_data.get('page_size')
    page_no=products_query_serializer.validated_data.get('page_no')
    
    start_index = page_no * page_size
    end_index = start_index + page_size

    try:
        if end_index>filtered_queryset.count():
            paginated_queryset=filtered_queryset[start_index:]
        else:
            paginated_queryset=filtered_queryset[start_index:end_index]
    except IndexError:
        print("List Index out of range")

    response=ProductOutputSerializer(paginated_queryset,many=True)

    return Response({"response": response.data, "count": paginated_queryset.count(), "total": filtered_queryset.count()})

@api_view(['GET'])
def loadHomePage(request):
    banners=list(Banner.objects.all())
    banner_results=[]

    for item in banners:
        slug=list(Product.objects.filter(id=item.product.id).values('slug'))
        img_name=list(Image.objects.filter(id=item.img.id).values('link'))

        img_location=os.path.join(settings.MEDIA_ROOT,"banners",img_name[0]['link'])
        if os.path.exists(img_location):
            # img_path=request.build_absolute_uri(request.get_host()+settings.MEDIA_URL+"banners/"+img_name[0]['link'])
            img_path=request.build_absolute_uri(settings.MEDIA_URL+"banners/"+img_name[0]['link'])
        else:
            img_path=""
        result = {
            "img_path":img_path,
            "linked_product_slug": slug[0]['slug']
        }
        banner_results.append(result)

    brands=list(Brand.objects.all())
    brand_results=[]

    for item in brands:
        img_name=list(Image.objects.filter(id=item.img.id).values('link'))
        img_location=os.path.join(settings.MEDIA_ROOT,"brand",img_name[0]['link'])

        if os.path.exists(img_location):
            # img_path=request.build_absolute_uri(request.get_host()+settings.MEDIA_URL+"brand/"+img_name[0]['link'])
            img_path=request.build_absolute_uri(settings.MEDIA_URL+"brand/"+img_name[0]['link'])
        else:
            img_path=""

        result={
            "name": item.name,
            "img_path": img_path,
        }
        brand_results.append(result)

    products=list(Product.objects.filter(top_featured=True).values('slug','name','id'))
    product_results=[]

    for item in products:
        img_ids=list(ProductImage.objects.filter(product=item['id']).values('img'))
        image_names=[]

        for img_id in img_ids:
            img_name=list(Image.objects.filter(id=img_id['img']).values('link'))
            img_location=os.path.join(settings.MEDIA_ROOT,"products",img_name[0]['link'])

            if os.path.exists(img_location):
                # img_path=request.build_absolute_uri(request.get_host()+settings.MEDIA_URL+"products/"+img_name[0]['link'])
                img_path=request.build_absolute_uri(settings.MEDIA_URL+"products/"+img_name[0]['link'])
            else:
                img_path=""

            image_names.append(img_path)

        result={
            "name": item['name'],
            "slug": item['slug'],
            "img_paths": image_names,
        }
        product_results.append(result)
        
    results={
        "banners": banner_results,
        "brands": brand_results,
        "products": product_results
    }

    return Response(results, status=status.HTTP_200_OK)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def getAllProducts(requesst):
    products  = Product.objects.select_related("image_id").all().values()
   
    catogories = Category.objects.select_related("img")
    banners = Banner.objects.select_related("img__link", "category_id", "brand_id").values("id", "product_id", "product_id__name" , "img_id" , "img_id__link")
    for item in catogories:
        print(item)
    print(catogories)
    catogories = Category.objects.select_related("img").values("id", "name", "img", "img__link")
    print(catogories)
    brands = Brand.objects.select_related("img_id").all().values("id","slug", "name", "img_id" , "img_id__link")
    print(type(products))
    
    data = {
        "products": list(products),
        "catogories": list(catogories),
        "brands": list(brands),
        "banners": list(banners)
    }
    
    # return Response( json.dumps(list(products)) , status = status.HTTP_200_OK)
    return Response( data , status = status.HTTP_200_OK)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def updateProducts(request):
    data = request.POST
    print("the data came in is", data)
    print(request.FILES)
    print(data.get("id"))
    product  = Product.objects.get(id=data.get("id"))
    print("the product to be edited is", product.id, product.name)
    print(product)
    product.name = data.get("product_name")
    # product.slug = data.get("product_slug")
    product.features = data.get("product_features")
    product.brand_id = int(data.get("brand_id"))
    product.category_id = int(data.get("category_id"))

    product.save()

    
    image = request.FILES.get("image")
    if image is not None:
        print("chaning image")
        handle_uploaded_file(image , f"./media/products/{product.slug}_0.png")
        
    

    

    return Response( "" , status = status.HTTP_200_OK)



@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def updateCategories(request):
    data = request.POST
    print("the data is",data)
    cat  = Category.objects.select_related("img").get(id=data.get("id"))
    print(cat)
    cat.name = data.get("category_name")

    image_link = cat.img.link

    print(image_link)

    image = request.FILES.get("image")
    cat.save()
    if image is not None:
        handle_uploaded_file(image , f"./media/category/{image_link}")
    

    

    return Response( "" , status = status.HTTP_200_OK)

@api_view(['POST'])
def updateBanners(request):
    data = request.POST 

    banner = Banner.objects.select_related('img').get( id = data.get('id'))
    banner.product_id = data.get("product_id")

    

    banner.save()
    image = request.FILES.get("image")
    

    if image is not None:
        handle_uploaded_file(image , f"./media/banners/{banner.img.link}")

    return Response( "", status.HTTP_200_OK)

    



@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def updateBrand(request):
    data = request.POST
    print(data)
    brand  = Brand.objects.select_related("img").get(id=data.get("id"))
    print(brand)
    brand.name = data.get("brand_name")
    image_link = brand.img.link
    print(image_link)

    brand.save()

    image = request.FILES.get("image")
    if image is not None:
        handle_uploaded_file(image , f"./media/brand/{image_link}")

    return Response( "" , status = status.HTTP_200_OK)



@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def loadProductData(request):
    print(request.body)
    data = json.loads(request.body).get('data')
    print("the data is ", data)
    product_data = Product.objects.select_related('brand_id', 'category_id').filter(slug = data.get("slug")).values("id", "name", "slug", "features", "brand_id__name", "category_id__name", "category_id")
    print(product_data)

    product_category_id = product_data[0]["category_id"]

    print(product_category_id)

    related_products = Product.objects.filter(category_id = product_category_id).values()
    print(related_products)
    responseData = {
        'product_data': product_data , 
        'related_products': related_products
    }
    

    return Response(  responseData , status = status.HTTP_200_OK)
