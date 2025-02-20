from django.urls import path
from . import views

app_name = 'tournament'

urlpatterns = [
    path('', views.tournaments_list, name='tournaments_list'),
    path('customize/', views.customize_tournament, name='customize_tournament')
]