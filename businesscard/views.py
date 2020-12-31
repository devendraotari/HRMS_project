from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, viewsets
from businesscard.models import Card,Like,Comment,Post
from businesscard.serializers import LikeSerializer,CommentSerializer,CardSerializers
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class PostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs ):
        request_data = request.data
        


