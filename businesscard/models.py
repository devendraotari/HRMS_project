import uuid
from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from typing import Any, Callable, Iterator, Union, Optional, List
from core.profile.models import UserProfile as Profile

User = get_user_model()


class Like(models.Model):
    owner = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    post_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    owner = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    text = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    post_id = models.CharField(max_length=255)


class CardTemplate(models.Model):
    '''
    Owner:User this user will be the HR admin who has access to create the card template
    This card template is used by HR-Admin for creating the company card
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    background_image = models.FileField(upload_to="card/background/", max_length=100)
    text = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to="card/logo_image/", blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(User, related_name="card_template", blank=True, null=True, on_delete=models.CASCADE)

    # class Meta:
    #     permissions = (
    #         ("create_card_template", "can create_card_template"),
    #         ("update_card_template", "can update card template"),
    #         ("delete_card_template", "can delete card template"),
    #         ("view_card_template", "can view card template")
    #     )


class CompanyCard(models.Model):
    """
    Owner:User this user is the employee who will be using the card and sharing the same
    This Company card is the instance which HR will create for employee and employees can share it
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    card_template = models.ForeignKey(CardTemplate,related_name="+",blank=False,null=False,on_delete=models.CASCADE)
    owner = models.ForeignKey(User,related_name='card',on_delete=models.CASCADE)
    text = models.CharField(max_length=255, blank=True, null=True)


class NonCompanyCard(models.Model):
    """
    Owner:User here owner is the regular cardish user who has not
               added/subscribed to company but he/she can possess a personal card
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    background_image = models.FileField(upload_to="non_company_card/background/", max_length=100)
    text = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to="non_company_card/logo_image/", blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(User, related_name="non_company_card", blank=True, null=True, on_delete=models.CASCADE)


class Post(models.Model):
    """
    Post: this is the feed post of cardish app
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=150, blank=True, null=True)
    content = models.TextField(blank=False, null=False)
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
        owner_name = None
        profile = Profile.objects.get(user=self.owner)
        owner_name = str(profile.firstname + " " + profile.lastname)
        return owner_name

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

    def __str__(self) -> str:
        return str(self.firstname)


class SharedCardsMapping(models.Model):
    card_id = models.CharField(max_length=17)
    owner_id = models.CharField(max_length=17)
    shared_with_user_id = models.CharField(max_length=17)
    created_at = models.DateTimeField(auto_now_add=True)
