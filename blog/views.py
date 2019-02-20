from django.shortcuts import render
from .models import Blog
from comment.views import blogcommentview
from comment.forms import CKEditorForm

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
        for b in blog:
            page = {'id': '', 'title': '', 'author': '', 'label': '', 'date': '', \
                    'views': '', 'article': '', 'abstract': '', 'cover': ''}
            page['id'] = b.pk
            page['title'] = b.title
            page['author'] = b.author.username
            page['label'] = b.label
            page['date'] = b.date
            page['views'] = b.views
            page['article'] = b.essay
            page['abstract'] = b.essay[:50]
            page['cover'] = b.cover
            pages.append(page)
        if request.user.is_authenticated:
            context = {'pages': pages, 'page_range': range(page_id, page_id + 5),
                       'page_id': page_id, 'page_next': page_id + 1, 'page_pre': page_id - 1}
        else:
            context = {'pages': pages, 'page_range': range(page_id, page_id + 5),
                       'page_id': page_id, 'page_next': page_id + 1, 'page_pre': page_id - 1}
        return render(request, 'blog/blog-home.html', context)


def blog(request, blog_id):
    if request.method == 'GET':
        blog = Blog.objects.get(pk=blog_id)
        page = {'title': '', 'author_id': '', 'label': '', 'date': '', \
                'views': '', 'article': '', 'common': [], 'abstract': ''}
        page['title'] = blog.title
        page['author'] = blog.author
        page['label'] = blog.label
        page['date'] = blog.date
        page['views'] = blog.views
        page['article'] = blog.essay
        page['cover'] = blog.cover
        ck = CKEditorForm()
        comments = blogcommentview(request, blog_id)
        if request.user.is_authenticated:
            context = {'page': page, 'ck': ck, 'comments': comments, 'comments_count': len(comments),
                       'blog_id': blog_id}
        else:
            context = {'page': page, 'ck': ck, 'comments': comments, 'comments_count': len(comments),
                       'blog_id': blog_id}
        return render(request, 'blog/blog-detail.html', context)
