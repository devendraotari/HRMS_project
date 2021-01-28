# from rest_framework import serializers
# from management.models import Company
#
# class CompanySerializer(serializers.ModelSerializer):
#
#     # profile = UserSerializer(required=False)
#     name = serializers.CharField(max_length=255,required=False)
#     address = serializers.CharField(max_length=255,required=False)
#     website = serializers.CharField(max_length=255,required=False)
#     logo = serializers.FileField(upload_to="company/logo/",required=False)
#     phone = serializers.CharField(max_length=255,required=False)
#     class Meta:
#         model = Company
#         fields = ("name", "address","website","logo","phone")
#
#     def create(self,validated_data):
#         company = Company.objects.create(**validated_data)
#         return company