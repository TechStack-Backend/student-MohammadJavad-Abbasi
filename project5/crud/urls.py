from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

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

    path('user/signup/', views.NewUser.as_view(), name='signup'),
    path('user/login/', views.LoginUser.as_view(), name='login'),
    path('user/logout-confirm/', views.ConfirmLogout.as_view(), name='confirm_logout'),
    path('user/logout/', views.LogoutUser.as_view(), name='logout'),
    path('user/profile/edit', views.UpdateUserProfile.as_view(), name='update_profile'),
    path('user/dashboard', views.Dashboard.as_view(), name='dashboard'),

    path('user/reset-password/',
        auth_views.PasswordResetView.as_view(
            template_name='crud/password_reset.html',
            email_template_name='crud/password_reset_email.html',
            subject_template_name='crud/password_reset_subject.txt',
            success_url='/user/reset-password/done/'
        ),
        name='user/password_reset'),

    
    path('user/reset-password/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='crud/password_reset_done.html'
        ),
        name='user/password_reset_done'),

    
    path('user/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='crud/password_reset_confirm.html',
            success_url='/user/reset/complete/'
        ),
        name='password_reset_confirm'),

    
    path('user/reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='crud/password_reset_complete.html'
        ),
        name='password_reset_complete'),
]
