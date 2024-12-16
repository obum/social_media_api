from rest_framework import serializers
from .models import Comment, Like, Post

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    likes_count = serializers.SerializerMethodField() # Added to know the number of likes for a post

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
        
    def get_likes_count(self, obj):
        return obj.likes.count() # counts the likes in a given post using the reverse relationship / related name

    def validate_title(self, value):
        if Post.objects.filter(title=value).exists():
            raise serializers.ValidationError('Post with this title already exists')
        return value

class CommentSerializer(serializers.ModelSerializer):
    # Ensure that only post the exists can be commented on or referenced.
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = '__all__'
        
class LikeSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    
    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


