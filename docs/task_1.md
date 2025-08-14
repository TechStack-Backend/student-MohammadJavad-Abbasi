# General Web Concepts

## Q1: What is a web server ?
### A web server is software running on a physical or virtual machine in the back-end of web applications. Web servers use HTTP/HTTPS to communicate with clients**;** they are constantly listening on ports 443 and 80 for requests from clients and deliver content to them.
### Nginx is a famous web server application. It has various features from basic web server capabilities to advanced features like acting as a proxy server, load balancer, and help to improve the security of web servers, etc.

## Q2: How do a client (browser) and server (backend) communicate?
### Client and server talk to each other based on a structured manner (HTTP/HTTPS).
### First, the client sends an HTTP request to the server.
### When the server receives the request, it processes the request and creates a response, and then sends it back to the client.
### Finally, the client receives the response and renders it.

## Q3: What is HTTP? What happens when you visit a URL?
### HTTP (Hypertext Transfer Protocol) is the protocol or set of rules that clients and servers use to communicate with each other. It defines how messages are formatted and what actions the browser and server need to take based on the methods defined within HTTP.

## Q4: Where does a Django app fit in the network architecture?
### Django is a Python framework for creating back-end web applications. It resides on the server side. After a client’s request reaches the server, the server routes the request to the Django application. The Django application processes the request, generates a response, and then the server sends the response back to the client. The Django application essentially provides the application logic.

## Q5: Understand the following flow and describe what happens at each step: Browser → DNS → Network → Web Server → Django App → Database
### **Browser**: You type the URL, and the browser creates the HTTP request and sends it to the server.
### **DNS**: The browser queries DNS to translate the domain name into an IP address.
### **Network**: The browser sends the request through the network to the server using the obtained IP address.
### **Web Server**: The server receives the request and, if it’s for dynamic content, passes it to the appropriate back-end application (like Django).
### **Django App**: The Django app processes the request, performs the necessary business logic, and prepares a response.
### **Database**: The Django app interacts with the database to perform CRUD (Create, Read, Update, Delete) operations as needed.
### Finally, the response goes back: Database -> Django App -> Web Server -> Network -> Browser. (The database returns data to Django, which formats it into an HTTP response that the web server sends back to the browser.)

# Django and Backend Fundamentals

## Q6
### MVT (Model-View-Template) is a pattern used for developing web applications, and it's a variant of the MVC (Model-View-Controller) pattern, though there are some key distinctions between the two.

#### **Model**: This is the data layer. It defines the structure of the application's data, how it's stored, and the logic associated with that data. It acts as the blueprint for the database schema.

#### **View**: This is the logic layer. It receives HTTP requests from the client (browser), interacts with the Model to fetch or modify data, and then decides which Template to render and what HTTP response to send back to the client. It contains the application's business logic.

#### **Template**: This is the presentation layer. It defines how the data is displayed to the user, typically using HTML. 

### Comparing MVC and MVT:
#### Model: The Model in MVC and MVT are essentially the same.
#### View (in MVC) vs. Template (in MVT): The View in the traditional MVC pattern is primarily concerned with the user interface and presentation. In Django's MVT, this role is done by the Template.
#### Controller (in MVC) vs. View (in MVT): The Controller in MVC is responsible for handling user input, interacting with the Model, and selecting the View to display. In Django's MVT, this is done by the View.

### Core Components in Django:
#### URL: It serves as a router in django. It maps incoming URL requests to specific views.
#### View: Handles the request/response cycle, processes logic, interacts with models, and chooses a template for rendering.
#### Model: Defines the data structure and interacts with the database.
#### Template: Defines the presentation layer for the data.

## Q7: What is a Python virtual environment (virtualenv)? Why is it important in Django or any Python project?
### A venv in python is an isolated folder with a specefic interpreter and packages, seperate from the system's global python installation.
### Importance:
#### Dependency isolation
#### Reproducibility
#### Cleanliness
#### Portability

## Q8: What is the difference between Django REST Framework and Django Templates? Compare their purpose, usage, and when to use each one.
### Django templates:
#### Its purpose is to render HTML pages that are sent directly to the user's browser.
#### Usage: You write html files with special django tags and variables. In djago view, process data and pass that data to a specific template and return a httpresponse.
#### We use it for traditional multi-page web apps or for content-heavy pages or blogs

### Django REST Framework 
#### Its purpose is to build web APIs that allow different apps communicate with each other using JSON or XML.
#### Usage: You You define Serializers which convert complex data types into native Python datatypes that can then be easily rendered into JSON, XML, or other content types.
#### You create APIViews or ViewSets that handle incoming requests, interact with your Models, and return data responses.
#### Clients make HTTP requests to your DRF, and DRF returns data. The client is then responsible for rendering that data.
#### We use it when we wanna build backend API for frontend apps, mobile apps or microservices.


# Hands-On Setup Questions

## Q9: How can we create a simple Django project?
### First create a venv in a folder using this command:

``` python -m venv <folder-name> ```

### Now activate the venv using

``` .\<folder-name>\Scripts\activate ```

### Install django:

``` pip install django ```

### Start a django project:

``` django-admin startproject myproject ```

my_django_projects/
├── venv/                     # Your virtual environment files
├── manage.py                 # A command-line utility to interact with your project
└── myproject/                # The Python package for your project
    ├── __init__.py           # Makes Python treat this directory as a package
    ├── asgi.py               # For serving your project with ASGI-compatible servers
    ├── settings.py           # Project settings and configurations
    ├── urls.py               # Project-level URL declarations
    └── wsgi.py               # For serving your project with WSGI-compatible servers


## Q10: How can we create an app inside a Django project?
### First cd to the project folder and then using 

``` python manage.py startapp myapp ```

### build your app
### Now go to the main app of your project. Inside the settings.py add the name of the newly created app to the INSTALLED_APPS list
### Using urls.py and urlpattern list you can route to your app.