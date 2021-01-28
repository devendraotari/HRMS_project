import uuid
from django.db import models
from django.contrib.auth import get_user_model

# from management.models import Company,SalaryInfo,LeaveInfo

User = get_user_model()


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, verbose_name="user", related_name="profile", on_delete=models.CASCADE
    )
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    profile_pic = models.FileField(upload_to="profile_pics/", blank=True, null=True)
    age = models.PositiveIntegerField(default=True, blank=True, null=True)
    gender = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"

    def __str__(self):
        return self.firstname

# class HRProfile(UserProfile):
#     company = models.OneToOneField(
#         Company,
#         verbose_name="company",
#         related_name="employees",
#         on_delete=models.CASCADE,
#         blank=True, null=True,
#     )
#     joining_date = models.DateTimeField(blank=True, null=True)
#     department = models.CharField(max_length=255, blank=True, null=True)
#     designation = models.CharField(max_length=255, blank=True, null=True)
#     salary_info = models.OneToOneField(SalaryInfo,related_name="hr_profile" ,blank=True)
#     leave_info = models.ForeignKey(LeaveInfo,related_name="hr_profile")
#
#
#
#     def __str__(self):
#         return
#
#     def __unicode__(self):
#         return
