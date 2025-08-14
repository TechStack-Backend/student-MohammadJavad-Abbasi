from django.urls import path
from . import views

urlpatterns = [
    path('', views.say_my_name, name='test')
]