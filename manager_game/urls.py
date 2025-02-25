from django.urls import path
from . import views

app_name = 'manager_game'

urlpatterns = [
    path('', views.game_redirect, name='game_redirect'),
    path('start/', views.start_game, name='start_game'),
    path('<int:game_id>/', views.game_dashboard, name='game_dashboard'),
    path('<int:game_id>/ppv/<int:ppv_id>/simulate/', views.simulate_ppv, name='simulate_ppv'),
]