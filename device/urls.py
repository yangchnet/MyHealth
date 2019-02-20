from django.urls import path
from . import views

app_name = 'device'

urlpatterns = [
    path('devices/', views.devices, name='devices'),
    path('device/<int:device_id>/', views.device, name='device'),
]