from django.urls import path
from . import views

app_name = 'mhuser'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctor/<int:doctor_id>/', views.doctor, name='doctor'),
    path('profile', views.profile, name='profile'),
    path('heartbeat', views.heartbeat, name='heartbeat'),
    path('notification/', views.notification, name='notification'),
]
