from django.urls import path
from . import views
urlpatterns = [
    path('', views.homepage, name='homepage'),

    path('developers_list', views.developers_list, name='developers_list'),
    path('developers_list/<str:pk>/', views.developer_skills, name='developer_skills'),
    path('create_developer', views.new_developer, name='new_developer'),
    path('add_skill', views.add_skill, name='add_skill'),

    path('projects_list', views.projects_list, name='projects_list'),
    path('create_project', views.new_project, name='new_project'),


]