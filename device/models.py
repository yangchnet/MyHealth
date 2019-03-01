from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.
class Device(models.Model):
    name = models.CharField(default='', max_length=30, verbose_name='品名')
    cover1 = models.ImageField(upload_to='device/Cover',  default=None)
    cover2 = models.ImageField(upload_to='device/Cover',  default=None, null=True, blank=True)
    cover3 = models.ImageField(upload_to='device/Cover',  default=None, null=True, blank=True)
    cover4 = models.ImageField(upload_to='device/Cover',  default=None, null=True, blank=True)
    cover5 = models.ImageField(upload_to='device/Cover',  default=None, null=True, blank=True)
    label = models.TextField(default='', max_length=50, verbose_name='标签')
    sales = models.IntegerField(default=0, verbose_name='销量')
    price = models.FloatField(default=0.0, verbose_name='价格')
    detailimage1 = models.ImageField(upload_to='device/detailimage',  default=None, null=True, blank=True)
    detailimage2 = models.ImageField(upload_to='device/detailimage', default=None, null=True, blank=True)
    detailimage3 = models.ImageField(upload_to='device/detailimage', default=None, null=True, blank=True)
    detailimage4 = models.ImageField(upload_to='device/detailimage',  default=None, null=True, blank=True)
    detailimage5 = models.ImageField(upload_to='device/detailimage', default=None, null=True, blank=True)
