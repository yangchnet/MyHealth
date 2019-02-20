from django.urls import path
from . import views

app_name = 'mhuser'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctor/<int:doctor_id>/', views.doctor, name='doctor'),
    path('individual/<int:user_id>/', views.individual, name='individual'),
    path('heartbeat/<int:user_id>/', views.heartbeat, name='heartbeat'),
]
