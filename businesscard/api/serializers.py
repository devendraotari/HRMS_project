from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from businesscard.models import Card, Post, Like, Comment
from core.profile.models import UserProfile

User = get_user_model()


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'firstname', 'lastname', 'age', 'gender', "profile_pic")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.content = validated_data.get("content", instance.content)
        return instance


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"


class CardSerializers(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    card = CardSerializers(required=False)
    # owner = CustomUserSerializer()
    owner_id = serializers.CharField(required=True)
    class Meta:
        model = Post
        fields = ("id", "title", "content", "owner_id", "card", "total_likes", "total_comments", "owner_name")

    def create(self, validated_data):
        print(f'entered create {validated_data}')
        card_id = validated_data.pop("card_id", None)
        owner_id = validated_data.pop("owner_id",None)
        card = None
        try:
            if card_id:
                card = Card.objects.get(id=card_id)
            if owner_id:
                validated_data["owner"] = User.objects.get(id=owner_id)
            validated_data["card"] = card
            print(f'about to create {validated_data}')
            post: Post = Post.objects.create(**validated_data)
            print(f" from serializer post.owner {post.owner}")
            return post
        except ObjectDoesNotExist as odne:
            raise odne
        except Exception as e:
            raise e

    def update(self, instance, validated_data):
        card_id = validated_data.pop("card_id", None)
        card = instance.card
        try:
            if card_id:
                card = Card.objects.get(id=card_id)
            validated_data["card"] = card
            instance.title = validated_data.get("title", instance.title)
            instance.content = validated_data.get("content", instance.content)

            return instance
        except Exception as e:
            raise e
