import uuid
from django.db.models import Q
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from businesscard.models import Like, Comment, Post, CardTemplate, NonCompanyCard, CompanyCard
from businesscard.api.serializers import CommentSerializer, PostSerializer, CardTemplateSerializers, \
    NonCompanyCardSerializers, CompanyCardSerializer
from rest_framework import permissions
from core.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth import get_user_model

User = get_user_model()


class PostCreateAPIView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        validated_data = {}
        owner = request.user
        validated_data.update(request.data)
        validated_data.update({"owner": request.user.id})
        print(f"before serializer {validated_data}")
        serializer = self.serializer_class(data=validated_data, partial=True)
        try:
            if serializer.is_valid(raise_exception=True):
                print('before save')
                serializer.save()
                return Response({"msg": "post created successfully", "created_post": serializer.data},
                                status=status.HTTP_201_CREATED)
        except Exception as e:
            print('in exception')
            return Response({"error": str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)


class PostUpdateDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication]
    model = Post

    def put(self, request, pk=None):
        owner = request.user
        instance = Post.objects.get(id=pk)
        validated_data = request.data
        serializer = PostSerializer(data=validated_data, instance=instance, partial=True)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"msg": "post updated successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def get(self, request):
        return Response({"error": "GET method not allowed"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk=None):
        try:
            post = Post.objects.get(id=pk)
            if post:
                post.delete()
                return Response({"msg": "post deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"post not found for given id {pk}"}, status=status.HTTP_404_NOT_FOUND)


class PostListRetrieveView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request, pk=None):
        if pk:
            post = Post.objects.get(id=pk)
            serializer = PostSerializer(post)
            return Response({"post": serializer.data}, status=status.HTTP_200_OK)

        else:
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return Response({"posts": serializer.data}, status=status.HTTP_200_OK)


class LikeOnPostView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request):
        if "post_id" in request.data:
            like = Like.objects.get_or_create(owner=request.user, post_id=request.data["post_id"])
            # like.post_id = request.data["post_id"]
            like[0].save()
            return Response({"msg": f"post with id {request.data['post_id']} liked"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": f"need post_id in request data"}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request):
        return Response({"error": "GET method not allowed"}, status=status.HTTP_403_FORBIDDEN)


class UnLikeOnPostView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request):
        if "post_id" in request.data:
            like = Like.objects.get(Q(owner=request.user) and Q(post_id=request.data["post_id"]))
            if like:
                like.delete()
            return Response({"msg": f"post with id {request.data['post_id']} unliked"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": f"need post_id in request data"}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request):
        return Response({"error": "GET method not allowed"}, status=status.HTTP_403_FORBIDDEN)


class CommentOnPostView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def get(self, request):
        if "post_id" in request.GET:
            comments = Comment.objects.all().filter(post_id=request.GET.get("post_id"))
            serialized = CommentSerializer(comments, many=True)
            return Response({"comments": serialized.data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": f"need post_id in request GET params"}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        if "post_id" in request.data:
            comment = Comment.objects.create(
                post_id=request.data.get("post_id"),
                text=request.data.get("text"),
                owner=request.user,
            )
            comment.save()
            return Response({"msg": f"post with id {request.data['post_id']} id commented"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": f"need post_id in request data"}, status=status.HTTP_204_NO_CONTENT)


class CommentOnPostRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def put(self, request, pk=None, *args, **kwargs):
        comment = Comment.objects.get(id=pk)
        serializer = self.serializer_class(data=request.data, instance=comment, partial=True)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"msg": f"comment with id {pk} is updated"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk=None, *args, **kwargs):
        comment = Comment.objects.get(id=pk)
        if comment:
            comment.delete()
            return Response({"msg": f"comment with id {pk} is deleted"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": f"comment with id {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk=None, *args, **kwargs):
        comment = Comment.objects.get(id=pk)
        if comment:
            serialized = CommentSerializer(comment)
            return Response({"comment": serialized.data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": f"comment with id {pk} not found"}, status=status.HTTP_404_NOT_FOUND)


'''
Card sharing Related APIs  
'''


class CardTemplateAPIView(APIView):
    """
    This View for CRUD operations on CardTemplate
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        validated_data = {}
        validated_data.update(request.data)
        owner = request.user
        validated_data.update({"owner": owner.id})
        serializer = CardTemplateSerializers(data=validated_data, partial=True)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"msg": f"card template is created with id {serializer.data}"},
                                status=status.HTTP_201_CREATED
                                )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, *args, **kwargs):
        try:
            pk = uuid.UUID(pk)
            card_template = CardTemplate.objects.get(id=pk, owner=request.user)
            serializer = CardTemplateSerializers(card_template)
            return Response({"msg": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            pk = uuid.UUID(pk)
            card_template = CardTemplateSerializers.objects.get(id=pk)
            card_template.delete()
            return Response({"msg": f"card template with id {pk} is deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, *args, **kwargs):
        try:
            pk = uuid.UUID(pk)
            instance = CardTemplateSerializers.objects.get(id=pk)
            serializer = CardTemplateSerializers(instance=instance, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                return Response({"msg": f"card template with id {pk} is updated with {serializer.data}"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"error": f"data in post request is not appropriate"},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class NonCompanyCardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        validated_data = {}
        validated_data.update(request.data)
        owner = request.user
        validated_data.update({"owner": owner.id})
        serializer = NonCompanyCardSerializers(data=validated_data, partial=True)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"msg": f"card template is created with id {serializer.data}"},
                                status=status.HTTP_201_CREATED
                                )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, *args, **kwargs):
        try:
            pk = uuid.UUID(pk)
            non_company_card = NonCompanyCard.objects.get(id=pk, owner=request.user)
            serializer = NonCompanyCardSerializers(non_company_card)
            return Response({"msg": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            pk = uuid.UUID(pk)
            non_company_card = NonCompanyCardSerializers.objects.get(id=pk)
            non_company_card.delete()
            return Response({"msg": f"card template with id {pk} is deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, *args, **kwargs):
        try:
            pk = uuid.UUID(pk)
            instance = NonCompanyCardSerializers.objects.get(id=pk)
            serializer = NonCompanyCardSerializers(instance=instance, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                return Response({"msg": f"card template with id {pk} is updated with {serializer.data}"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"error": f"data in post request is not appropriate"},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


'''
company card related views
'''


class CompanyCardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        validated_data = {}
        owner = request.user
        try:
            validated_data.setdefault("owner", owner.id)
            validated_data.setdefault("card_template", uuid.UUID(request.data.get("card_template_id")))
            validated_data.setdefault("text", request.data.get("text", f"{owner.username}"))

            serializer = CompanyCardSerializer(data=validated_data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"msg": f"card template is created with id {serializer.data}"},
                                status=status.HTTP_201_CREATED
                                )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, *args, **kwargs):
        try:
            pk = uuid.UUID(pk)
            company_card = CompanyCard.objects.get(id=pk, owner=request.user)
            serializer = CompanyCardSerializer(company_card)
            return Response({"msg": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            pk = uuid.UUID(pk)
            company_card = CompanyCardSerializer.objects.get(id=pk)
            company_card.delete()
            return Response({"msg": f"card template with id {pk} is deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, *args, **kwargs):
        try:
            instance = CompanyCard.objects.get(id=pk)
            serializer = CompanyCardSerializer(instance=instance, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                return Response({"msg": f"card template with id {pk} is updated with {serializer.data}"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"error": f"data in post request is not appropriate"},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
