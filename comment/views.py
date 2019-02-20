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
import re
import time
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
# Create your views here.

def blogcommentview(requets, blog_id):
    blog_comment_list = []
    blog_comments = BlogComment.objects.filter(followed_blog_id=blog_id)
    for blog_c in blog_comments:
        comment = {'avatar': None, 'author': '', 'time': '', 'content': '', 'bottom_comments': ''}
        comment['bottom_comments'] = '0'
        # comment['author'] = MhUser.objects.get(id=blog_c.author_id)
        comment['author'] = blog_c.author.username
        comment['time'] = blog_c.time
        comment['content'] = blog_c.comment
        # if blog_c.author.is_superuser == 1:
        #     comment['avatar'] = ''#管理员头像
        # try:
        #     comment['avatar'] = NormalUser.objects.get(user=blog_c.author).avatar
        # except BaseException:
        #     comment['avatar'] = DoctorUser.objects.get(user=blog_c.author).avatar
        blog_comment_list.append(comment)

        for bottom in BottomComment.objects.filter(followed_comment_id=blog_c.id):
            comment = {'author': '', 'time': '', 'content': '', 'bottom_comments': ''}
            comment['bottom_comments'] = '1'
            comment['author'] = bottom.author
            comment['time'] = bottom.time
            comment['content'] = bottom.comment
            # try:
            #     comment['avatar'] = NormalUser.objects.get(user=blog_c.author).avatar
            # except BaseException:
            #     comment['avatar'] = DoctorUser.objects.get(user=blog_c.author).avatar
            blog_comment_list.append(comment)
    return blog_comment_list


@login_required
def addcomment(request, blog_id):
    if request.user.is_authenticated:
        comment = CKEditorForm(request.POST)
        if comment.is_valid():
            soup = BeautifulSoup(comment.cleaned_data['content'])
            if soup('p')[0].text == '#回复：':
                try:
                    parent_comment = BlogComment.objects.get(author=MhUser.objects.get(username=soup('p')[1].text.lower()),
                                                             time=soup('p')[2].text)
                except BaseException:
                    parent_comment = BottomComment.objects.get(author=MhUser.objects.get(username=soup('p')[1].text.lower()),
                                                             time=soup('p')[2].text)
                for i in range(3):
                    soup('p')[0].replace_with('')
                try:
                    BottomComment(followed_comment=parent_comment, author=request.user,
                              comment=soup.text).save()
                except ValueError:
                    BottomComment(followed_self=parent_comment, author=request.user,
                                  comment=soup.text).save()
            else:
                BlogComment(comment=comment.cleaned_data['content'],
                            followed_blog_id=Blog.objects.get(pk=blog_id).id,
                        author_id=request.user.id).save()
    return HttpResponseRedirect(''.join(('/blog/blog/', str(blog_id))))

