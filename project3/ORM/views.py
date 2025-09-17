from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from .models import Developer, Project, Skill
from .forms import DeveloperForm, ProjectForm, SkillForm

def homepage(request):
    return render(request, 'ORM/index.html')


def developers_list(request):

    devs = Developer.objects.all()
    context = {'Developers' : devs}
    return render(request, 'ORM/developers_list.html', context)


def developer_skills(request, pk):
    
    dev = Developer.objects.get(id = pk)
    if dev:
        skills = Skill.objects.all().filter(developer__id = pk)

        context = {'dev' : dev, 'skills' : skills}
        return render(request, 'ORM/skills.html', context)

    raise Http404("Developer not found!")    


def projects_list(request):
    
    projects = Project.objects.all()
    context = {'projects':projects}
    return render(request, 'ORM/projects_list.html', context)


def new_developer(request):
    
    form = DeveloperForm()

    if request.method == 'POST':
        form = DeveloperForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('developers_list')        

    context = {'form':form}
    return render(request, 'ORM/new_developer.html', context)


def new_project(request):
    
    form = ProjectForm()
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('projects_list')

    context = {'form':form}
    return render(request, 'ORM/new_project.html', context)


def add_skill(request):
    
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            
            skill = form.save()
            pk = skill.developer_id
            return redirect(f'developers_list/{pk}')
        
    context = {'form':form}
    return render(request, 'ORM/add_skill.html', context)
    