from django.db.models import Q
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from businesscard.models import Card, Like, Comment, Post
from businesscard.serializers import LikeSerializer, CommentSerializer, CardSerializers, PostSerializer
from rest_framework import permissions
from core.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class PostCreateAPIView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        validated_data = {}
        validated_data.update(request.data)
        validated_data["owner"] = request.user
        serializer = self.serializer_class(data=validated_data, partial=True)
        try:
            if serializer.is_valid(raise_exception=True):
                print('before save')
                serializer.save()
                print('in after save')
                return Response({"msg": "post created successfully"}, status=status.HTTP_201_CREATED)
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
        post = Post.objects.get(id=pk)
        if post:
            post.delete()
            return Response({"msg": "post deleted successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "post not found for given pk"}, status=status.HTTP_404_NOT_FOUND)


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
            like = Like.objects.get_or_create(owner=request.user,post_id=request.data["post_id"])
            #like.post_id = request.data["post_id"]
            like.save()
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
            serialized = CommentSerializer(comments,many=True)
            return Response({"comments": serialized.data},status=status.HTTP_200_OK)
        else:
            return Response({"error": f"need post_id in request GET params"}, status=status.HTTP_204_NO_CONTENT)


    def post(self, request):
        if "post_id" in request.data:
            comment = Comment.objects.create(
                post_id=request.data.get("post_id"),
                content=request.data.get("content"),
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

    def get(self, request,pk=None, *args, **kwargs):
        comment = Comment.objects.get(id=pk)
        if comment:
            serialized = CommentSerializer(comment)
            return Response({"comment": serialized.data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": f"comment with id {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

