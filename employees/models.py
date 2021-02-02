import uuid
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class EmployeeProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name="emp_profile", on_delete=models.CASCADE)
    joining_date = models.DateTimeField(blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    salary = models.PositiveIntegerField(default=0, blank=True, null=True)
    Profile_picture = models.ImageField(upload_to='employee/images/')


class Leave(models.Model):
    from_date = models.DateTimeField(max_length=20)
    till_date = models.DateTimeField(max_length=20)
    emp_name = models.CharField(max_length=20)
    subject = models.CharField(max_length=100)
    explain_Reason = models.CharField(max_length=200)
    document = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)
    owner = models.ForeignKey(User, related_name="leaves", on_delete=models.CASCADE)

    def __str__(self):
        return self.emp_name



