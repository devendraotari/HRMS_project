from rest_framework import serializers
from employees.models import Leave, EmployeeProfile
from django.contrib.auth import get_user_model

User = get_user_model()


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = ("from_date", "to_date", "subject", "reason")

    def create(self, validated_data) -> Leave:
        user = validated_data.pop("user")
        leave_request = Leave.objects.create(**validated_data)
        leave_request.employee = user
        return leave_request

    def update(self, instance, validated_data) -> Leave:
        instance.from_date = validated_data.get("from_date", instance.from_date)
        instance.to_date = validated_data.get("to_date", instance.to_date)
        instance.subject = validated_data.get("subject", instance.subject)
        instance.reason = validated_data.get("reason", instance.reason)
        return instance


class EmployeeProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = (
            "id",
            "user",
            "joining_date",
            "designation",
            "department",
            "salary",
            "profile_pic",
        )

    def create(self, validated_data) -> EmployeeProfile:
        try:
            employee_profile = EmployeeProfile.objects.create(**validated_data)
            return employee_profile
        except Exception as e:
            raise e

    def update(self, instance, validated_data) -> EmployeeProfile:
        instance.joining_date = validated_data.get("joining_date", instance.joining_date)
        instance.designation = validated_data.get("designation", instance.designation)
        instance.department = validated_data.get("department", instance.department)
        instance.salary = validated_data.get("salary", instance.salary)
        instance.profile_pic = validated_data.get("profile_pic", instance.profile_pic)
        return instance
