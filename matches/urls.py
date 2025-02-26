from django.urls import path

from .views import match_list, add_match, delete_match, auto_decide_winner

app_name = 'matches'

urlpatterns = [
    path('', match_list, name='match_list'),
    path('add/', add_match, name='add_match'),
    path('delete/<int:match_id>/', delete_match, name='delete_match'),
    path('match/<int:match_id>/auto-decide-winner/', auto_decide_winner, name='auto_decide_winner'),
]
