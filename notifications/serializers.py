from rest_framework import serializers
from .models import Notification
from posts.serializers import LikeSerializer

class NotificationSerializer(serializers.ModelSerializer):
    target = LikeSerializer()  # Add this to serialize the Like object

    class Meta:
        model = Notification
        fields = ['recipient', 'actor', 'verb', 'target', 'timestamp']
        read_only_fields = ['recipient', 'actor', 'verb', 'target', 'timestamp']