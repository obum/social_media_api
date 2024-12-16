from django.contrib import admin
from .models import User, Profile
from posts.models import Post

# Register your models here.

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Profile)