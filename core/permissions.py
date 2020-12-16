from rest_framework.permissions import BasePermission

class IsEmployee(BasePermission):

    def __init__(self, action, entity):
        self.action = action
        self.entity = entity

    def has_permission(self, request, view):
        print(self.action)
        print(self.entity)
        if request.user and request.user.role.access_rights.filter(action=self.action,entity=self.entity):
            print('permission granted')            
            return True
        else:
            return False