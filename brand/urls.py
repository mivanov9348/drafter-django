from django.urls import path
from .views import brand_list, brand_create, brand_delete

app_name ='brand'

urlpatterns = [
    path('brands/', brand_list, name='brand_list'),
    path('brands/create/', brand_create, name='brand_create'),
    path('brands/<int:pk>/delete/', brand_delete, name='brand_delete'),

]
