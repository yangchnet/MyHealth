from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    path('addcomment/<int:blog_id>', views.addcomment, name='addcomment'),
]
