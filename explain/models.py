from django.db import models
from myhealth.models import *

# Create your models here.

class Explain(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, default='')
    author = models.ForeignKey(MhUser, on_delete=models.CASCADE, default='')
    time = models.DateTimeField(auto_now_add=True)
    context = models.TextField(max_length=300, default='')
