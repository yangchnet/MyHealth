from django.contrib import admin
from .models import  *
# Register your models here.
admin.site.register(MhUser)
admin.site.register(Blog)
admin.site.register(NormalUser)
admin.site.register(DoctorUser)
admin.site.register(Data)
admin.site.register(Match)



# admin.site.register(Commont)