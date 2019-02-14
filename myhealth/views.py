from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth import logout
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def index(request):
    '''
    log_phd, log_url_phd
    :param request:
    :return:
    '''
    if request.method == "GET":
        if request.user.is_authenticated:
            context = {"log_placeholder": "注销", 'log_url_placeholder': './logout'}
            return render(request, 'myhealth/index.html', context)
        else:
            context = {"log_placeholder": "登录", 'log_url_placeholder': './login'}
            return render(request, 'myhealth/index.html', context)


def register(request):
    if request.method == 'GET':
        user = Register()
        context = {'user': user}
        return render(request, 'myhealth/register.html', {'user': user})
    if request.method == 'POST':
        user = Register(request.POST)
        if user.is_valid():
            try:
                if user.cleaned_data['user_type'] == '1':
                    curr_user = NormalUser.objects.create_user(username=user.cleaned_data['user_name'],
                                                               email=user.cleaned_data['user_email'],
                                                               password=user.cleaned_data['user_password'])
                else:
                    curr_user = DoctorUser.objects.create_user(username=user.cleaned_data['user_name'],
                                                               email=user.cleaned_data['user_email'],
                                                               password=user.cleaned_data['user_password'])
                curr_user = auth.authenticate(request, username=user.cleaned_data['user_name'],
                                              password=user.cleaned_data['user_password'])
                if curr_user is not None:
                    login(request, curr_user)
                    context = {'log_placeholder': '注销'}
                    return render(request, 'myhealth/index.html', context)
            except IntegrityError as e:
                context = {'user': user, 'z_placeholder': '用户名被占用'}
                return render(request, 'myhealth/register.html', context)
    return render(request, 'myhealth/register.html', {'user': user})


def user_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            context = {"log_placeholder": "注销", 'log_url_placeholder': './logout'}
            return HttpResponseRedirect('/myhealth/index', context)
        else:
            return render(request, 'myhealth/login.html', )
    if request.method == 'POST':
        user = Login(request.POST)
        if user.is_valid():
            curr_user = auth.authenticate(username=user.cleaned_data['user_name'],
                                          password=user.cleaned_data['user_password'])
            if curr_user is not None:
                login(request, curr_user)
                context = {"log_placeholder": "注销", 'log_url_placeholder': './logout'}
                return HttpResponseRedirect('/myhealth', context)
        return render(request, 'myhealth/login.html')


@csrf_exempt
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/myhealth')
    else:
        return HttpResponseRedirect('/myhealth')


# def bloghome(request, page_id):
#     '''
#     log_phd, log_url_phd
#     :param request:
#     :param page_id:
#     :return:
#     '''
#
#     pages = []
#     if request.method == 'GET':
#         blog = Bolg.objects.all()[4 * (page_id - 1): 4 * page_id]
#         for b in blog:
#             commonreply = {'author': '', 'date': '', 'reply': ''}
#             common = {'author': '', 'date': '', 'commont': '', 'reply': []}
#             page = {'id': '', 'title': '', 'author_id': '', 'label': '', 'date': '', \
#                     'views': '', 'article': '', 'common': [], 'abstract': ''}
#             page['id'] = b.pk
#             page['title'] = b.title
#             page['author_id'] = User.objects.get(id=b.author_id).username
#             page['label'] = b.label
#             page['date'] = b.date
#             page['views'] = b.views
#             page['article'] = b.article
#
#             for c in BlogCommon.objects.filter(article=b):
#                 common['author'] = c.author
#                 common['date'] = c.date
#                 common['commont'] = c.commont
#                 page['common'].append(common)
#                 i = 0
#                 for r in CommonReply.objects.filter(common=c):
#                     commonreply['author'] = r.author
#                     commonreply['date'] = r.date
#                     commonreply['reply'] = r.reply
#                     page['common'][i]['reply'].append(commonreply)
#                     i += 1
#             page['abstract'] = b.article[:50]
#             pages.append(page)
#
#         if request.user.is_authenticated:
#             context = {'log_placeholder': '注销', 'log_url_placeholder': '../logout', \
#                        'pages': pages, 'page_range': range(page_id, page_id+5), 'page_id': page_id}
#         else:
#             context = {'log_placeholder': '登录', 'log_url_placeholder': '../login', \
#                        'pages': pages, 'page_range': range(page_id, page_id+5), 'page_id': page_id}
#         return render(request, 'myhealth/blog-home.html', context)

def bloghome(request, page_id):
    '''
    log_phd, log_url_phd
    :param request:
    :param page_id:
    :return:
    '''

    pages = []
    if request.method == 'GET':
        blog = Blog.objects.all()[4 * (page_id - 1): 4 * page_id]
        for b in blog:
            page = {'id': '', 'title': '', 'author_id': '', 'label': '', 'date': '', \
                    'views': '', 'article': '', 'abstract': '', 'commonts': ''}
            page['id'] = b.pk
            page['title'] = b.title
            page['author_id'] = User.objects.get(id=b.author_id).username
            page['label'] = b.label
            page['date'] = b.date
            page['views'] = b.views
            page['article'] = b.essay
            page['commonts'] = str(len(list(TopComment.objects.filter(blog=b))))
            page['abstract'] = b.essay[:50]


        if request.user.is_authenticated:
            context = {'log_placeholder': '注销', 'log_url_placeholder': '../logout', \
                       'pages': pages, 'page_range': range(page_id, page_id+5), 'page_id': page_id}
        else:
            context = {'log_placeholder': '登录', 'log_url_placeholder': '../login', \
                       'pages': pages, 'page_range': range(page_id, page_id+5), 'page_id': page_id}
        return render(request, 'myhealth/blog-home.html', context)

def blog(request, blog_id):
    if request.method == 'GET':
        blog = Blog.objects.get(pk=blog_id)
        commonreply = {'author': '', 'date': '', 'reply': ''}
        common = {'author': '', 'date': '', 'commont': '', 'reply': []}
        page = {'title': '', 'author_id': '', 'label': '', 'date': '', \
                'views': '', 'article': '', 'common': [], 'abstract': ''}
        page['title'] = blog.title
        page['author_id'] = User.objects.get(id=blog.author_id).username
        page['label'] = blog.label
        page['date'] = blog.date
        page['views'] = blog.views
        page['article'] = blog.essay
        ck = CKEditorForm()
        if request.user.is_authenticated:
            context = {'log_placeholder': '注销', 'log_url_placeholder': '../logout',
                       'page': page, 'ck':ck}
        return render(request, 'myhealth/blog-details.html', context)