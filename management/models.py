from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

PHONE_REGEX = "^[0-9]*$"
User = get_user_model()


class Company(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    logo = models.FileField(upload_to="company/logo/", blank=True, null=True)
    phone = models.CharField(
        max_length=12, validators=[RegexValidator(PHONE_REGEX)], blank=True, null=True
    )

    def __str__(self):
        return self.name


class HRProfile(models.Model):
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
    profile_pic = models.FileField(upload_to="profile_pic/", blank=True, null=True)
    phone = models.CharField(
        max_length=12,
        validators=[
            RegexValidator(regex=PHONE_REGEX, message="phone number string not valid")
        ],
        blank=True,
        null=True,
    )

