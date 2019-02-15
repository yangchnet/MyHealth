from django.shortcuts import render
from django.views.generic.list import ListView
from .models import *
from .forms import *
from myhealth.models import *
from django.views.generic.edit import BaseCreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, NoReverseMatch
from django.core.exceptions import PermissionDenied, ImproperlyConfigured


# Create your views here.




class BlogCommentView(ListView):
    '文章评论列表'
    model = BlogComment
    # 前端使用Ajax请求评论数据，故该模板仅包含评论部分
    template_name = 'comment/article_comment.html'
    context_object_name = 'comment_list'
    # 分页，每页10条评论
    paginate_by = 10

    # 筛选目标文章的评论，article_id为url中的参数
    def get_queryset(self):
        return super().get_queryset().filter(article_id=self.kwargs['article_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if context["page_obj"].number == 1 and self.request.user.is_authenticated:
            # 评论的第一页需要提供表单让用户创建新评论
            context['form'] = BlogCommentForm({'article': self.kwargs['article_id']})
        elif context["page_obj"].number == 1:
            # 没有登录的用户需要登录，传article_id是为了在评论中创建url，详细的在模板中解释
            context['article_id'] = self.kwargs['article_id']

        # 计算评论的次序
        first_num = context["paginator"].count - \
                    self.paginate_by * (context["page_obj"].number - 1)
        last_num = first_num - self.paginate_by
        context['comment_list'] = zip(range(first_num, last_num, -1), context['comment_list'])
        return context


class EditArticleCommentMixin():
    '修改文章评论Mixin'

    def render_to_response(self, context, **response_kwargs):
        '禁止get方法和form无效的post'
        raise PermissionDenied

    def form_valid(self, form):
        '保存前设置创建评论的用户'
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        '操作成功后转向文章详情页'
        try:  # POST字典中必须提供文章的id
            url = reverse('blog:detail', kwargs={'pk': self.request.POST['article']})
        except NoReverseMatch:
            raise ImproperlyConfigured('Wrong URL to redirect.')
        return url


class CreateArticleCommentView(LoginRequiredMixin, EditArticleCommentMixin, BaseCreateView):
    '创建一条新的文章评论'
    model = BlogComment
    form_class = BlogCommentForm


class CreateArticleCommentReplyView(CreateArticleCommentView):
    '创建一条新的文章二级评论'
    model = BottomComment
    form_class = BottomCommentForm
