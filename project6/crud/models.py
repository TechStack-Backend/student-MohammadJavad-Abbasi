from django.db import models
from django.contrib.auth.models import User

class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='developer')
    age = models.IntegerField(null=True, blank=True)
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    availability = models.BooleanField(default=True)


    def __str__(self):
        return self.user.username
    
    class Meta:
        permissions = [
            ("edit_all_profiles", "Can edit all profiles")
        ]

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    developers = models.ManyToManyField(Developer)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        permissions = [
            ("approve_project", "Can approve project")
        ]

class Skill(models.Model):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='skills')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)

