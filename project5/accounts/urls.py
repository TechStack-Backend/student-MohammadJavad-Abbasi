from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.NewUser.as_view(), name='signup'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout-confirm/', views.ConfirmLogout.as_view(), name='confirm_logout'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('profile/edit', views.UpdateUserProfile.as_view(), name='update_profile'),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),

    path('reset-password/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html',
            email_template_name='accounts/password_reset_email.html',
            subject_template_name='accounts/password_reset_subject.txt',
            success_url='/user/reset-password/done/'
        ),
        name='password_reset'),

    
    path('reset-password/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ),
        name='password_reset_done'),

    
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html',
            success_url='/user/reset/complete/'
        ),
        name='password_reset_confirm'),

    
    path('reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ),
        name='password_reset_complete'),
]