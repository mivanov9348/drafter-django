from django.urls import path
from .views import brand_list

urlpatterns = [
    path('', brand_list, name='brand_list'),
]
