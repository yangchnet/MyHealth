from django.contrib import admin
from .models import  *
# Register your models here.
admin.site.register(NormalUser)
admin.site.register(DoctorUser)
admin.site.register(Bolg)
admin.site.register(BlogCommon)
admin.site.register(CommonReply)