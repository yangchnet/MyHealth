from django.contrib import admin
from .models import  *
# Register your models here.
admin.site.register(NormalUser)
admin.site.register(DoctorUser)
admin.site.register(Blog)
admin.site.register(TopComment)
admin.site.register(BottomComment)
# admin.site.register(Commont)