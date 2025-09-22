from django.forms import ModelForm
from . import models

class DeveloperForm(ModelForm):
    
    class Meta:
        model = models.Developer
        fields = '__all__'


class SkillForm(ModelForm):
    
    class Meta:
        model = models.Skill
        fields = '__all__'


class ProjectForm(ModelForm):
    
    class Meta:
        model = models.Project
        fields = '__all__'
