import uuid
from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from typing import Any, Callable, Iterator, Union, Optional, List

User = get_user_model()


class Like(models.Model):
    owner = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    post_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    owner = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    text = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    post_id = models.PositiveIntegerField()


class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    background_image = models.FileField(upload_to="card/background/", max_length=100)
    text = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to="card/logo_image/", blank=True, null=True)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=150, blank=True, null=True)
    content = models.TextField(blank=False, null=False)
    card = models.ForeignKey(
        Card, related_name="+", blank=True, null=True, on_delete=models.CASCADE
    )
    # likes = models.ForeignKey(Like, related_name="+", blank=True, null=True, on_delete=models.CASCADE)
    # comments = models.ForeignKey(Comment, related_name="+", blank=True, null=True, on_delete=models.CASCADE)
    share_link = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(User, related_name="posts", blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self: Any) -> str:
        return str(self.title)

    @property
    def posted_on(self) -> str:
        ini_time_for_now = datetime.now()
        delta = ini_time_for_now - (
            self.created_at if self.created_at > self.updated_at else self.updated_at
        )
        posted_on = str(delta).split(" ")[0]
        return posted_on

    @property
    def owner_name(self) -> str:
        return str(self.owner.profile.firstname + " " + self.owner.profile.laststname)

    @property
    def total_likes(self) -> int:
        likes = Like.objects.all().filter(post_id=self.id)
        total_likes = len(likes) if likes else 0
        return total_likes

    @property
    def total_comments(self) -> int:
        comments = Comment.objects.all().filter(post_id=self.id)
        total_comments = len(comments) if comments else 0
        return total_comments


class RegularProfile(models.Model):
    user = models.OneToOneField(
        User, related_name="regular_profile", on_delete=models.CASCADE
    )
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    profile_pic = models.FileField(
        upload_to="business_card/profile_pic/", max_length=100
    )
    my_card = models.ForeignKey(Card, related_name="regular_profile", blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return str(self.firstname)
