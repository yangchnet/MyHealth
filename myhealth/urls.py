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
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
