from django.contrib import admin
from .models import NormalUser, DoctorUser, Match, MhUser, Data
# Register your models here.
admin.site.register(NormalUser)
admin.site.register(DoctorUser)
admin.site.register(Match)
admin.site.register(MhUser)
admin.site.register(Data)