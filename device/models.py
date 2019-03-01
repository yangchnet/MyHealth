from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.
class Device(models.Model):
    cover1 = ProcessedImageField(upload_to='decice/Cover', processors=[ResizeToFill(300, 200)], format='JPEG',
                                 options={'quality': 200}, default=None)
    cover2 = ProcessedImageField(upload_to='decice/Cover', processors=[ResizeToFill(300, 200)], format='JPEG',
                                 options={'quality': 200}, default=None)
    cover3 = ProcessedImageField(upload_to='decice/Cover', processors=[ResizeToFill(300, 200)], format='JPEG',
                                 options={'quality': 200}, default=None)
    cover4 = ProcessedImageField(upload_to='decice/Cover', processors=[ResizeToFill(300, 200)], format='JPEG',
                                 options={'quality': 200}, default=None)
    cover5 = ProcessedImageField(upload_to='decice/Cover', processors=[ResizeToFill(300, 200)], format='JPEG',
                                 options={'quality': 200}, default=None)
    label = models.TextField(default='', max_length=50, verbose_name='标签')
    sales = models.IntegerField(default=0, verbose_name='销量')
    price = models.FloatField(default=0.0, verbose_name='价格')
    detailimage1 = ProcessedImageField(upload_to='device/detailimage', processors=[ResizeToFill(500, 200)], format='JPEG',
                                 options={'quality': 500}, default=None)
    detailimage2 = ProcessedImageField(upload_to='device/detailimage', processors=[ResizeToFill(500, 200)],
                                       format='JPEG',
                                       options={'quality': 500}, default=None)
    detailimage3 = ProcessedImageField(upload_to='device/detailimage', processors=[ResizeToFill(500, 200)],
                                       format='JPEG',
                                       options={'quality': 500}, default=None)
    detailimage4 = ProcessedImageField(upload_to='device/detailimage', processors=[ResizeToFill(500, 200)],
                                       format='JPEG',
                                       options={'quality': 500}, default=None)
    detailimage5 = ProcessedImageField(upload_to='device/detailimage', processors=[ResizeToFill(500, 200)],
                                       format='JPEG',
                                       options={'quality': 500}, default=None)
