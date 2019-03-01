from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'blog'
urlpatterns = [
    path('bloghome/<int:page_id>/', views.bloghome, name='bloghome'),
    path('blog/<int:blog_id>/', views.blog, name='blog'),
    path('blogwrite/', views.blogwrite, name='blogwrite'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

