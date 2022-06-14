from django.utils import timezone
from django.db import models

from apps.social_auth.models import SocialUser


class Post(models.Model):
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=100)
    user = models.ForeignKey(SocialUser, on_delete=models.CASCADE)
    pub_time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-pub_time"]

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(SocialUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_time = models.DateField(default=timezone.now)

    class Meta:
        ordering = ["-liked_time"]
        unique_together = ('user', 'post',)


class Comment(models.Model):
    user = models.ForeignKey(SocialUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commented_time = models.DateField(default=timezone.now)
    comment_description = models.CharField(max_length=100)

    class Meta:
        ordering = ["-commented_time"]
