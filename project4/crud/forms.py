from django.forms import ModelForm, forms
from . import models
from django.forms import widgets


class DeveloperForm(ModelForm):
    class Meta:
        model = models.Developer
        fields = '__all__'

    def clean_age(self):
        age = self.cleaned_data.get('age')
        
        if age < 18:
            raise forms.ValidationError("Age must be 18 or older.")
        
        return age
    
    
class SkillForm(ModelForm):    
    class Meta:
        model = models.Skill
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'developer' in self.fields:
            self.fields['developer'].disabled = True

    def clean_description(self):
        description = self.cleaned_data.get('description').strip()

        if not description:
            raise forms.ValidationError("Description is required")
        
        return description
    

class ProjectForm(ModelForm):
    class Meta:
        model = models.Project
        fields = '__all__'
        widgets = {
            'developers': widgets.CheckboxSelectMultiple(),  
        }

    def clean(self):
        cleaned_data = super().clean()
        
        description = cleaned_data.get('description')
        
        if not description.strip():
            raise forms.ValidationError("Description is required.")

        return cleaned_data 