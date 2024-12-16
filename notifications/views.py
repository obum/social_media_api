from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Notification

# Create your views here.

class ListNotificationView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Notification.objects.all()
    
