from django.shortcuts import render, get_object_or_404, redirect
from . import models, forms
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .mixins import OwnerOrPermissionMixin, OwnerAssignMixin, SkillOwnerOrPermissionMixin, SkillObjectOwnerOrPermissionMixin
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied

def homepage(request):
    return render(request, 'crud/index.html')


class DevelopersList(PermissionRequiredMixin, ListView):
    model = models.Developer
    template_name = 'crud/developers_list.html'
    context_object_name = 'Developers'
    permission_required = 'crud.view_developer'
    raise_exception = True
    
class DeveloperSkills(PermissionRequiredMixin, DetailView):
    model = models.Developer
    template_name = 'crud/developer_skills.html'
    context_object_name = 'dev'

    permission_required = 'crud.view_developer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skills'] = self.object.skills.all()
        return context
        
class NewDeveloper(PermissionRequiredMixin, OwnerAssignMixin, CreateView):
    model = models.Developer
    form_class = forms.DeveloperForm
    template_name = 'crud/new_developer.html'
    success_url = reverse_lazy("developers_list")
    permission_required = 'crud.add_developer'

    # instead of assinging the owner using mixin:
    # def form_valid(self, form):
    #     form.instance.owner = self.request.user
    #     return super().form_valid(form)

class UpdateDeveloper(OwnerOrPermissionMixin, UpdateView):
    model = models.Developer
    form_class = forms.DeveloperForm
    template_name = 'crud/update_developer.html'
    success_url = reverse_lazy("developers_list")
    permission_required = 'crud.change_developer'

    owner_field = "user"
    permission_required = "crud.change_developer"
    raise_exception = True

class DeleteDeveloper(OwnerOrPermissionMixin, DeleteView):
    model = models.Developer
    template_name = 'crud/delete_developer.html'
    success_url = reverse_lazy('developers_list')

    owner_field = "user"
    permission_required = "crud.delete_developer"
    raise_exception = True


class AddSkill(LoginRequiredMixin, SkillOwnerOrPermissionMixin, CreateView):
    model = models.Skill
    form_class = forms.SkillForm
    template_name = 'crud/add_skill.html'
    permission_required = "crud.add_skill"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        dev_id = self.kwargs.get('dev_id')
        if dev_id:
            if 'developer' in form.fields:
                del form.fields['developer']
        return form

    def form_valid(self, form):

        if hasattr(self, "developer"):
            form.instance.developer = self.developer
            form.instance.user = self.developer.user

        else:
            dev = form.cleaned_data.get("developer")
            if not dev:
                form.add_error("developer", "Developer is required.")
                return self.form_invalid(form)
            
            form.instance.user = dev.user
        
        return super().form_valid(form)

    
    def get_success_url(self):
        dev_id = self.object.developer.id
        return reverse_lazy('developer_skills', kwargs={'pk':dev_id})

class UpdateSkill(LoginRequiredMixin, SkillObjectOwnerOrPermissionMixin, UpdateView):
    model = models.Skill
    form_class = forms.SkillForm
    template_name = 'crud/update_skill.html'
    permission_required = 'crud.change_skill'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'developer' in form.fields:
            del form.fields['developer']
        return form
    
    def get_success_url(self):
        dev = self.object.developer
        dev_id = dev.id
        return reverse_lazy('developer_skills', kwargs={'pk': dev_id})

class DeleteSkill(LoginRequiredMixin, SkillObjectOwnerOrPermissionMixin, DeleteView):
    model = models.Skill
    template_name = 'crud/delete_skill.html'
    permission_required = 'crud.delete_skill'

    def get_success_url(self):
        dev_id = self.object.developer_id
        return reverse_lazy('developer_skills', kwargs={'pk':dev_id})
    

class ProjectsList(PermissionRequiredMixin, ListView):
    model = models.Project
    template_name = 'crud/projects_list.html'
    context_object_name = 'projects'
    permission_required = 'crud.view_project'

class NewProject(PermissionRequiredMixin, OwnerAssignMixin, CreateView):
    model = models.Project
    form_class = forms.ProjectForm
    template_name = 'crud/new_project.html'
    success_url = reverse_lazy('projects_list')
    permission_required = 'crud.add_project'

class UpdateProject(OwnerOrPermissionMixin, UpdateView):
    model = models.Project
    form_class = forms.ProjectForm
    template_name = 'crud/update_project.html'
    success_url = reverse_lazy('projects_list')

    owner_field = "user"
    permission_required = 'crud.change_project'


class DeleteProject(OwnerOrPermissionMixin, DeleteView):
    model = models.Project
    template_name = 'crud/delete_project.html'
    success_url = reverse_lazy('projects_list')

    owner_field = "user"
    permission_required = 'crud.delete_project'
    
@permission_required('crud.approve_project', raise_exception=True)
def approve_project(request, pk):
    project = get_object_or_404(models.Project, pk=pk)
    
    project.is_approved = not project.is_approved

    project.save()
    return redirect("projects_list")
