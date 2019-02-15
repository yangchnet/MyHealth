from django.shortcuts import render
from django.views.generic.list import ListView
from .models import *
from .forms import *
from myhealth.models import *
from django.views.generic.edit import BaseCreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, NoReverseMatch
from django.contrib import auth
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def blogcommentview(requets, blog_id):
    blog_comment_list = []
    blog_comments = BlogComment.objects.filter(followed_blog_id=blog_id)
    for blog_c in blog_comments:
        comment = {'author': '', 'time': '', 'content': '', 'bottom_comments': ''}
        comment['bottom_comments'] = '0'
        comment['author'] = mhUser.objects.get(id=blog_c.author_id)
        comment['time'] = blog_c.time
        comment['content'] = blog_c.comment
        blog_comment_list.append(comment)

        for bottom in BottomComment.objects.filter(followed_comment_id=blog_c.id):
            comment = {'author': '', 'time': '', 'content': '', 'bottom_comments': ''}
            comment['bottom_comments'] = '1'
            comment['author'] = bottom.author
            comment['time'] = bottom.time
            comment['content'] = bottom.comment

            blog_comment_list.append(comment)
    return blog_comment_list

def addcomment(request, blog_id):
    if request.user.is_authenticated:
        comment = CKEditorForm(request.POST)
        if comment.is_valid():

            BlogComment(comment=comment.cleaned_data['content'],
                            followed_blog_id=Blog.objects.get(pk=blog_id).id,
                        author_id=request.user.id).save()
    else:
        return HttpResponseRedirect('/myhealth/login/')
    return HttpResponseRedirect(''.join(('/myhealth/blog/', str(blog_id))))

