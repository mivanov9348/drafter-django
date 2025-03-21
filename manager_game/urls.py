from django.urls import path
from . import views
from .views import remove_game

app_name = 'manager_game'

urlpatterns = [
    path('', views.game_redirect, name='game_redirect'),
    path('start/', views.start_game, name='start_game'),
    path('<int:game_id>/', views.game, name='game'),  # Главна страница
    path('<int:game_id>/dashboard/', views.game_dashboard, name='game_dashboard'),  # Dashboard
    path('<int:game_id>/next/', views.next_day, name='next_day'),
    path('<int:game_id>/ppv/<int:ppv_id>/simulate/', views.simulate_ppv, name='simulate_ppv'),
    path('<int:game_id>/remove/', remove_game, name='remove_game'),
    path('<int:game_id>/matches/', views.game_matches, name='game_matches'),
    path('game/<int:game_id>/matches/add/', views.add_match, name='add_match'),
    path('game/<int:game_id>/matches/<int:match_id>/edit/', views.edit_match, name='edit_match'),
    path('<int:game_id>/brands/', views.game_brands, name='game_brands'),
    path('<int:game_id>/power-rankings/', views.power_rankings, name='power_rankings'),
    path('<int:game_id>/championships/', views.championships, name='championships'),
    path('<int:game_id>/options/', views.options, name='options'),
    path('<int:game_id>/edit/', views.edit_game, name='edit_game'),
    path('<int:game_id>/reset/', views.reset_game, name='reset_game'),
    path('<int:game_id>/rivalries/', views.game_rivalries, name='game_rivalries'),
    path('<int:game_id>/rivalries/<int:rivalry_id>/delete/', views.delete_rivalry, name='delete_rivalry'),
    path('<int:game_id>/dashboard/simulate_day/', views.simulate_day, name='simulate_day'),
path('<int:game_id>/next_season/', views.next_season, name='next_season'),
]
