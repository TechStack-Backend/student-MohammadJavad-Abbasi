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

def homepage(request):
    return render(request, 'crud/index.html')


class DevelopersList(LoginRequiredMixin, ListView):
    model = models.Developer
    template_name = 'crud/developers_list.html'
    context_object_name = 'Developers'
    
    


class DeveloperSkills(LoginRequiredMixin, DetailView):
    model = models.Developer
    template_name = 'crud/developer_skills.html'
    context_object_name = 'dev'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skills'] = self.object.skill_set.all()
        return context
    
    
class NewDeveloper(LoginRequiredMixin, CreateView):
    model = models.Developer
    form_class = forms.DeveloperForm
    template_name = 'crud/new_developer.html'
    success_url = reverse_lazy("developers_list")



class UpdateDeveloper(LoginRequiredMixin, UpdateView):
    model = models.Developer
    form_class = forms.DeveloperForm
    template_name = 'crud/update_developer.html'
    success_url = reverse_lazy("developers_list")


class DeleteDeveloper(LoginRequiredMixin, DeleteView):
    model = models.Developer
    template_name = 'crud/delete_developer.html'
    success_url = reverse_lazy('developers_list')


class AddSkill(LoginRequiredMixin, CreateView):
    model = models.Skill
    form_class = forms.SkillForm
    template_name = 'crud/add_skill.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        dev_id = self.kwargs.get('dev_id')
        if dev_id:
            if 'developer' in form.fields:
                del form.fields['developer']
        return form

    def form_valid(self, form):
        dev_id = self.kwargs.get('dev_id')
        
        if dev_id:
            developer = models.Developer.objects.get(id = dev_id)
            skill = form.save(commit=False)
            skill.developer = developer
            skill.save()
        else:
            form.save()

        return super().form_valid(form)
    
    def get_success_url(self):
        dev_id = self.object.developer.id
        return reverse_lazy('developer_skills', kwargs={'pk':dev_id})

class UpdateSkill(LoginRequiredMixin, UpdateView):
    model = models.Skill
    form_class = forms.SkillForm
    template_name = 'crud/update_skill.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'developer' in form.fields:
            del form.fields['developer']
        return form
    
    def get_success_url(self):
        dev = self.object.developer
        dev_id = dev.id
        return reverse_lazy('developer_skills', kwargs={'pk': dev_id})


class DeleteSkill(LoginRequiredMixin, DeleteView):
    model = models.Skill
    template_name = 'crud/delete_skill.html'
    def get_success_url(self):
        dev_id = self.object.developer_id
        return reverse_lazy('developer_skills', kwargs={'pk':dev_id})
    
class ProjectsList(LoginRequiredMixin, ListView):
    model = models.Project
    template_name = 'crud/projects_list.html'
    context_object_name = 'projects'

class NewProject(LoginRequiredMixin, CreateView):
    model = models.Project
    form_class = forms.ProjectForm
    template_name = 'crud/new_project.html'
    success_url = reverse_lazy('projects_list')


class UpdateProject(LoginRequiredMixin, UpdateView):
    model = models.Project
    form_class = forms.ProjectForm
    template_name = 'crud/update_project.html'
    success_url = reverse_lazy('projects_list')


class DeleteProject(LoginRequiredMixin, DeleteView):
    model = models.Project
    template_name = 'crud/delete_project.html'
    success_url = reverse_lazy('projects_list')
    

class NewUser(CreateView):
    model = User
    form_class = forms.UserForm
    template_name = 'crud/new_user.html'
    success_url = reverse_lazy('login')

class LoginUser(LoginView):
    template_name = 'crud/login.html'
    form_class = forms.LoginForm
    redirect_authenticated_user = True
    next_page = reverse_lazy('dashboard')

class ConfirmLogout(View):
    def get(self, request):
        return render(request, 'crud/logout.html')

class LogoutUser(LogoutView):
    next_page = reverse_lazy('homepage')


class UpdateUserProfile(LoginRequiredMixin, View):

    template_name = 'crud/update_profile.html'
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
    template_name = 'crud/dashboard.html'