import uuid
from django.db import models
from django.contrib.auth import get_user_model
from core.profile.models import UserProfile 

from management.models import Company,SalaryInfo,LeaveInfo

User = get_user_model()


class EmployeeProfile(UserProfile):    
    company = models.OneToOneField(
        Company,
        verbose_name="company",
        related_name="employees",
        on_delete=models.CASCADE,
        blank=True, null=True,
    )
    joining_date = models.DateTimeField(blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)


class LeaveRequest(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    employee = models.ForeignKey(User, related_name='leave_request', on_delete=models.CASCADE,blank=True, null=True)
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    subject = models.CharField(max_length=255,blank=True, null=True)
    reason = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.is_approved)
    
    class Meta:
        permissions = (
            ("create_leave_request","can create leave request"),
            ("read_leave_request","can create leave request"),
            ("update_leave_request","can create leave request"),
            ("delete_leave_request","can create leave request"),
        )






