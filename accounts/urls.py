from django.urls import path, include
from .views import LoginView, LogoutAPIView, RegisterView, ProfileViewSet, LogoutAPIView, FollowUserView, UnFollowUserView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views  

router = DefaultRouter()

# Router to handle Get profile and obtain profile requests
router.register('profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('lgout/', LogoutAPIView.as_view(), name='logout'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', UnFollowUserView.as_view(),  name='unfollow')
]

# A mechanism for clients to obtain a token given the username and password.
# REST framework provides a built-in view to provide this behavior. 
urlpatterns += [
    path('token', views.obtain_auth_token)
]
# /follow/<int:user_id>/ and /unfollow/<int:user_id>/).