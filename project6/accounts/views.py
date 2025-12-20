from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from . import models, forms
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from crud.models import Developer
from .mixins import SelfOrAdminMixin, UserObjectPermissionMixin

class NewUser(CreateView):
    model = User
    form_class = forms.UserForm
    template_name = 'accounts/new_user.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        self.object = user

        developer_group, _ = Group.objects.get_or_create(name="Developer")
        user.groups.add(developer_group)

        Developer.objects.get_or_create(user=user)

        return HttpResponseRedirect(self.get_success_url())


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

class DeleteAccountConfirmation(LoginRequiredMixin,SelfOrAdminMixin, TemplateView):
    template_name = "accounts/confirm_delete_account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["target_user"] = self.get_target_user()
        return context


class DeleteAccount(LoginRequiredMixin, SelfOrAdminMixin, View):
    def post(self, request, *args, **kwargs):
        target_user = self.get_target_user()

        if target_user == request.user:
            logout(request)
            target_user.delete()
            return redirect("login")

        target_user.delete()
        return redirect("developers_list")


class UpdateUserProfile(LoginRequiredMixin, SelfOrAdminMixin, View):
    template_name = "accounts/update_profile.html"

    def get(self, request, *args, **kwargs):
        target_user = self.get_target_user()

        user_form = forms.UserUpdateForm(instance=target_user)
        profile_form = forms.UserProfileForm(instance=target_user.userprofile)
        password_form = PasswordChangeForm(target_user)

        return render(request, self.template_name, {
            "user_form": user_form,
            "profile_form": profile_form,
            "password_form": password_form,
            "target_user": target_user,
        })

    def get_success_url(self):
        return reverse_lazy(
            "user_profile",
            kwargs={"pk": self.get_target_user().pk}
        )

    def post(self, request, *args, **kwargs):
        target_user = self.get_target_user()

        if "save_all" in request.POST:
            user_form = forms.UserUpdateForm(request.POST, instance=target_user)
            profile_form = forms.UserProfileForm(
                request.POST,
                request.FILES,
                instance=target_user.userprofile
            )

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, "Profile and account info updated.")
                return redirect(self.get_success_url())  # ✅ FIXED

            messages.error(request, "Fix the errors below.")
            return render(request, self.template_name, {
                "user_form": user_form,
                "profile_form": profile_form,
                "password_form": PasswordChangeForm(target_user),
                "target_user": target_user,
            })

        if "change_password" in request.POST:
            password_form = PasswordChangeForm(target_user, request.POST)

            if password_form.is_valid():
                user = password_form.save()

                if target_user == request.user:
                    update_session_auth_hash(request, user)

                messages.success(request, "Password updated.")
                return redirect(self.get_success_url())  # ✅ FIXED

            return render(request, self.template_name, {
                "user_form": forms.UserUpdateForm(instance=target_user),
                "profile_form": forms.UserProfileForm(instance=target_user.userprofile),
                "password_form": password_form,
                "target_user": target_user,
            })



class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
                
        user = self.request.user

        context['developer'] = getattr(user, 'developer', None)
        context['profile'] = getattr(user, 'userprofile', None)

        return context  
    
class ViewProfile(
    LoginRequiredMixin,
    UserObjectPermissionMixin,
    DetailView
):
    model = User
    template_name = "accounts/view_profile.html"
    context_object_name = "profile_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.object
        context["profile"] = getattr(user, "userprofile", None)
        context["developer"] = getattr(user, "developer", None)

        return context