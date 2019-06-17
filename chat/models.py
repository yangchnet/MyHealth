from django.db import models
from mhuser.models import NormalUser
# Create your models here.
# class ChatModel(models.Model):
#     sender = models.ForeignKey(NormalUser, on_delete=models.CASCADE, default='1', verbose_name='发送者')
#     receiver = models.ForeignKey(NormalUser, on_delete=models.CASCADE, default='1', verbose_name='接收者')
#     time = models.DateTimeField(auto_now_add=True, verbose_name='时间')
#     content = models.TextField(max_length=1000, verbose_name='对话内容')