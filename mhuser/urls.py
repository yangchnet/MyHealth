from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'mhuser'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctor/<int:doctor_id>/', views.doctor, name='doctor'),
    path('profile', views.profile, name='profile'),
    # path('heartbeat/<int:user_id>/', views.heartbeat, name='heartbeat'),
    path('notification/<int:page_id>/', views.notification, name='notification'),
    path('noti/<int:noti_id>/', views.noti, name='noti'),
    path('myclient/', views.myclient, name='myclient'),
    # path('tem/<int:user_id>/', views.tem, name='tem'),
    # path('oxygen/<int:user_id>/', views.oxygen, name='oxygen'),
    # path('pressure/<int:user_id>/', views.pressure, name='pressure'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
