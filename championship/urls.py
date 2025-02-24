from django.urls import path
from . import views

app_name = 'championships'

urlpatterns = [
    path('', views.championship_list, name='championship_list'),
    path('add/', views.add_championship, name='add_championship'),
]