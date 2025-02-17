from django.contrib import admin
from django.urls import path, include
from accounts.views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('core/', include('core.urls')),
    path('wrestlers/', include('wrestler.urls')),
    path('brands/', include('brand.urls')),
    path('draft/', include('draft.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

