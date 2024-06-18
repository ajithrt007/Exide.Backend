from django.urls import path
from .views import addCategory, addBrand, getBrands, getCategories, addProduct, getProductsNames, addBanner

urlpatterns =[
    path('addCategory/',addCategory,name='add_category'),
    path('addBrand/',addBrand,name='add_Brand'),
    path('addProduct/',addProduct,name='add_Product'),
    path('addBanner/',addBanner,name='add_Banner'),
    path('getCategories/',getCategories,name='get_Categories'),
    path('getBrands/',getBrands,name='get_Brands'),
    path('getProductsNames/',getProductsNames,name='get_ProductsNames'),
]