from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('developers', views.developers, name='developers'),
    path('developers/<str:name>/', views.developer_cv, name='developer_cv'),
    
]
