from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('upload/', views.upload_video, name='upload_video'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
    path('video/<int:video_id>/like/', views.like_video, name='like_video'),
    path('video/<int:video_id>/dislike/', views.dislike_video, name='dislike_video'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]