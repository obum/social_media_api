from django.urls import path

from .views import ListNotificationView

urlpatterns = [
    path('notifications/', ListNotificationView.as_view(), name='notifications')
]