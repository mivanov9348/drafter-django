from django.urls import path
from .views import brand_list, brand_create, delete_brand

app_name ='brand'

urlpatterns = [
    path('brands/', brand_list, name='brand_list'),
    path('brands/create/', brand_create, name='brand_create'),
    path('delete/<int:brand_id>/', delete_brand, name='brand_delete'),

]
