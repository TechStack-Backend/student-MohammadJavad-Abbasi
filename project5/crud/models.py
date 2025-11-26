from django.db import models
from django.contrib.auth.models import User

class Developer(models.Model):
    user_name = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user_name})"

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    developers = models.ManyToManyField(Developer)

    def __str__(self):
        return f"{self.title}"

class Skill(models.Model):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(max_length=1000, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.svg') 

    def __str__(self):
        return f"{self.user.username}'s Profile"