from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings

app_name = 'myhealth'
urlpatterns = [
    path('', views.index, name='index'),
    path('ajax_post/', views.ajax_post, name='ajax_post'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
