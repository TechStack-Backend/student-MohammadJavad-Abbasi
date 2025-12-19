# Task 6: Authorization & Signals

## 1. What is @permission_required, and how does it work for function-based views?
@permission_required is a Django view decorator used to restrict access to a view based on Django’s permission system.

It ensures that only users who have a specific permission can access a function‑based view (FBV).

```py
from django.contrib.auth.decorators import permission_required

@permission_required('blog.add_post')
def create_post(request):
    ...
```

Equivalent to:
```py
User.has_perm("blog.add_post")
```

## 2. What is PermissionRequiredMixin, and how is it used in class-based views? 
PermissionRequiredMixin is a Django mixin used with Class‑Based Views (CBVs) to restrict access based on user permissions.

It is the CBV equivalent of @permission_required for function‑based views.

```py
from django.contrib.auth.mixins import PermissionRequiredMixin
```

Basic usage:

```py
from django.views.generic import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Developer

class DevelopersList(PermissionRequiredMixin, ListView):
    model = Developer
    permission_required = "crud.view_developer"
```

## 3. What is the effect of setting raise_exception=True? 

Instead of redirecting the user to LOGIN_URL it raises PermissionDenied(HTTP 403 Forbidden) error.

FBV:

```py
@permission_required("crud.change_post", raise_exception=True)
def edit_post(request, pk):
    ...
```

CBV:

```py
class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "crud.change_post"
    raise_exception = True
```


## 4. What is the difference between @login_required and @permission_required? 

@login_required only checks authentication

@permission_required checks for authentication and permissions, it has more flexibility, it checks for authorization and it can raise 403 error

## 5. What are Django’s default model permissions (add, change, delete, view)?

These are the model permissions that Django creates automatically for each model.

<*appname*>.add_<*model*> : Allows the user to create new objects.

<*appname*>.change_<*model*> : Allows the user to edit/update existing objects.

<*appname*>.delete_<*model*> : Allows the user to delete objects.

<*appname*>.view_<*model*> : Allows the user to see/read objects. 

Note: The model name has to be singular: developer, not developers


## 6. How can we define custom permissions using Meta.permissions in a model? 

In Django, custom permissions are defined directly on a model using Meta.permissions. Django then creates them in the database during migrations, just like the default add / change / delete / view permissions.

```py
from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    is_public = models.BooleanField(default=True)

    class Meta:
        permissions = [
            ("publish_project", "Can publish project"),
            ("archive_project", "Can archive project"),
        ]
```

What Django creates:

- app_label.publish_project

- app_label.archive_project

run migrations:

```
python manage.py makemigrations
python manage.py migrate
```

## 7. How can we use custom permissions using Meta.permissions? 

First add the custom permissions to your model

Now create a group, give the group the custom permissions, add the user to the group.

```py
from django.contrib.auth.models import Group, Permission

editors, _ = Group.objects.get_or_create(name="Editors")

publish_perm = Permission.objects.get(codename="publish_project")
archive_perm = Permission.objects.get(codename="archive_project")

editors.permissions.add(publish_perm, archive_perm)
```

```py
user.groups.add(editors)
```


## 8. How does user.has_perm() work internally?

```
user.has_perm("crud.publish_project")
│
├─ Is user active & superuser? → YES → True 
│
├─ Loop through auth backends
│   └─ ModelBackend.has_perm()
│
├─ Collect user.permissions
├─ Collect group.permissions
├─ Union them
│
└─ Is "crud.publish_project" in the set? → True / False
```

## 9. When should we use model-level permissions instead of hard-coded role checks?

Use model‑level permissions when access control is about what actions a user is allowed to perform, not who the user is.

They are best when:

• rules may change or grow over time

• multiple roles share overlapping abilities

• access must be enforced consistently across views, templates, APIs, and admin

• the action is tied to a model (publish, approve, export, archive)

Avoid hard‑coded role checks except for fixed identity rules (e.g., superuser) or ownership checks.

In most real apps, the correct pattern is permissions for capabilities + explicit ownership checks for objects.

### 9. What is the difference between assigning permissions to a Group vs directly to a User? 
### 10. Why are group-based permissions more scalable in real projects? 
### 11. In what special cases is assigning permissions directly to users justified? 
### 12. How can we restrict access so that only the owner of an object can edit it? 
### 13. What are the limitations of Django’s built-in permission system regarding object-level access? 
### 14. How can we combine ownership checks with model permissions? 
### 16. How can we implement a reusable owner_required decorator? 
### 17. How can we write an OwnerOrPermissionMixin for class-based views? 
### 18. What are the best practices for keeping permission logic clean and testable? 