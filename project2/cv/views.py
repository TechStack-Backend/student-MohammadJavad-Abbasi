from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib import messages

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

developersDict = {dev['username'] : dev for dev in developersList}




def homepage(request):
    return render(request, 'cv/index.html')


def developers(request):
    
    context = {'Developers' : developersList}
    return render(request, 'cv/developers.html', context)


def developer_cv(request, name):
    
    dev = developersDict.get(name)
    
    if not dev:
        messages.add_message(request, messages.ERROR, 'Developer not found!')
    
    context = {'dev':dev}
    return render(request, 'cv/CVs.html', context)
