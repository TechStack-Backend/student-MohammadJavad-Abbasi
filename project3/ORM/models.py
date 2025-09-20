from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
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

class Skill(models.Model):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)

    