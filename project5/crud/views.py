from django.shortcuts import render, HttpResponse, redirect
from . import models, forms
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
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
    

