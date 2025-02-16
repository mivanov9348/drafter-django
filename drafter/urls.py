from django.contrib import admin
from django.urls import path, include
from accounts.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('core/', include('core.urls')),
    path('wrestlers/', include('wrestler.urls')),
    path('brands/', include('brand.urls')),
]
