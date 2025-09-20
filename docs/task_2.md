# Django Views, Templates, and URL Routing

## Q1: What is a view in Django?
Views in django are functions which receive web request and return web response

## Q2: What’s the difference between a function-based view and a class-based view?
Class-based views provide an alternative way to implement views as Python objects instead of functions. They do not replace function-based views, but have certain differences and advantages when compared to function-based views: Organization of code related to specific HTTP methods ( GET , POST , etc.)

## Q3: What arguments does a function-based view typically take, and what does it return?
Each function takes a `request` as an argument and returns an `HttpResponse` object with the appropriate content

## Q4: How can a view return:

   ### o HTML content? 
   ```
    from django.shortcuts import render

    # Create your views here.
    def geeks_view(request):
    
        # render function takes argument  - request
        # and return HTML as response
        return render(request, "home.html")
   ```


   ### o JSON response?
   There are two simple ways to return a JSON response from a Django View. We can either use HttpResponse or JsonResponse classes
   1. JSON response using HttpResponse:
   ``` 
        import json
        from django.http import HttpResponse

        def my_view(request):
            data = {
                'name': 'GeeksForGeeks',
      	        'startedIn': 2009,
                'city': 'Noida'
            }
            response = HttpResponse(json.dumps(data), content_type='application/json')
            return response 
   ```

   2. Using Django's JsonResponse Class:
   ```
   from django.http import JsonResponse

    def my_view(request):
        data = {
            'name': 'GeeksForGeeks',
            'startedIn': 2009,
            'city': 'Noida'
        }
        return JsonResponse(data)
   ```

## Q5: What is HttpResponse vs render()? When do you use each?
HTTPResponse are used for generating raw HTTP responses.

render() are used for rendering HTML templates.

HTTPResponse is useful when you need to return non-HTML content like plain text, file responses, JSON, XML, setting content_type, setting status_code, adding headers,.etc
The arguements for render() are context, content_type, status and 'using' can also be in use.


## Q6: What is the role of templates in Django?
Django's template provides a mini-language for defining the user-facing layer of you application, encouraging seperation of application and presentation logic
A template is a text file. It can generate any text-based format (HTML, XML, CSV, etc.).

A template contains variables, which get replaced with values when the template is evaluated, and tags, which control the logic of the template.


## Q7: How do you create and connect a template to a view?
In the app folder create a folder named templates, inside that folder create another folder with the same name as your app. Now inside this folder you can create your template files.
For connecting your template to the view, inside the views.py, in the function that you want to return that template , use the function render() and pass the path of the template.

``` return render(request, 'path/to/template', other_aruments) ``` 

## Q8: Explain the concept of template context and how variables are passed from the view to the template.
Context is a Python dictionary containing key-value pairs, where keys represent variable names, and values are the data associated with those variables.

``` context = {'key1':'value1', 'key2':'value2'} ```

For passing the variables to the template from the view , first create a dictionary and pass the variable as a value to this dictionary, then pass the dictionary to render() function.

``` return render(request, 'path/to/template', context) ```

For using the variabled in the template use it like this: 

``` {{key1}} ```


## Q9: What are template tags and filters? (How we can dynamically show data that we pass to templates)
Template tags and filters are special syntax elements within Django templates that allow you to perform various operations
Here is an example for dynamically show data in template:
``` 
{% extends './base.html' %}

{% block title %}{{dev.username}}'s profile{% endblock %}

{% block content %}
    <ul>
        <li>Full name: {{dev.first_name}} {{dev.last_name}}</li>
        <li>User name: {{dev.username}}</li>
        <li>Skills:
            <ul> 
                {% for skill in dev.skills %}
                    <li>{{skill}}</li>
                {% endfor %}
            </ul>
        </li>
    </ul>
    <a href="{% url 'developers' %}">Back to developer page</a>
{% endblock %}

```

## Q10: How do you extend templates to avoid repeating HTML code (template inheritance)?
In the template folder create a html file named base.html, in this file write the generic html and for each part that you want to customize in different html files, use appropriate tag
For inheriting the base html file use :
 ``` {% extends 'path/to/base.html' %} ``` 
and add the html code you want in the blocks that is defined in the base.html



## Q11:  What is the role of urls.py in Django?
It routes urls to the views using a list named 'urlpatterns' and functions like path() and include() , so for each url there is an appropriate response


## Q12: What is path()? 
path() is designed to create simple, readable URL patterns. It allows us to define URLs using a more straightforward syntax. With path(), we can use route converters to capture variable parts of the URL.

## Q13:  How do you name a URL pattern, and why is it useful?
We can name a url pattern like this : ``` path('ulr', views.function, name='nameOfThePattern')
It can be helpful when you want to add links to the html file, you can use 
``` {% url 'nameOfThePattern' %} ```
in the href part of the 'a' tag