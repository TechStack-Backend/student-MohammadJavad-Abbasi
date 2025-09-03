from django.shortcuts import render, HttpResponse

# Create your views here.
def say_my_name(request):
    return HttpResponse("Hello Javad")