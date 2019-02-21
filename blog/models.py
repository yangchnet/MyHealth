from django.db import models
from mhuser.models import MhUser
from ckeditor.fields import RichTextField
# Create your models here.

class Blog(models.Model):
    author = models.ForeignKey(MhUser, on_delete=models.CASCADE, default=1,
                               related_name='+', verbose_name='作者')
    essay = RichTextField(verbose_name='正文')
    date = models.DateTimeField(auto_now_add=True)
    label = models.CharField(default='', max_length=20, verbose_name='标签')
    views = models.IntegerField(default=0, verbose_name='观看次数')
    class Meta:
        ordering = ['-date']
    # cover = models.ImageField(verbose_name='封面', default='', null=True, blank=True)


