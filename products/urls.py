from django.urls import path
from .views import addCategory, addBrand, getBrands, getCategories, addProduct, getProductsNames, loadProductData ,updateBanners,  addBanner, loadHomePage , updateBrand , updateCategories ,  updateProducts ,getAllProducts

urlpatterns =[
    path('addCategory/',addCategory,name='add_category'),
    path('addBrand/',addBrand,name='add_Brand'),
    path('addProduct/',addProduct,name='add_Product'),
    path('addBanner/',addBanner,name='add_Banner'),
    path('getCategories/',getCategories,name='get_Categories'),
    path('getBrands/',getBrands,name='get_Brands'),
    path('getProductsNames/',getProductsNames,name='get_ProductsNames'),
    path('loadHomePage/',loadHomePage,name="loadHomePage"),
    path('updateProduct/',updateProducts,name="updateProduct"),
    path('updateBrand/',updateBrand,name="updateBrand"),
    path('updateCategories/',updateCategories,name="updateCategories"),
    path('updateBanners/',updateBanners,name="updateBanners"),
    path('getAllProducts/',getAllProducts,name="getAllProducts"),
    path('loadProductData/',loadProductData,name="loadProductData"),
]