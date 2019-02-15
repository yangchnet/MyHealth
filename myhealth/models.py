from django.db import models
from django.contrib.auth.models import User, AbstractUser
import datetime
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class mhUser(AbstractUser):
    usertype = models.CharField(default='normal', max_length=30,
                                choices=(('normal', '普通用户'), ('doctor', '医生')),
                                verbose_name='用户类型')

class Blog(models.Model):
    author = models.ForeignKey(mhUser, on_delete=models.CASCADE, default=1,
                               related_name='+', verbose_name='作者')
    essay = RichTextUploadingField(verbose_name='正文')
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, default='', primary_key=True, verbose_name='标题')
    label = models.CharField(default='', max_length=20, verbose_name='标签')
    views = models.IntegerField(default=0, verbose_name='观看次数')
    cover = models.ImageField(verbose_name='封面', default='')





