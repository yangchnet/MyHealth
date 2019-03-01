from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'device'

urlpatterns = [
    path('devices/', views.devices, name='devices'),
    path('device/<int:device_id>/', views.device, name='device'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)