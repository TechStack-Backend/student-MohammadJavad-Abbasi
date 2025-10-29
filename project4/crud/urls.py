
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),

    path('developers/', views.DevelopersList.as_view(), name='developers_list'),
    path('developers/<int:pk>/', views.DeveloperSkills.as_view(), name='developer_skills'),
    path('developers/create/', views.NewDeveloper.as_view(), name='new_developer'),
    path('developers/<int:pk>/update/', views.UpdateDeveloper.as_view(), name='update_developer'),
    path('developers/<int:pk>/delete/', views.DeleteDeveloper.as_view(), name='delete_developer'),

    path('developers/<int:dev_id>/add-skill/', views.AddSkill.as_view(), name='add_skill_dev'),
    path('skills/add-skill/', views.AddSkill.as_view(), name='add_skill'),
    path('skills/<int:pk>/update-skill/', views.UpdateSkill.as_view(), name='update_skill'),
    path('skills/<int:pk>/delete-skill/', views.DeleteSkill.as_view(), name='delete_skill'),


    path('projects/', views.ProjectsList.as_view(), name='projects_list'),
    path('projects/create/', views.NewProject.as_view(), name='new_project'),
    path('projects/<int:pk>/update/', views.UpdateProject.as_view(), name='update_project'),
    path('projects/<int:pk>/delete/', views.DeleteProject.as_view(), name='delete_project'),


    #path('error/user-not-found/', views.user_not_found, name='user_not_found'),
]