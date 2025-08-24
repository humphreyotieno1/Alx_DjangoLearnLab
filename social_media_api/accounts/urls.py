from django.urls import path
from .views import RegisterView, LoginView, ProfileView, FollowersView, FollowingView, FollowUserView, UnfollowUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('followers/', FollowersView.as_view(), name='followers'),
    path('following/', FollowingView.as_view(), name='following'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow'),
]
