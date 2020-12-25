from rest_framework import serializers
from django.contrib.auth import get_user_model
from businesscard.models import Card,Post,Like,Comment
from core.profile.models import UserProfile

User = get_user_model()

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email',)

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = "__all__"


class CardSerializers(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(required=False)
    comments = serializers.IntegerField(required=False)
    card = CardSerializers(required=False)
    class Meta:
        model = Post
        fields = ("id","title","content","card","likes","comments","author")