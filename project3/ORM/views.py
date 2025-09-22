from django.shortcuts import render, redirect
from .models import Developer, Project
from .forms import DeveloperForm, ProjectForm, SkillForm
from django.contrib import messages

def homepage(request):
    return render(request, 'ORM/index.html')


def developers_list(request):

    devs = Developer.objects.all()
    context = {'Developers' : devs}
    return render(request, 'ORM/developers_list.html', context)


def developer_skills(request, pk):
    
    try:
        dev = Developer.objects.get(id = pk)
    except Developer.DoesNotExist:
        request.session['error_message'] = "User not found!"
        return redirect('user_not_found')

    skills = dev.skill_set.all()

    context = {'dev':dev, 'skills':skills}
    return render(request, 'ORM/skills.html', context)


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
    
def user_not_found(request):
    error = request.session.get('error_message', None)
    return render(request, 'ORM/user_not_found.html', {'error_message':error})
