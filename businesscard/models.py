import uuid
from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from typing import Any, Callable, Iterator, Union, Optional, List

User = get_user_model()


class Like(models.Model):
    user = models.ForeignKey(User, related_name="+")
    created_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)


class UnReadNotification(models.Model):
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=255, blank=True)


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
    content = models.models.TextField(blank=False, null=False)
    card = models.ForeignKey(
        Card, related_name="+", blank=True, null=True, on_delete=models.CASCADE
    )
    likes = models.ForeignKey(Like, related_name="+", blank=True, null=True)
    comments = models.ForeignKey(Comment, related_name="+", blank=True, null=True)
    share_link = models.CharField(max_length=255, blank=True, null=True)
    author = models.ForeignKey(User, related_name="+", blank=True, null=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self:Any)-> str:
        return str(self.title)

    @property
    def posted_on(self)-> str:
        ini_time_for_now = datetime.now()
        delta = ini_time_for_now - (
            self.created_at if self.created_at > self.updated_at else self.updated_at
        )
        posted_on = str(delta).split(" ")[0]
        return posted_on

    @property
    def total_likes(self)-> int:
        total_likes = len(self.likes) if self.likes else 0
        return total_likes

    @property
    def total_comments(self)-> int:
        total_comments = len(self.comments) if self.comments else 0
        return total_comments
        

class RegularProfile(models.Model):
    user = models.OneToOneField(
        User, related_name="regular_profile", on_delete=models.CASCADE
    )
    firstname = models.CharField(max_length=255, blank=True, null=True)
    laststname = models.CharField(max_length=255, blank=True, null=True)
    profile_pic = models.FileField(
        upload_to="business_card/profile_pic/", max_length=100
    )
    my_card = models.ForeignKey(Card, related_name="regular_profile")


    def __str__(self)-> str:
        return str(self.firstname)