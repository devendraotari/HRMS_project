# Create your views here.

'''
Here the 
login 
Registration
authentication
'''
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from core.api.serializers import UserRegistrationSerializer, UserLoginSerializer
from core.models import CustomUser as User


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, partial=True)
        print(f"{request.data}")
        try:
            if serializer.is_valid(raise_exception=True):
                print("Serializer")
                serializer.save()
                status_code = status.HTTP_201_CREATED
                response = {
                    'success': 'True',
                    'status code': status_code,
                    'message': 'User registered  successfully',
                }
            else:

                status_code = status.HTTP_406_NOT_ACCEPTABLE
                response = {
                    'success': 'False',
                    'status code': status_code,
                    'message': 'User registration  failed',
                }
            return Response(response, status=status_code)
        except Exception as e:
            status_code = status.HTTP_406_NOT_ACCEPTABLE
            response = {
                'success': 'False',
                'status code': status_code,
                'message': f'{str(e)}',
            }
            return Response(response, status=status_code)


# hr registration for

# class HRUserRegistrationView(CreateAPIView):
#     serializer_class = HRUserRegistrationSerializer
#     permission_classes = (AllowAny,)
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data, partial=True)
#         print(f"{request.data}")
#         try:
#             if serializer.is_valid(raise_exception=True):
#                 print("Serializer")
#                 serializer.save()
#                 status_code = status.HTTP_201_CREATED
#                 response = {
#                     'success': 'True',
#                     'status code': status_code,
#                     'message': 'HR User registered  successfully',
#                 }
#             else:
#
#                 status_code = status.HTTP_406_NOT_ACCEPTABLE
#                 response = {
#                     'success': 'False',
#                     'status code': status_code,
#                     'message': 'HR User registeration  failed',
#                 }
#             return Response(response, status=status_code)
#         except Exception as e:
#             status_code = status.HTTP_406_NOT_ACCEPTABLE
#             response = {
#                 'success': 'False',
#                 'status code': status_code,
#                 'message': f'{str(e)}',
#             }
#             return Response(response, status=status_code)


class UserLoginView(RetrieveAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token': serializer.data['token'],
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


class UserForgotPasswordView(APIView):

    def post(self, request):
        pass
