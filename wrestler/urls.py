from django.urls import path
from wrestler.views import all_wrestlers

app_name = 'wrestler'

urlpatterns = [
    path('wrestlers/', all_wrestlers, name='wrestlers'),
]
