from django.urls import path
from . import views

app_name = 'championships'

urlpatterns = [
    path('', views.championship_list, name='championship_list'),
    path('add/', views.add_championship, name='add_championship'),
path('edit/<int:championship_id>/', views.edit_championship, name='edit_championship'),
    path('delete/<int:championship_id>/', views.delete_championship, name='delete_championship'),
]