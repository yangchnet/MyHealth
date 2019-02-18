from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from myhealth.models import  Blog, MhUser
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
class BaseComment(models.Model):
    comment = RichTextUploadingField(verbose_name='评论')
    time = models.DateTimeField(auto_now_add=True, verbose_name='时间')
    author = models.ForeignKey(MhUser, on_delete=models.CASCADE, verbose_name='作者')

    class Meta:
        abstract = True


class BlogComment(BaseComment):
    followed_blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='被评论对象')

    class Meta:
        ordering = ['-time']


class BottomComment(BaseComment):
    followed_comment = models.ForeignKey(BlogComment, on_delete=models.CASCADE, verbose_name='被评论对象')
    followed_self = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='评论的评论')

    class Meta:
        ordering = ['time']
