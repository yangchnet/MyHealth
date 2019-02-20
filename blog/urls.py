from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('bloghome/<int:page_id>/', views.bloghome, name='bloghome'),
    path('blog/<int:blog_id>/', views.blog, name='blog'),
    path('blogwrite/', views.blogwrite, name='blogwrite'),
]
