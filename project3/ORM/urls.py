from django.urls import path
from django.shortcuts import render 
from . import views
urlpatterns = [
    path('', views.homepage, name='homepage'),

    path('developers/', views.developers_list, name='developers_list'),
    path('developers/create/', views.new_developer, name='new_developer'),
    path('developers/add-skill/', views.add_skill, name='add_skill'),
    path('developers/<int:pk>/', views.developer_skills, name='developer_skills'),

    path('projects/', views.projects_list, name='projects_list'),
    path('projects/create/', views.new_project, name='new_project'),

    path('error/user-not-found/', views.user_not_found, name='user_not_found'),
]
