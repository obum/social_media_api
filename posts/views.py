from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from notifications.models import Notification # For customized responses
from .serializers import PostSerializer, CommentSerializer
from .models import Like, Post, Comment
# from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
# from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions
from django_filters import rest_framework
from .permissions import IsAuthorOrReadOnly
from rest_framework.generics import ListAPIView

from rest_framework import generics
from rest_framework import status

from django.contrib.contenttypes.models import ContentType

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'content'] # Exact match filtering
    search_fields = ['title', 'content'] # search partial match
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        # Automatically set the author as the current user
        print(f"Authenticated User: {self.request.user}")
        print(f"Authenticated User: {self.request.user}, Is Authenticated: {self.request.user.is_authenticated}")
        serializer.save(author=self.request.user)

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set the author as the current user
        serializer.save(author=self.request.user)


class FeedView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    # queryset = Post.objects.all()
    
    def get_queryset(self):
        # Get the current user
        
        logged_in_user = self.request.user
        print(logged_in_user)
        
        # Get the users the logged in user is following
        following_users = logged_in_user.following.all()
        print(following_users)
        # Fetch posts from those users, ordered by creation date (most recent first)
        posts_by_following = Post.objects.filter(author__in=following_users).order_by('-created_at')
    
        print(posts_by_following)
        return posts_by_following
    
    
class LikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk, *args, **kwargs):
        ...
        # get the post to like from the database while getting the id from the endpoint.
        post_to_like = generics.get_object_or_404(Post, pk=pk)
        
        # get the logged in user
        logged_in_user = request.user
        
        # get the author of the post
        post_author = post_to_like.author
        
        # Check if the logged_in user wants to like his own post
        if logged_in_user == post_author:
            return Response({"error": "You cannot like your own post."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the post is already liked by user.
        
        is_liked = Like.objects.filter(post=post_to_like, liked_by=logged_in_user).exists()
        
        if is_liked:
            return Response({"error": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        
        # If all above is False - create a like object in the database
        like = Like.objects.create(post=post_to_like, liked_by=logged_in_user)
        
        # Create a notification object after for the like 
        
        like_content_type = ContentType.objects.get_for_model(Like)
        
        notification = Notification.objects.create(
            recipient= post_author,
            actor= logged_in_user,
            verb= 'like',
            content_type= like_content_type,
            object_id= like.id, # The ID of the Like instance   
            )
        is_notification = Notification.objects.filter(id=notification.id).exists()
        
        return Response({
            'message': f"{logged_in_user} liked '{post_to_like}' by {post_author}.",
            "like_id": like.id,
            "notification_created": is_notification
                }, status=status.HTTP_201_CREATED
                        )


class UnLikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk, *args, **kwargs):
        # get the post to unlike from the unlike endpoint.
        # generics.get_object_or_404(Post, pk=pk)
        post_to_unlike = generics.get_object_or_404(Post, pk=pk)
        
        # get the logged_in_user.
        logged_in_user = request.user
        
        # get the post_author
        
        post_author = post_to_unlike.author
        
        # Check if logged_in user is trying to unlike his own post
        
        if logged_in_user == post_author:
            return Response(
                {
                    'error': 'You cannot unlike your own post.'
                },  status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if post has been liked by user.
        
        try:
            # Like.objects.get_or_create(user=request.user, post=post)
            liked = Like.objects.get(post=post_to_unlike, liked_by=logged_in_user)

            # like_id_to_unlike = liked.id
        
        except ObjectDoesNotExist:
            return Response(
                {
                    'error': 'post is already unliked.'
                },  status=status.HTTP_400_BAD_REQUEST
            )
            
        liked.delete()
        
        
        notification = Notification.objects.create(
            recipient= post_author,
            actor= logged_in_user,
            verb= 'unlike',
            content_type= ContentType.objects.get_for_model(Like),
            object_id= post_to_unlike.id, # The ID of the Like instance would        
        )
        
        is_notification = Notification.objects.filter(pk=notification.id).exists()
        
        return Response({
            'message': f"{logged_in_user} unliked '{post_to_unlike}' by {post_author}.",
            "like_id": post_to_unlike.id,
            "notification_created": is_notification
                }, status=status.HTTP_204_NO_CONTENT
            )
        
        
        