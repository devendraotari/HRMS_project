from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from employees.models import LeaveRequest
from employees.serializers import LeaveRequestSerializer

class LeaveRequestViewSet(viewsets.ModelViewSet):
    model = LeaveRequest
    permissions = [IsAuthenticated]
    queryset = LeaveRequest.objects.all()

    def create(self,request,*args,**kwargs):
        user = request.user
        valid_data = request.data
        valid_data['user'] = user
        serializer = self.serializer_class(data=valid_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def delete(self,request,pk=None,*args,**kwargs):
        leave_request = LeaveRequest.objects.get(id=pk)
        leave_request.delete()


