from django.urls import path
from .views import wrestler_list

urlpatterns = [
    path('', wrestler_list, name='wrestler_list'),
]
