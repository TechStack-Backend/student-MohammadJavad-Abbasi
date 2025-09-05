from django.shortcuts import render
from django.http import HttpResponse, Http404

developersList = [
        {
            "username": "hassan",
            "first_name": "Hassan",
            "last_name": "Kabirian",
            "skills": ["Python", "Django", "Vue.js"],
        },
        {
            "username": "sara",
            "first_name": "Sara",
            "last_name": "Ahmadi",
            "skills": ["JavaScript", "React", "CSS"],
        },
        {
            "username": "ali",
            "first_name": "Ali",
            "last_name": "Rezayi",
            "skills": ["Java", "Spring Boot", "SQL"],
        },
    ]

def homepage(request):
    return render(request, 'cv/index.html')

def developers(request):
    
    context = {'Developers' : developersList}
    return render(request, 'cv/developers.html', context)

def developer_cv(request, name):
    dev = next((d for d in developersList if d['username'] == name), None)
    if not dev:
        raise Http404("Developer not found")
    
    context = {'dev' : dev}
    return render(request, 'cv/CVs.html', context)

    

    