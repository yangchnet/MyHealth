from django.db import models
from django.contrib.auth.models import User, AbstractUser
# Create your models here.

class MhUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('normal', '普通用户'),
        ('doctor', '医生')
    )
    usertype = models.CharField(choices=USER_TYPE_CHOICES, default='normal',
                                verbose_name='用户类型', max_length=10)


class NormalUser(models.Model):
    user = models.OneToOneField(MhUser, on_delete=models.CASCADE, primary_key=True)
    age = models.IntegerField(default=0, verbose_name='年龄', null=True, blank=True)
    gender = models.CharField(default='man', choices=(('man', '男'), ('woman', '女')),
                              verbose_name='性别', null=True, blank=True, max_length=10)
    weight = models.FloatField(default=0, verbose_name='体重', null=True, blank=True)
    marry = models.BooleanField(default=False, verbose_name='已婚', null=True, blank=True)
    career = models.CharField(default='', max_length=10, verbose_name='职业', null=True, blank=True)
    signature = models.CharField(default='', max_length=100, verbose_name='个性签名', null=True, blank=True)
    medicalhistory = models.TextField(default='', max_length=1000, verbose_name='用药史', null=True, blank=True)
    avatar = models.ImageField(verbose_name='头像', default=None, null=True, blank=True)

    def __str__(self):
        return self.user.username


class DoctorUser(models.Model):
    user = models.OneToOneField(MhUser, on_delete=models.CASCADE, primary_key=True)
    age = models.IntegerField(default=0, verbose_name='年龄', null=True, blank=True)
    gender = models.CharField(default='man', choices=(('man', '男'), ('woman', '女')),
                              verbose_name='性别', null=True, blank=True, max_length=10)
    signature = models.CharField(default='', max_length=100, verbose_name='个性签名', null=True, blank=True)
    expert = models.CharField(default='', max_length=100, verbose_name='擅长', null=True, blank=True)
    avatar = models.ImageField(verbose_name='头像', default='', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Match(models.Model):
    DATA_TYPE_CHOICES = (
        ('pressure', '血压数据'),
        ('oxygen', '血氧数据'),
        ('heartbeat', '心跳数据'),
        ('tem', '体温数据')
    )
    normaluser = models.ForeignKey(NormalUser, on_delete=models.CASCADE, default='1', verbose_name='普通用户')
    doctor = models.ForeignKey(DoctorUser, on_delete=models.CASCADE, default='1', verbose_name='医生')
    charged = models.CharField(choices=DATA_TYPE_CHOICES,
                               default='heartbeat', verbose_name='医生负责的部分', max_length=20)

class Data(models.Model):
    DATA_TYPE_CHOICES = (
        ('pressure', '血压数据'),
        ('oxygen', '血氧数据'),
        ('heartbeat', '心跳数据'),
        ('tem', '体温数据')
    )
    own = models.ForeignKey(NormalUser, on_delete=models.CASCADE, default='1', verbose_name='条目所有者')
    datatype = models.CharField(choices=DATA_TYPE_CHOICES,
                                default='heartbeat', verbose_name='数据类型', max_length=20)
    doctor = models.ForeignKey(DoctorUser, on_delete=models.CASCADE, default='1', verbose_name='个人医生')
    time = models.DateTimeField(auto_now_add=True, verbose_name='时间')
    value = models.FloatField(default='', verbose_name='具体数值')