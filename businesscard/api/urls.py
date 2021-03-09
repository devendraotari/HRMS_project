from django.urls import path
from businesscard.api.views import PostCreateAPIView, PostUpdateDeleteAPIView, PostListRetrieveView, LikeOnPostView, \
    UnLikeOnPostView, CommentOnPostView, CommentOnPostRetrieveUpdateDestroyView,CardTemplateAPIView

urlpatterns = [
    path("create-post/", PostCreateAPIView.as_view()),
    path("post-update/<str:pk>", PostUpdateDeleteAPIView.as_view()),
    path("post-delete/<str:pk>", PostUpdateDeleteAPIView.as_view()),
    path("post/", PostListRetrieveView.as_view()),
    path("post/<str:pk>", PostListRetrieveView.as_view()),
    path("like-post/", LikeOnPostView.as_view()),
    path("unlike-post/", UnLikeOnPostView.as_view()),
    path("comment-post/", CommentOnPostView.as_view()),
    path("comment-post/<str:pk>", CommentOnPostRetrieveUpdateDestroyView.as_view()),
    path("card-template/",CardTemplateAPIView.as_view()),
]
