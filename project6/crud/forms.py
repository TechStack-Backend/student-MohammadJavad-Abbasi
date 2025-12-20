from django import forms
from django.forms import ModelForm
from . import models
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User



class DeveloperForm(ModelForm):
    class Meta:
        model = models.Developer
        exclude = ['user']

    def clean_age(self):
        age = self.cleaned_data.get('age')
        
        if age is not None and age < 18:
            raise forms.ValidationError("Age must be 18 or older.")
        
        return age
    
    
class SkillForm(ModelForm):    
    class Meta:
        model = models.Skill
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user and hasattr(user, "developer") and not user.has_perm("crud.add_skill"):
            self.fields.pop("developer")

        if "developer" in self.fields:
            self.fields["developer"].queyset = models.Developer.objects.select_related("user")
            

    def clean_description(self):
        description = self.cleaned_data.get('description').strip()

        if not description:
            raise forms.ValidationError("Description is required")
        
        return description
    

class ProjectForm(ModelForm):
    class Meta:
        model = models.Project
        exclude = ['user', 'is_approved']
        widgets = {
            'developers': widgets.CheckboxSelectMultiple(),  
        }

    def clean(self):
        cleaned_data = super().clean()
        
        description = cleaned_data.get('description')
        
        if not description.strip():
            raise forms.ValidationError("Description is required.")

        return cleaned_data 
    

