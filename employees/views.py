from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from employees.models import Leave, EmployeeProfile
from employees.serializers import EmployeeProfileSerializers, LeaveSerializer
from core.permissions import IsOwnerOrReadOnly


class EmployeeProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        validated_data = {}
        validated_data.update(request.data)
        validated_data["user"] = request.user
        serialized = EmployeeProfileSerializers(data=validated_data, partial=True)
        try:
            if serialized.is_valid(raise_exception=True):
                serialized.save()
                return Response({"msg": "employee profile created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, *args, **kwargs):
        try:
            employee_profile = EmployeeProfile.objects.get(id=pk)
            if employee_profile:
                serialized = EmployeeProfileSerializers(employee_profile)
                return Response({"employee_profile": serialized.data}, status=status.HTTP_200_OK)
            else:
                return Response({"error": f"employee profile of id {pk} not found"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"{str(e)}"}, status=status.HTTP_200_OK)

    def put(self, request, pk=None, *args, **kwargs):

        try:
            employee_profile = EmployeeProfile.objects.get(id=pk)
            validated_data = {}
            validated_data.update(request.data)
            validated_data["user"] = request.user
            serialized = EmployeeProfileSerializers(data=validated_data, instance=employee_profile, partial=True)
            if serialized.is_valid(raise_exception=True):
                serialized.save()
                return Response({"employee_profile": serialized.data}, status=status.HTTP_200_OK)
            else:
                return Response({"error": f"employee profile of id {pk} not found"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"{str(e)}"}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return Response({"error": "method not allowed"}, status=status.HTTP_400_BAD_REQUEST)


class LeaveAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        validated_data = {}
        validated_data.update(request.data)
        validated_data["owner"] = request.owner
        serialized = LeaveSerializer(data=validated_data, partial=True)
        try:
            if serialized.is_valid(raise_exception=True):
                serialized.save()
                return Response({"msg": "Leave request created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, *args, **kwargs):
        validated_data = {}
        validated_data.update(request.data)
        validated_data["owner"] = request.owner
        try:
            leave = Leave.objects.get(id=pk)
            serialized = LeaveSerializer(data=validated_data, instance=leave, partial=True)
            if serialized.is_valid(raise_exception=True):
                serialized.save()
                return Response({"msg": "Leave request created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
