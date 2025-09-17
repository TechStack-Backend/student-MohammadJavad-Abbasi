# Task 3: Django Models, ORM, and Database Relationships

## Datebase:
### What is Relational Database? 
Realational database is a database variant which stores data based on relational algebra (using tables, rows and columns)

## Models and ORM
### Q1: What is a model in Django, and how is it connected to the database?
A model in django is a python class which represents an SQL entity.

The ORM translates your Python model operations into SQL queries.

### Q2: What is the role of migrations in Django?
Migration is Django's way to propagate changes in models into the database schema

### Q3: How do you create a model class in Django? Provide an example.
Inside the app that you want to create your model, go to models.py. Make sure the django.db.models is imported:

`from django.db import models` 

Now create a class with the name of the data that you want to store and inherit from models.Model class. Now create all the attributes for the data that you want to store.

example:

```py
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

```

### Q4: What is the difference between makemigrations and migrate?
makemigrations is responsible for packaging up your model changes into individual migration files - analogous to commits - and migrate is responsible for applying those to your database.

### Q5: What is the Django ORM, and how does it differ from writing raw SQL queries?
Django’s ORM is like a translator. It takes the Python code you write and turns it into SQL queries for you. This means you can work with your database using Python objects, without needing to write complex SQL code.

```py
# Using ORM to get all books by a certain author
 books = Book.objects.filter(author='J.K. Rowling')
```

```py
# Raw SQL for a more complex query 

from django.db import connection 
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM book WHERE author = %s", ['J.K. Rowling']) 
    books = cursor.fetchall()
```

### Q6: How do you perform basic queries with the ORM? For example:
Consider the following class:
```py
class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name
```

#### o Create a new object and save it.
```py
from blog.models import Blog
b = Blog(name="Beatles Blog", tagline="All the latest Beatles news.")
b.save()
```

#### o Retrieve all objects.
```py
all_blogs = Blog.objects.all()
```

#### o Filter objects by a condition.
```py
Blog.objects.filter(name='nameOfTheObject')
```

#### o Update an object.
```py
b.name = "New name"
b.save()
```

#### o Delete an object.
```py
b = Blog.objects.get(pk=1)
b.delete()
```

## Relationships

### Q7: What are the three types of relationships in Django models?
### Q8: Provide an example of when you would use each relationship.
### Q9: How do you define relationships in Django models? Show code snippets.

#### o One-to-One (why not just use one model?)
Each record in Table A is associated with one and only one record in Table B, and vice versa.

To define a one-to-one relationship, use OneToOneField. You use it just like any other Field type: by including it as a class attribute of your model.

Why not just use one model?

In Django:

1. Separation of concerns:
User (authentication) might be a generic reusable model (e.g., django.contrib.auth.User).
Profile is specific to your app’s needs.
Keeps unrelated fields out of the “core” table.

2. Optional relationships:
Some users might not have a profile until later.
This avoid filling the main table with mostly NULL fields.

3. Permissions & modularity:
You can put the Profile model in a different app.
Permissions, queries, and forms can target the profile without touching user auth.

4. Plug‑and‑play flexibility:
Makes it easier to extend third‑party models without modifying their schema.

5. Third‑party compatibility:
You may not own the base model (like Django’s built‑in User) — you extend it via 1:1.

In DBMS:

1. You might want to cluster or partition the two "endpoint" tables of a 1:1 relationship differently.

2. If your DBMS allows it, you might want to put them on different physical disks (e.g. more performance-critical on an SSD and the other on a cheap HDD).

3. You have measured the effect on caching and you want to make sure the "hot" columns are kept in cache, without "cold" columns "polluting" it.

4. You need a concurrency behavior (such as locking) that is "narrower" than the whole row. This is highly DBMS-specific.

5. You need different security on different columns, but your DBMS does not support column-level permissions.

6. Triggers are typically table-specific. While you can theoretically have just one table and have the trigger ignore the "wrong half" of the row, some databases may impose additional limits on what a trigger can and cannot do. For example, Oracle doesn't let you modify the so called "mutating" table from a row-level trigger - by having separate tables, only one of them may be mutating so you can still modify the other from your trigger (but there are other ways to work-around that).


#### o One-to-Many (ForeignKey)
Each record in Table A can be associated with multiple records in Table B, but each record in Table B is associated with only one record in Table A. A ForeignKey is used in Table B to represent the corresponding row in Table A. 

```py
from django.db import models


class Manufacturer(models.Model):
    # ...
    pass


class Car(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    # ...
```

#### o Many-to-Many (what happened in behind)

A Many‑to‑Many (M2M) relationship means:
* Each record in Model A can relate to multiple records in Model B. And each record in Model B can relate to multiple records in Model A.

Behind the scene Django will create a join table or through table.

```py
from django.db import models


class Topping(models.Model):
    # ...
    pass


class Pizza(models.Model):
    # ...
    toppings = models.ManyToManyField(Topping)
```
###### It doesn’t matter which model has the ManyToManyField, but you should only put it in one of the models – not both.

##### It is also possible to create the through table yourself, if you need additional fields associated with the relation :

```py
from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through="Membership")

    def __str__(self):
        return self.name


class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["person", "group"], name="unique_person_group"
            )
        ]
```

## Admin and Data Management

### Q10: What is Django Admin?
Django Admin is a CRUD user interface for all of the application models

### Q11: How do you register models in the Django admin site?

You can register your models in admin.py like this: 

```py
from django.contrib import admin
from myapp.models import Author

admin.site.register(Author)
```

### Q12: How do you create a superuser and log in to the Django admin?

First your project needs to be properly migrated using makemigrations and migrate

now you can follow these steps to create a superuser:

1. Navigate to your project folder
`cd path/to/your/django/project`

2. Run the command for creating a superuser:
` python manage.py createsuperuser `

3. Enter required info

For loggin into the admin account you've just created: 

1. First, run the server:
` python manage.py runserver `

2. Navigate to the admin page:
` http://127.0.0.1:8000/admin/ `

3. Enter the username and password and login.

### Q13: What is a Django Form, and how does it differ from raw HTML forms?
### Q15: What are the advantages of Django forms (e.g., validation, security, reusability)?

Django Forms are used to gather input from users, validate that input, and process it, often saving the data to the database. For example, when registering a user, a form collects information like name, email, and password.

In raw HTML:

* Browser sends key‑value pairs to the server.
* You’re responsible for reading request.POST, validating data, and preventing security problems (like CSRF).
* There’s no automatic data binding or validation — you do everything manually.

In Django Form:

* Knows your fields.
* Can render HTML for you.
* Handles validation rules.
* Integrates with models (ModelForms).
* Provides security features like CSRF tokens and input cleaning.


### Q14: How do you create a forms.py file and connect it to a view?

```py
# myapp/forms.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your name")
    email = forms.EmailField(label="Email address")
    message = forms.CharField(widget=forms.Textarea, label="Message")
```

```py
# myapp/views.py
from django.shortcuts import render
from .forms import ContactForm  # Import the form

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Access cleaned data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # Process data here (send email, save, etc.)
            return render(request, 'myapp/success.html', {"name": name})
    else:
        form = ContactForm()  # Empty form for GET requests
    
    return render(request, 'myapp/contact.html', {'form': form})
```

```py
# myapp/urls.py
from django.urls import path
from .views import contact_view

urlpatterns = [
    path('contact/', contact_view, name="contact"),
]
```


### Q16:What’s the difference between ModelForm and Form in Django? When would you use each?

In forms.Form: 

```py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
```

* You define all fields.
* You decide how validated data is saved/processed (database, email, API, etc.).
* Not bound to any models.Model.

When to use:

* Forms that don’t directly save to your database.
* Search forms, login forms, filters, contact forms.
* Cases where model fields and form fields don’t match exactly.


In forms.ModelForm:

```py
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'email']
```

* Django generates form fields from the model fields.
* Handles saving automatically
* Useful for CRUD pages where form ↔ model mapping is direct.

When to use:

* Create/update forms for existing database tables.
* Admin dashboards, profile editors, content submission.
* Cases where you want Django to handle most of the boilerplate.