from django.shortcuts import render
from .models import Blog
from comment.views import blogcommentview
from comment.forms import CKEditorForm
from blog.forms import  BlogForm
from mhuser.forms import Login
from mhuser.models import *
from bs4 import BeautifulSoup
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.

def bloghome(request, page_id):
    '''
    :param request:
    :param page_id:
    :return:
    '''

    pages = []
    if request.method == 'GET':
        blog = Blog.objects.all()[4 * (page_id - 1): 4 * page_id]
        if request.user.usertype == 'normal':
            profile = NormalUser.objects.get(user=request.user)
        else:
            profile = DoctorUser.objects.get(user=request.user)
        for b in blog:
            page = {'id': '', 'title': '', 'author': '', 'label': '', 'date': '', \
                    'views': '', 'article': '', 'abstract': '', 'cover': ''}
            page['id'] = b.pk
            page['author'] = b.author.username
            page['label'] = b.label
            page['date'] = b.date
            page['views'] = b.views
            page['article'] = b.essay
            soup = BeautifulSoup(b.essay)
            # page['abstract'] = str(soup('p')[0]) + str(soup('p')[1]) + str(soup('p')[2])
            page['abstract'] = str(soup('p')[0])
            pages.append(page)
        if request.user.is_authenticated:
            context = {'pages': pages, 'page_range': range(page_id, page_id + 5),
                       'page_id': page_id, 'page_next': page_id + 1, 'page_pre': page_id - 1, 'profile':profile}
        else:
            context = {'pages': pages, 'page_range': range(page_id, page_id + 5),
                       'page_id': page_id, 'page_next': page_id + 1, 'page_pre': page_id - 1}
        return render(request, 'blog/blog-home.html', context)


def blog(request, blog_id):
    if request.method == 'GET':
        blog = Blog.objects.get(pk=blog_id)
        ck = CKEditorForm()
        comments = blogcommentview(request, blog_id)
        if request.user.is_authenticated:
            context = {'blog': blog, 'ck': ck, 'comments': comments, 'comments_count': len(comments),
                       'blog_id': blog_id}
        else:
            context = {'blog': blog, 'ck': ck, 'comments': comments, 'comments_count': len(comments),
                       'blog_id': blog_id}
        return render(request, 'blog/blog-detail.html', context)

@login_required
def blogwrite(request):
    if request.method == 'GET':
        ck = CKEditorForm()
        return render(request, 'blog/blog-write.html', {'ck':ck})
    else:
        blog = BlogForm(request.POST)
        if blog.is_valid():
            Blog(essay=request.POST['content'], label=request.POST['label']).save()
            return HttpResponseRedirect('/blog/bloghome/1')


