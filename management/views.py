# from rest_framework.views import APIView
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from employee.serializers import EmployeeProfileSerializers
#
#
# '''
# add employee
# approve leaves
# create business card
# salary related info
# '''
#
# class AddEmployeeView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         response_status = None
#         response_data = None
#         if request.user.role.name == 'H':
#
#         else:
#             response_status = status.HTTP_403_FORBIDDEN
#             response_data = {"error":error_msg}
#
