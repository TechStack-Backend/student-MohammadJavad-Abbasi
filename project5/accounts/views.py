from django.shortcuts import render, HttpResponse, redirect
from . import models, forms
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.auth.mixins import LoginRequiredMixin


class NewUser(CreateView):
    model = User
    form_class = forms.UserForm
    template_name = 'accounts/new_user.html'
    success_url = reverse_lazy('login')

class LoginUser(LoginView):
    template_name = 'accounts/login.html'
    form_class = forms.LoginForm
    redirect_authenticated_user = True
    next_page = reverse_lazy('dashboard')

class ConfirmLogout(View):
    def get(self, request):
        return render(request, 'accounts/logout.html')

class LogoutUser(LogoutView):
    next_page = reverse_lazy('homepage')


class UpdateUserProfile(LoginRequiredMixin, View):

    template_name = 'accounts/update_profile.html'
    success_url = reverse_lazy('dashboard')

    def get(self, request):
        user_form = forms.UserUpdateForm(instance=request.user)
        profile_form = forms.UserProfileForm(instance=request.user.userprofile)
        password_form = PasswordChangeForm(request.user)

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
            'password_form': password_form
        })

    def post(self, request):

        if 'save_all' in request.POST:
            user_form = forms.UserUpdateForm(request.POST, instance=request.user)
            profile_form = forms.UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, "Profile and account info updated.")
                return redirect(self.success_url)
            else:
                messages.error(request, "Fix the errors below.")
                return render(request, self.template_name, {
                    'user_form': user_form,
                    'profile_form': profile_form,
                    'password_form': PasswordChangeForm(request.user)
                })

        if 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password updated.")
                return redirect(self.success_url)

            return render(request, self.template_name, {
                'user_form': forms.UserUpdateForm(instance=request.user),
                'profile_form': forms.UserProfileForm(instance=request.user.userprofile),
                'password_form': password_form
            })


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
