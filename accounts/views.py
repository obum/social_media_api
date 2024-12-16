# from django.shortcuts import render #Do not need tis import
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, UserSerializer

from rest_framework.views import APIView
from rest_framework.authentication import authenticate
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model


from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework import generics, permissions

User = get_user_model()
# Create your views here.


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user :
            # token = Token.objects.get(user=user)
            # Delete any existing tokens for the user
            Token.objects.filter(user=user).delete()
            # Generate a new token
            token = Token.objects.create(user=user)
            return Response({"token": token.key}, status=HTTP_200_OK)
        return Response({"error": "Invalid username or password"}, status=HTTP_400_BAD_REQUEST)
   
class ProfileViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Restrict to the logged-in user's profile
        return self.queryset.filter(id=self.request.user.id)
    
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the user's token and delete it
            request.user.auth_token.delete()
            return Response({"message": "Successfully logged out."}, status=HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Token not found."}, status=HTTP_400_BAD_REQUEST)
        
    # class RegisterView(CreateAPIView):
    #     serializer_class = RegisterSerializer
    #     permission_classes = [AllowAny]

    #     def create(self, request, *args, **kwargs):
    #         # Validate and save the user using the serializer
    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid(raise_exception = True)
    #         user = serializer.save()

    #         # Ensure user is valid and token is created
    #         if user is None:
    #             return Response({"error": "User could not be created"}, status=HTTP_400_BAD_REQUEST)
            
    #         # Generate or retrieve the token for the user
    #         token, created = Token.objects.get_or_create(user=user)

    #         # Prepare the response data
    #         response_data = {
    #             "token": token.key,
    #             "user": UserSerializer(user).data
    #         }
            
    #         # Return the response
    #         return Response(response_data, status=HTTP_201_CREATED)


# ----------- follow / unfollow action to modify the following relationship ----------- #

class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id, *args, **kwargs):
        # Get the user to follow from the database using the user_id (unique identifier)
        user_to_follow = get_object_or_404(User, pk=user_id)
        # CustomUser.objects.all()
        logged_in_user = request.user

        # Check if the logged-in user is trying to follow themselves
        if logged_in_user == user_to_follow:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the logged-in user is already following the user
        is_following = logged_in_user.following.filter(id=user_to_follow.id).exists()

        if is_following:
            return Response({"error": f"You are already following {user_to_follow.username}."}, status=status.HTTP_400_BAD_REQUEST)

        # Add the user to the logged-in user's following list
        logged_in_user.following.add(user_to_follow)

        return Response({'message': f'You are now following {user_to_follow.username}.'}, status=status.HTTP_200_OK)

class UnFollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, user_id, *args, **kwargs):
        
        # Get the user object to unfollow from the database but parsed from the endpoint
        user_to_unfollow = get_object_or_404(User, pk=user_id)
        
        logged_in_user = request.user # user who wants to unfollow
        
        # check if the user wants to unfollow himself
        
        if logged_in_user == user_to_unfollow:
            return Response({"error": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        # check if the user wants to unfollow someone who is not being followed
        is_followed = logged_in_user.following.filter(id=user_to_unfollow.id).exists()
        
        if not is_followed:
            return Response({"error": f"{user_to_unfollow} is already unfollowed."}, status=status.HTTP_400_BAD_REQUEST)
            
        logged_in_user.following.remove(user_to_unfollow)
        return Response({'message': f'You are no longer following {user_to_unfollow.username}.'}, status=status.HTTP_200_OK)


