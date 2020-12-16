from django.shortcuts import render

# Create your views here.

'''
Here the 
login 
Registration
authentication
'''
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from core.views import UserRegistrationView,UserLoginView
urlpatterns = [
    # Your URLs...
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',UserRegistrationView.as_view()),
    path('login/',UserLoginView.as_view()),


]