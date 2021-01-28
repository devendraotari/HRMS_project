# from rest_framework import serializers
# from employee.models import LeaveRequest, LeaveInfo, EmployeeProfile
# from management.serializers import CompanySerializer
# from management.models import Company
# from core.serializers import UserRegistrationSerializer
# from django.contrib.auth import get_user_model
#
# User = get_user_model()
#
# # class
#
#
# class LeaveRequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LeaveRequest
#         fields = ("from_date", "to_date", "subject", "reason")
#
#     def create(self, validated_data):
#         user = validated_data.pop("user")
#         leave_request = LeaveRequest.objects.create(**validated_data)
#         leave_request.employee = user
#         return leave_request
#
#     def update(self, validated_data):
#         pass
#
#
# class EmployeeProfileSerializers(serializers.ModelSerializer):
#     is_existing = serializers.BooleanField(required=False)
#     user_id = serializers.CharField(required=False)
#     company = CompanySerializer()
#
#     class Meta:
#         model = EmployeeProfile
#         fields = (
#             "joining_date",
#             "designation",
#             "department",
#             "company",
#             "user_email",
#             "is_existing",
#         )
#
#     def create(self, validated_data):
#         is_existing = bool(validated_data.pop("is_existing", None))
#         company_name = validated_data.pop('company')
#         try:
#             if is_existing:
#                 user_id = validated_data.pop('user_id',None)
#                 userObj = User.objects.get(id=user_id)
#                 profileObj = userObj.profile
#                 validated_data.setdefault('firstname',profileObj.firstname,None)
#                 validated_data.setdefault('lastname',profileObj.lastname,None)
#                 validated_data.setdefault('age',profileObj.age,None)
#                 validated_data.setdefault('gender',profileObj.gender,None)
#                 validated_data.setdefault('profile_pic',profileObj.profile_pic,None)
#
#                 companyObj = Company.objects.get(name=company_name)
#                 validated_data.setdefault('company',companyObj)
#                 employeeProfileObj = EmployeeProfile.objects.create(**validated_data)
#                 return employeeProfileObj
#
#         except Exception as e:
#             raise e
#
#
#
