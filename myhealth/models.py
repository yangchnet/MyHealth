from django.db import models
from django.contrib.auth.models import User
import datetime
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class NormalUser(User):
    usertype = models.CharField(default='1', max_length=1)

class DoctorUser(User):
    usertype = models.CharField(default='2', max_length=2)


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    essay = RichTextUploadingField(verbose_name='正文')
    date = models.DateTimeField(default=datetime.datetime.now())
    title = models.CharField(max_length=100, default='', primary_key=True)
    label = models.CharField(default='', max_length=20)
    views = models.IntegerField(default=0)

class BaseComment(models.Model):
    time = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    content = RichTextUploadingField(verbose_name='正文', )

    class Meta:
        abstract = True

class TopComment(BaseComment):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    class Meta:
        ordering = ['-time']

class BottomComment(BaseComment):
    topcomment = models.ForeignKey(TopComment, on_delete=models.CASCADE)



