from django.db import models
from mhuser.models import Match, MhUser, NormalUser
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.

class Explain(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, default='')
    author = models.ForeignKey(MhUser, on_delete=models.CASCADE, default='')
    time = models.DateTimeField(auto_now_add=True)
    context = RichTextUploadingField(verbose_name='留言', max_length=10000)
    ######################################################################
    # 兼容Android
    touserid = models.ForeignKey(NormalUser, on_delete=models.CASCADE, default='', null=True, blank=True)
    ######################################################################
    read = models.CharField(default=False, max_length=1)

    class Meta:
        ordering = ['-time']
