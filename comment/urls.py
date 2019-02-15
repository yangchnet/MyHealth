from django.urls import re_path
from comment.views import BlogCommentView
from . import views

app_name = 'comment'

urlpatterns = [
    re_path(r'^(?P<pk>[0-9]+)/$', views.BlogCommentView.as_view(), name='detail'),
    re_path(r'^(?P<article_id>[0-9]+)/comment/$', BlogCommentView.as_view(), name='article_comment'),
]