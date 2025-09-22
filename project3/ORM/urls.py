from django.urls import path
from django.shortcuts import render 
from . import views
urlpatterns = [
    path('', views.homepage, name='homepage'),

    path('developers-list', views.developers_list, name='developers_list'),
    path('developers-list/<str:pk>/', views.developer_skills, name='developer_skills'),
    path('create-developer', views.new_developer, name='new_developer'),
    path('add-skill', views.add_skill, name='add_skill'),

    path('projects-list', views.projects_list, name='projects_list'),
    path('create-project', views.new_project, name='new_project'),

    path('error/user-not-found', views.user_not_found, name='user_not_found'),
]
