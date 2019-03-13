from django.contrib import admin
from .models import NormalUser, DoctorUser, Match, MhUser, TemData, PressureData, OxygenData, HeartData
# Register your models here.
admin.site.register(NormalUser)
admin.site.register(DoctorUser)
admin.site.register(Match)
admin.site.register(MhUser)
admin.site.register(TemData)
admin.site.register(PressureData)
admin.site.register(OxygenData)
admin.site.register(HeartData)

