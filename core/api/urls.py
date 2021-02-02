from django.shortcuts import render

# Create your views here.

"""
Here the 
login 
Registration
authentication
"""
from django.urls import path
from rest_framework_jwt import views as jwt_views
from core.views import (
    UserRegistrationView,
    UserLoginView,
    UserForgotPasswordView,
    # HRUserRegistrationView,
)

urlpatterns = [
    # Your URLs...
    path("token/", jwt_views.ObtainJSONWebToken.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.RefreshJSONWebToken.as_view(), name="token_refresh"),
    path("register/", UserRegistrationView.as_view()),
    # path("register-hr/",HRUserRegistrationView.as_view()),
    path("login/", UserLoginView.as_view()),

    # not implemented
    # path('forgotpassword/',UserForgotPasswordView.as_view()),
    # path('changeusername/')
    # path('changepssword/')
]
