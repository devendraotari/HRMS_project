from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from businesscard.models import CardTemplate, Post, Like, Comment, NonCompanyCard, CompanyCard
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


class CardTemplateSerializers(serializers.ModelSerializer):
    class Meta:
        model = CardTemplate
        fields = ("id", "created_at", "updated_at", "owner", "name", "background_image", "text", "logo", "company_name")

    def create(self, validated_data):
        try:
            print(validated_data)
            card_template = CardTemplate.objects.create(**validated_data)
            return card_template
        except Exception as e:
            raise e

    def update(self, instance, validated_data):
        try:
            instance.name = validated_data.get("name", instance.name)
            if "background_image" in validated_data:
                if validated_data.get("background_image") != " " or validated_data.get(
                        "background_image") != "":
                    instance.background_image = validated_data.get("background_image", instance.background_image)
            if "logo" in validated_data:
                if validated_data.get("logo") != " " or validated_data.get("logo") != "":
                    instance.logo = validated_data.get("logo", instance.logo)
            instance.text = validated_data.get("text", instance.text)
            instance.logo = validated_data.get("logo", instance.logo)
            instance.company_name = validated_data.get("company_name", instance.company_name)
            return instance
        except Exception as e:
            raise e


class NonCompanyCardSerializers(serializers.ModelSerializer):
    class Meta:
        model = NonCompanyCard
        fields = ("id", "created_at", "updated_at", "owner", "name", "background_image", "text", "logo", "company_name")

    def create(self, validated_data):
        try:
            non_company_card = NonCompanyCard.objects.create(**validated_data)
            return non_company_card
        except Exception as e:
            raise e

    def update(self, instance, validated_data):
        try:
            instance.name = validated_data.get("name", instance.name)
            if "background_image" in validated_data:
                if validated_data.get("background_image") != " " or validated_data.get(
                        "background_image") != "":
                    instance.background_image = validated_data.get("background_image", instance.background_image)
            if "logo" in validated_data:
                if validated_data.get("logo") != " " or validated_data.get("logo") != "":
                    instance.logo = validated_data.get("logo", instance.logo)
            instance.text = validated_data.get("text", instance.text)
            instance.logo = validated_data.get("logo", instance.logo)
            instance.company_name = validated_data.get("company_name", instance.company_name)
            return instance
        except Exception as e:
            raise e


class CompanyCardSerializer(serializers.ModelSerializer):
    # card_template = CardTemplateSerializers()
    # owner_id = serializers.CharField(required=True)

    class Meta:
        model = CompanyCard
        fields = ("id", "card_template", "owner_id", "text")

    def create(self, validated_data):
        try:
            # owner_id = validated_data.pop("owner_id")
            # owner = User.objects.get(id=owner_id)
            # validated_data['owner'] = owner
            company_card = CompanyCard.objects.create(**validated_data)
            return company_card
        except Exception as e:
            raise e


'''
POST feed serializers
'''


class PostSerializer(serializers.ModelSerializer):
    owner_id = serializers.CharField(required=True)

    class Meta:
        model = Post
        fields = ("id", "title", "content", "owner_id", "total_likes", "total_comments", "owner_name","owner")

    def create(self, validated_data):
        print(f'entered create {validated_data}')
        owner_id = validated_data.pop("owner_id", None)
        try:
            if owner_id:
                validated_data["owner"] = User.objects.get(id=owner_id)
            print(f'about to create {validated_data}')
            post: Post = Post.objects.create(**validated_data)
            print(f" from serializer post.owner {post.owner}")
            return post
        except ObjectDoesNotExist as odne:
            raise odne
        except Exception as e:
            raise e

    def update(self, instance, validated_data):
        try:
            instance.title = validated_data.get("title", instance.title)
            instance.content = validated_data.get("content", instance.content)
            return instance
        except Exception as e:
            raise e
