from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings

app_name = 'myhealth'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('bloghome/<int:page_id>/', views.bloghome, name='bloghome'),
    path('blog/<int:blog_id>/', views.blog, name='blog'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctor/<int:doctor_id>/', views.doctor, name='doctor'),
    path('devices/', views.devices, name='devices'),
    path('device/<int:device_id>/', views.device, name='device'),
    path('individual/<int:user_id>/', views.individual, name='individual'),
    path('individual/<int:user_id>/heartbeat/', views.heartbeat, name='heartbeat'),
    path('ajax_post/', views.ajax_post, name='ajax_post'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
