# from rest_framework.permissions import BasePermission

# class IsEmployee(BasePermission):

#     def __init__(self, action, entity):
#         self.action = action
#         self.entity = entity

#     def has_permission(self, request, view):
#         print(self.action)
#         print(self.entity)
#         if request.user and request.user.role.access_rights.filter(action=self.action,entity=self.entity):
#             print('permission granted')            
#             return True
#         else:
#             return False

# class IsHRAdmin(BasePermission):

#     def __init__(self, action, entity):
#         self.action = action
#         self.entity = entity

#     def has_permission(self, request, view):
#         print(self.action)
#         print(self.entity)
#         if request.user and request.user.role.access_rights.filter(action=self.action,entity=self.entity):
#             print('permission granted')            
#             return True
#         else:
#             return False

# from management.models import SalaryInfo,LeaveInfo
# from employee.models import LeaveRequest
# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType

# ct_salary = ContentType.objects.get_for_model(SalaryInfo)
# ct_leave_request = ContentType.objects.get_for_model(LeaveRequest)
# ct_leaveinfo = ContentType.objects.get_for_model(LeaveInfo)

# salary_permission = Permission.objects.create(codename='can_publish',
#                                        name='Can Publish book',
#                                        content_type=content_type)