from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings


class User(AbstractUser):
    email = models.EmailField(max_length=255, null=True, blank=True)
    bio = models.TextField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    # followers = models.ManyToManyField('self', symmetrical=False, blank=True, through='Follow')
    following = models.ManyToManyField('self', symmetrical=False, blank=True)

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = []

    # objects = UserManager()

    def __str__(self):
        return self.username
    
# class Follow(models.Model):
#     from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         unique_together = ('from_user', 'to_user')
        
#     def __str__(self):
#         return f"{self.from_user.username} follows {self.to_user.username}"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return f"{self.user.username}'s profile"