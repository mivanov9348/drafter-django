from django.contrib import admin
from django.urls import path, include
from accounts.views import home
from django.conf import settings
from django.conf.urls.static import static

from core.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='home'),
    path('accounts/', include('accounts.urls')),
    path('core/', include('core.urls')),
    path('wrestlers/', include('wrestler.urls')),
    path('brands/', include('brand.urls')),
    path('draft/', include('draft.urls')),
    path('matches/', include('matches.urls')),
    path('tournament/', include('tournament.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

