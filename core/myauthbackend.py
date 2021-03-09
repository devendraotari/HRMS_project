from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class EmailPhoneBackend(BaseBackend):
    """
    docstring
    """
    def authenticate(self,request, email=None,phone=None, password=None):
        # Check the username/password and return a user.
        my_user_model = get_user_model()
        user = None
        try:
            print(f"{request.data['phone']}")
            if request.data.get('email',None):
                print(f"custom auth call{email}")
                user = my_user_model.objects.get(email=request.data.get('email',None))
            if request.data.get('phone',None):
                print("in auth phone")
                user = my_user_model.objects.get(phone=request.data.get('phone',None))
                print(f"user{user}")
            if user.check_password(password):
                return user # return user on valid credentials
        except my_user_model.DoesNotExist as mmode:
            print(f"{mmode}")
            return None # return None if custom user model does not exist 
        except Exception as e:
            return None # return None in case of other exceptions

    def get_user(self, user_id):
        my_user_model = get_user_model()
        try:
            return my_user_model.objects.get(pk=user_id)
        except my_user_model.DoesNotExist:
            return None
        