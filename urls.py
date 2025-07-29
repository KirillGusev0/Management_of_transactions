
import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from start.views.start import start
from debug.debug_view import debug_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', start, name="bitrix_home"),
    path('deals/', include('deals.urls')),
    path('debug/', debug_view, name='debug'),
    #Task 2
    path('qr/', include('QR.urls', namespace='QR')),
    #Task 3
    path('employees/', include('table_of_employees.urls')),
    #Task 4
    path("map/", include("yandex_map.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)