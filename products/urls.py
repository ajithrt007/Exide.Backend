from django.urls import path
from .views import addCategory, addBrand

urlpatterns =[
    path('addCategory/',addCategory,name='add_category'),
    path('addBrand/',addBrand,name='add_Brand')
]