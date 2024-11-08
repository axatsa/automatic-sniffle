from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Video(models.Model):
    video_title = models.CharField(max_length=100)
    video_content = models.FileField(upload_to='content/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    like = models.ManyToManyField(User, blank=True, related_name='liked_videos')
    dislike = models.ManyToManyField(User, blank=True, related_name='disliked_videos')
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    views_count = models.IntegerField(default=0)

    def __str__(self):
        return self.video_title

    @property
    def like_count(self):
        return self.like.count()

    @property
    def dislike_count(self):
        return self.dislike.count()


class Comment(models.Model):
    comment_text = models.TextField()
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.comment_user.username} - {self.comment_text[:50]}'
