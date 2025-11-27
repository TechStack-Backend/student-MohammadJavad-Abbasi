# Task 5: User Authentication and Static Files Management Objective

## User Authentication

### Q1. What is Django’s built-in authentication system, and what problems does it solve?

The Django authentication system handles both authentication and authorization. Briefly, authentication verifies a user is who they claim to be, and authorization determines what an authenticated user is allowed to do. Here the term authentication is used to refer to both tasks.

The auth system consists of:

* Users
* Permissions: Binary (yes/no) flags designating whether a user may perform a certain task.
* Groups: A generic way of applying labels and permissions to more than one user.
* A configurable password hashing system
* Forms and view tools for logging in users, or restricting content
* A pluggable backend system

### Q2. How web applications save the password and why?

web apps use cryptographic hashing, a one-way mathematical operation that transforms the password into a fixed-length string.

Process Overview:
User enters password → e.g., "MySecurePassword!"
App generates a random salt, e.g., "Xf09$1Bn"→ ensures uniqueness so that identical passwords produce different hashes.
App combines them:

   salted = password + salt

Then it applies a slow, secure hashing algorithm such as:

bcrypt
argon2
PBKDF2
scrypt
These algorithms intentionally slow down computation (using iterations or memory hardness) to make brute-force attacks impractical.

The app finally stores only:

   username | salt | hashed_password | hash_algorithm
Example:

🧾 3. When the User Logs In
The app retrieves that user’s salt and hash.
It rehashes the entered password + salt using the same algorithm and compares it to the stored hash.
If they match → login succeeds.
If not → login fails.
Key point: the app never needs to know or recover the original password. Hashing is irreversible.

🛡️ 4. Why a “Slow” Hash is Crucial
Modern attackers can try billions of passwords per second using GPUs.

Fast algorithms like MD5 or SHA-1 are easy to crack.

Slow hashes (bcrypt/argon2) make each guess take milliseconds — drastically reducing feasibility.


### Q3. What’s the difference between hashing, encoding, and encryption?

- #### Hashing:
    A one‑way mathematical function that turns input data into a fixed‑length digest.

    You can’t get the original data back from the hash.

    Common algorithms: SHA‑256, bcrypt, Argon2, MD5 (obsolete).

    Properties:

    Deterministic (same input → same output)
    Irreversible
    Collision‑resistant (hard to find two inputs with same output)
    Used for:
    Password storage
    File integrity checks
    Digital signatures

- #### Encryption:
    A reversible transformation using a secret key.

    You can decrypt it to retrieve the original data if you have the key.

    Types:

    Symmetric: one key used for both encryption/decryption (AES, ChaCha20)
    Asymmetric: public/private key pair (RSA, ECC)

- #### Encoding: 
    Maps data into a different format that can be decoded back to the original easily.

    No key, no secrecy — purely representational.

    Examples:

    Base64
    URL encoding
    UTF‑8 text encoding
    Used for:

    Transmitting binary data as ASCII, embedding images in HTML, percent‑encoding URLs, etc.

### Q4. What are sessions and cookies, and how do they help keep users logged in?

The Core Problem: HTTP Is “Stateless”
The HTTP protocol doesn’t remember anything between requests.

Each time your browser sends a request, the server sees it as new and separate — it has no memory of who you are or that you’ve already logged in.

To maintain continuity (“stay logged in” across pages), web apps need a way to persist user state between requests.

Enter: cookies and sessions.

* Cookies:
    A cookie is a small piece of data stored in the user’s browser by the website.

    It gets automatically sent with every request to that same domain.

    Example content:
    ` session_id=abc123xyz; Expires=Wed, 01 Jan 2026 00:00:00 GMT; Path=/; Secure; HttpOnly `

    Purpose:

    * Identify the user (or their session)
    * Store simple preferences (e.g., theme=dark)
    * Track analytics or authentication info indirectly

* Sessions:
    A session is a server-side storage object associated with a unique identifier (often the session_id stored in a cookie).

    Workflow:

    1. User logs in with username/password.
    2. Server authenticates and creates a session record like:

    ```
    {
        "session_id": "abc123xyz",
        "user_id": 42,
        "login_time": "2025-11-24T20:00:00Z",
        "cart_items": [17, 19]
    } 
    ```

    3. Server sends a cookie with just the session ID:

        ` Set-Cookie: session_id=abc123xyz; HttpOnly; Secure `

    4. On every request, the browser sends the cookie.
    5. The server looks up the session_id → retrieves associated data → knows which user you are.

### Q5: Where do sessions save?
- Server‑Side Sessions (Most Common)
    When a session is created after login, most servers store the data on the server, not in the browser.

    The browser only keeps the session ID (in a cookie) — the actual session content lives server‑side.

- Client‑Side Sessions (Token‑Based)
    Modern architectures (e.g., APIs, SPAs) may store all session info directly in the browser, instead of server memory.

    These use tokens such as:

    JWT (JSON Web Token) — contains user data + signature
    Stored in cookies or LocalStorage
    Since JWTs carry their own data, the server doesn’t need to maintain session state — it just verifies the token’s signature.

    Pros: scalable, stateless

    Cons: larger payloads, must protect against XSS/CSRF leaks

### Q6: What are the main authentication views Django provides (e.g., LoginView, LogoutView, PasswordChangeView)?

1- LoginView:  Handles user login (displays the login form and processes credentials).
Default template: registration/login.html

2- LogoutView
Purpose: Logs the user out and optionally displays a confirmation page.
Default template: registration/logged_out.html

3- PasswordChangeView
Purpose: Allows authenticated users to change their password while logged in.
Template: registration/password_change_form.html

4- PasswordChangeDoneView
Purpose: “Success” page after password is changed.
Template: registration/password_change_done.html

5- PasswordResetView
Purpose: Initiates “forgot password” process — sends reset email link.
Template: registration/password_reset_form.html

6- PasswordResetDoneView
Purpose: Confirmation shown after user requests a password reset (email sent).
Template: registration/password_reset_done.html

7- PasswordResetConfirmView
Purpose: Endpoint linked in the reset email — user sets new password.
Template: registration/password_reset_confirm.html

8- PasswordResetCompleteView
Purpose: “Password successfully reset” confirmation page.
Template: registration/password_reset_complete.html

### Q7: How can we restrict access to certain pages (for example, using @login_required or LoginRequiredMixin)?

#### Function‑Based Views: @login_required
If you’re defining a function-based view, use the decorator provided by Django:

```
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
```

What it Does
Checks if request.user.is_authenticated is True.
If not authenticated, redirects to the login page defined by settings.LOGIN_URL.
After login, Django automatically redirects the user back to the originally requested page using the ?next= query parameter.

In your settings.py:

```
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
```

LOGIN_URL: where unauthenticated users are sent.
LOGIN_REDIRECT_URL: where users are taken after a successful login.

#### Class‑Based Views: LoginRequiredMixin

For class-based views (CBVs), you use a mixin instead of a decorator.

```
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
```

Important: Place LoginRequiredMixin before the main view class (e.g., before TemplateView).

This ensures the mixin’s method resolution order (MRO) runs the authentication check first.

Customize Redirect Target
Like the decorator, the mixin has attributes you can override:

```
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = '/login/'
    redirect_field_name = 'next'
```

#### Restrict by Permissions
For even finer control, Django also provides:

- PermissionRequiredMixin
- UserPassesTestMixin


```py
from django.contrib.auth.mixins import PermissionRequiredMixin

class AdminView(PermissionRequiredMixin, TemplateView):
    permission_required = 'auth.view_user'
    template_name = 'admin_area.html'
```


```py
from django.contrib.auth.mixins import UserPassesTestMixin

class ManagerView(UserPassesTestMixin, TemplateView):
    def test_func(self):
        return self.request.user.groups.filter(name='Managers').exists()
```

### Q8: How can we create a custom user registration form?

In forms.py import User model and UserCreationForm
and create a custom form class that inherits from the UserCreationForm and add your custom logic:

forms.py
```py
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
```


Next in your views.py import that form and create a class inheriting from the CreateView and add the model and form you've just created:

views.py
```py
from django.contrib.auth.models import User

class NewUser(CreateView):
    model = User
    form_class = forms.UserForm
    template_name = 'crud/new_user.html'
    success_url = reverse_lazy('homepage')
```

### Q9: 9. What is Django default user model? 
 
By default, Django uses:

```py 
from django.contrib.auth.models import User
```

This is a class called User, provided by the built‑in django.contrib.auth app.

It’s a standard model that represents each user in the authentication system.

Main Fields
The default User includes the most common fields:

Field | Type | Description
--- | --- | --- |
username | CharField | unique identifier for login
password | CharField (hashed) | user password
email | EmailField | optional by default
first_name, last_name | CharField | optional name info
is_staff | BooleanField | can log in to admin site
is_active | BooleanField | disables account instead of deleting it
is_superuser | BooleanField | site‑wide permissions
last_login | DateTimeField | updated automatically on login
date_joined | DateTimeField	| when user was created


### Q10:  How we can extend Django default user model?

There are two ways to do this:

1- One-to-one extention (profile model)

```py
# user/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


# Automatically create/update profile when a User is saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
```

Pros:

Safe to add later, even in an existing project
Keeps the built‑in User untouched
Still uses Django admin, login, and permissions as usual


2- Custom user model (Swap the core class):

```py
# user/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    # you can remove 'username' if you want email-based login only

    def __str__(self):
        return self.username or self.email
```

```py
#settings.py
AUTH_USER_MODEL = 'user.CustomUser'
```
 - This line must be added before the first migrate, otherwise your DB will already contain the default auth_user table and changing it later will be painful.
  
You can then build your sign‑up and login forms against this new model using get_user_model():

```py
from django.contrib.auth import get_user_model
User = get_user_model()
```

Pros

Total control (fields, login identity, behavior)
Easier integrations with APIs or phone/email auth

cons

Must decide early (before initial migrate)
Slightly more boilerplate in views/forms

### Q11:  How can we connect the User model to other models (like linking a Developer to a User)?

Add a ForeignKey to Developer

```py
#models.py
from django.db import models
from django.contrib.auth.models import User  # or get_user_model() if using a custom model

class Developer(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='developers'
    )
    name = models.CharField(max_length=100)
    # other existing fields ...

    def __str__(self):
        return self.name
```

### Q12: Should we extend user model or use one to one relationship? 
### Q13:  Should we use Django default model without extending? 
The best-practice option is creating a new User class inheriting from the AbstractUser or AbstractBaseUser and then adding the features you need to the class or create a 1:1 relationship between the new User class and the features you need. 
If you want to add new features later in development , create the new User inheriting from django's abstract user classes but leave it as is.

```py
class newUserModel(AbstractUser):
    pass
```

For using these custome classes as the User model you also need to add your class in the project settings.py 
```py
   AUTH_USER_MODEL = 'accounts.CustomUser'
```

### Q14:

Concept	| Session‑based auth | JWT (JSON Web Token) auth
--- | --- | --- 
State	| Stateful — server keeps session data in memory or DB	| Stateless — server stores nothing, only verifies token
Storage (client) | Browser stores a session cookie | Browser/app stores a JWT token (usually localStorage, cookie, or header)
Server‑side persistence	| Server keeps session_id → user data mapping | Server keeps only a secret key to verify token signature
Response content | Server sends Set‑Cookie containing session ID | Server sends JWT string (header.payload.signature)
Authentication flow	| Client → login → server creates session → cookie stored → server looks up each request via session ID | Client → login → server issues JWT → client sends token in future requests → server verifies signature and decodes payload
Scalability	| Harder, sessions must be shared across servers or cached (Redis) | Easier, any server can validate the token without central storage
Revocation | Need manual logout to delete session; easy to invalidate | Harder — tokens are valid until expiry, need blacklist or short TTL
Security | Cookie controlled by browser; CSRF protection built‑in | Token in headers avoids CSRF but can suffer XSS if stored poorly
Expiration | Server controls session lifetime or refresh logic | Token has exp claim; once expired, must issue a new token
Best suited for	| Traditional web apps (Django templates, server‑rendered HTML)	| APIs, SPA clients (React, Vue, mobile) with detached front‑end


in Django: 
Session auth is native:

Uses django.contrib.auth + SessionMiddleware
On login, Django creates a record in the django_session table.
Client gets a cookie (sessionid).
Every subsequent request automatically identifies user based on that cookie.
JWT auth typically comes via packages such as:

djangorestframework-simplejwt
djangorestframework-jwt
Used in REST API backends for SPAs/mobile clients.