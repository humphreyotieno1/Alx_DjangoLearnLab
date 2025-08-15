from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:post_id>/comments/new/', views.CommentCreateView.as_view(), name='comment_create'),
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment_create'),
    path('posts/<int:post_id>/comments/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('posts/<int:post_id>/comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    
    # correction
    path('/comments/<int:pk>/new/', views.CommentUpdateView.as_view(), name='new'),
    path('/comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('/comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    
]