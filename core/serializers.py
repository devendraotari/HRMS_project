# from BusinessHRMS.core.models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from core.models import CustomUser as User,Role
from core.profile.models import UserProfile,HRProfile
from management.models import Company
from management.serializers import CompanySerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('firstname', 'lastname', 'age', 'gender',"profile_pic")



class UserRegistrationSerializer(serializers.ModelSerializer):

    profile = UserProfileSerializer(required=False,partial=True)
    role = serializers.CharField(max_length=255,required=False)
    email = serializers.CharField(max_length=255,required=False)
    phone = serializers.CharField(max_length=12,required=False)
    class Meta:
        model = User
        fields = ('username','email', 'password','phone',"role","profile")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        role = validated_data.pop('role',None)
        roleObj = None
        try:
            user = User.objects.create_user(**validated_data)
            if role == 'employee':
                roleObj = Role.objects.get_or_create(name="E")
                user.is_staff = False

            else:
                roleObj = Role.objects.get_or_create(name="R")
                user.is_staff = False

            UserProfile.objects.create(
                user=user,
                firstname=profile_data['firstname'],
                lastname=profile_data['lastname'],
                age=profile_data['age'],
                gender=profile_data['gender'],
                profile_pic=profile_data['profile_pic']
            )
            user.role = roleObj
            
            return user
        except ObjectDoesNotExist as e:
            raise e

# registration for hr

class HRProfileSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = HRProfile
        fields = ('firstname','lastname','age',"gender",
                "profile_pic","company",'department','designation')
    
    def create(self, validated_data):
        company_name  = validated_data.pop('company',None)
        try:
            company = Company.objects.get_or_create(company_name=company_name)
            validated_data.setdefault('company',company)
            hrprofile = HRProfile.objects.create(**validated_data)
        return hrprofile


class HRUserRegistration(serializers.ModelSerializer):
    profile = HRProfileSerializer()

    class Meta:
        model = User
        fields = ('username','email', 'password','phone',"profile")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        company_name  = profile_data.pop('company',None)
        role_name = validated_data.pop('role',None)
        try:
            user = User.objects.create_user(**validated_data)
            roleObj = Role.objects.get_or_create(name="H")
            user.is_staff = True
            user.role = roleObj
            company = Company.objects.get_or_create(company_name=company_name)
            profile_data.setdefault('company',company)
            HRProfile.objects.create(
                user=user,
                firstname=profile_data['firstname'],
                lastname=profile_data['lastname'],
                age=profile_data['age'],
                gender=profile_data['gender'],
                profile_pic=profile_data['profile_pic'],
                company=profile_data['company'],
                department=profile_data['department'],
                designation=profile_data['designation'],
            )
            return user
        except ObjectDoesNotExist as e:
            raise e





class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255,required=False)
    phone = serializers.CharField(max_length=12,required=False)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        phone = data.get("phone", None)
        password = data.get("password", None)
        user = None
        try:
            if email:
                user = User.objects.get(email=email)
            elif phone:
                user = User.objects.get(phone=phone)
                print(f"{phone}{password}")
            if user and check_password(password, user.password):
                payload = JWT_PAYLOAD_HANDLER(user)
                jwt_token = JWT_ENCODE_HANDLER(payload)
                update_last_login(None, user)
            else:
                raise serializers.ValidationError(
                    'A user with given credentials not found.'
                )
        except User.DoesNotExist:

            raise serializers.ValidationError(
                'A user with given credentials not found.'
            )
        except Exception as e:
            print(f"{e}")
            raise e
        
        return {
            'email':user.email,
            'token': jwt_token
        }