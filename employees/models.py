from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from management.models import Company

PHONE_REGEX = "^[0-9]*$"
User = get_user_model()


class Employee(models.Model):
    user = models.OneToOneField(
        User, verbose_name="user", related_name="hrprofile", on_delete=models.CASCADE
    )
    company = models.OneToOneField(
        Company,
        verbose_name="company",
        related_name="hrprofile",
        on_delete=models.CASCADE,
    )
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    profile_pic = models.FileField(upload_to="company/logo/", blank=True, null=True)
    phone = models.CharField(
        max_length=12,
        validators=[
            RegexValidator(regex=PHONE_REGEX, message="phone number string not valid")
        ],
        blank=True,
        null=True,
    )
    

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return self.name
