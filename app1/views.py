from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Video, Comment, Profile
from .forms import UserRegisterForm, VideoUploadForm, CommentForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def home(request):
    videos = Video.objects.all()
    return render(request, 'home.html', {'videos': videos})


@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            messages.success(request, 'Your content has been uploaded successfully!')
            return redirect('video_detail', video_id=video.id)
    else:
        form = VideoUploadForm()
    return render(request, 'upload_video.html', {'form': form})


@login_required
def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.views_count += 1
    video.save()

    comments = video.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comment_user = request.user
            comment.video = video
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('video_detail', video_id=video.id)
    else:
        form = CommentForm()

    return render(request, 'video_detail.html', {
        'video': video,
        'comments': comments,
        'form': form
    })


@login_required
def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.user in video.like.all():
        video.like.remove(request.user)
    else:
        video.like.add(request.user)
        video.dislike.remove(request.user)
    return redirect('video_detail', video_id=video.id)


@login_required
def dislike_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.user in video.dislike.all():
        video.dislike.remove(request.user)
    else:
        video.dislike.add(request.user)
        video.like.remove(request.user)
    return redirect('video_detail', video_id=video.id)

