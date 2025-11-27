from django import forms
from django.forms import ModelForm
from . import models
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=widgets.TextInput)
    password = forms.CharField(widget=widgets.PasswordInput)
    
class UserProfileForm(ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ['first_name', 'last_name', 'bio', 'avatar']