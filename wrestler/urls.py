from django.urls import path
from wrestler.views import all_wrestlers, wrestlers_api

app_name = 'wrestler'

urlpatterns = [
    path('wrestlers/', all_wrestlers, name='all_wrestlers'),
    path('api/wrestlers/', wrestlers_api, name='wrestlers_api'),
]
