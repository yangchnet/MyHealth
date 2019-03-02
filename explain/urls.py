from django.urls import path
from . import views

app_name = 'explain'

urlpatterns = [
    path('addexplain/<path:path>/', views.addexplain, name='addexplain'),

]
