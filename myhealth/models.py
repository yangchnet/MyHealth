from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class NormalUser(User):
    usertype = models.CharField(default='1', max_length=1)

class DoctorUser(User):
    usertype = models.CharField(default='2', max_length=2)

class Bolg(models.Model):
    title = models.CharField(max_length=100, default='', primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1, primary_key=True)
    label = models.CharField(default='', max_length=20)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date = models.DateTimeField()
    views = models.IntegerField(default=0)
    article = models.TextField(max_length=10000)

class BlogCommon (models.Model):
    article = models.ForeignKey(Bolg, on_delete=models.CASCADE, default=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date = models.DateTimeField()
    commont = models.TextField(max_length=1000, default='')

class CommonReply(models.Model):
    common = models.ForeignKey(BlogCommon, on_delete=models.CASCADE, default=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date = models.DateTimeField()
    reply = models.TextField(max_length=1000, default='')

