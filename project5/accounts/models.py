from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(max_length=1000, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.svg') 

    def __str__(self):
        return f"{self.user.username}'s Profile"