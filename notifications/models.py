from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications') # User that recieves the notification.
    actor  = models.ForeignKey(User, on_delete=models.CASCADE) # User that causes the notification.
    verb  = models.CharField(max_length=10) #  follow, unfollow, like, comment, post (optional)
    content_type  = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id  = models.PositiveIntegerField()
    target  = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)