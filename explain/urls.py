from django.urls import path
from . import views

app_name = 'explain'

urlpatterns = [
    path('addexplain/<str:own>/<str:type>', views.addexplain, name='addexplain'),
]
