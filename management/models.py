# import uuid
# from django.db import models
# from django.contrib.auth import get_user_model
# from django.core.validators import RegexValidator
# # from employees.models import LeaveRequest
#
#
# PHONE_REGEX = "^[0-9]*$"
# User = get_user_model()
#
#
# class Company(models.Model):
#     name = models.CharField(max_length=255, blank=True, null=True)
#     address = models.CharField(max_length=255, blank=True, null=True)
#     website = models.CharField(max_length=255, blank=True, null=True)
#     logo = models.FileField(upload_to="company/logo/", blank=True, null=True)
#     phone = models.CharField(
#         max_length=12, validators=[RegexValidator(PHONE_REGEX)], blank=True, null=True
#     )
#
#     def __str__(self):
#         return self.name
#
#
# class SalaryInfo(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     # admin who created or updated the salary info
#     updated_by = models.ForeignKey(
#         User,
#         verbose_name="updated_by",
#         related_name="salary_info_updated",
#         on_delete=models.CASCADE,
#     )
#     # when the last time employee was paid
#     last_paid = models.DateTimeField(blank=True, null=True)
#     last_paid_amount = models.FloatField(blank=True, null=True)
#
#     # salary package per annum
#     current_package = models.FloatField(blank=True, null=True)
#
#     # amount to be paid next (mothly salary or In hand)
#     monthly_salary = models.FloatField(blank=True, null=True)
#
#     # if received any extra bonus
#     bonus = models.FloatField(blank=True, null=True)
#
#     # if paid by any HR
#     paid_by = models.ForeignKey(
#         User,
#         verbose_name="user",
#         related_name="salary_paid_by",
#         on_delete=models.SET_NULL,
#         blank=True, null=True
#     )
#
#     # employee to whom salary will be paid to
#     employee = models.OneToOneField(
#         User, verbose_name="user", related_name="salary_info",
#         on_delete=models.SET_NULL,blank=True, null=True
#     )
#
#     # in percentage
#     last_increment = models.FloatField(default=0.0, blank=True, null=True)
#
#     # date of last appraisal
#     incremented_on = models.DateTimeField(blank=True, null=True)
#
#     def __str__(self):
#         return self.employee
#
#     class Meta:
#         permissions = (
#             ("create_salary_info","can create salary info"),
#             ("read_salary_info","can create salary info"),
#             ("update_salary_info","can create salary info"),
#             ("delete_salary_info","can create salary info"),
#         )
#
# # class LeaveInfo(models.Model):
# #     created_at = models.DateTimeField(auto_now_add=True)
# #     updated_at = models.DateTimeField(auto_now=True)
# #     approved_at = models.DateTimeField(blank=True, null=True)
# #
# #     leave_request = models.OneToOneField(
# #         LeaveRequest,
# #         on_delete=models.SET_NULL,
# #         related_name="leave_info",
# #         blank=True, null=True,
# #     )
# #     approver = models.ForeignKey(
# #         User,
# #         related_name="+",
# #         on_delete=models.SET_NULL,
# #         blank=True, null=True
# #
# #     )
# #     from_date = models.DateTimeField(blank=True, null=True)
# #     to_date = models.DateTimeField(blank=True, null=True)
# #     is_approved = models.BooleanField(default=False)
# #
# #     def __str__(self):
# #         return str(self.id)
# #
# #     class Meta:
# #         permissions = (
# #             ("create_leave_info","can create salary info"),
# #             ("read_leave_info","can create salary info"),
# #             ("update_leave_info","can create salary info"),
# #             ("delete_leave_info","can create salary info"),
# #         )
#
#
# class UserDocument(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     user = models.ForeignKey(User, related_name="documents",blank=True, null=True,on_delete=models.SET_NULL)
#     name = models.CharField(max_length=255, blank=True, null=True)
#     document = models.FileField(upload_to="user/docs", max_length=100)
#
#     def __str__(self):
#         return
#
#     def __unicode__(self):
#         return
#
#
#
