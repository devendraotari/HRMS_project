import uuid
from django.db import models
from django.core.validators import RegexValidator

from django.contrib.auth.models import (
		BaseUserManager, AbstractBaseUser
	)

# USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'

class CustomUserManager(BaseUserManager):
	def create_user(self, email, password=None):
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
					email = self.normalize_email(email)
				)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password=None):
		user = self.create_user(
				email, password=password
			)
		user.is_admin = True
		user.is_staff = True
		user.save(using=self._db)
		return user



class CustomUser(AbstractBaseUser):
	id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
	email = models.EmailField(
			max_length=255,
			unique=True,
			verbose_name='email address'
		)
	
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	objects = CustomUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	def __str__(self):
		return self.email

	def get_short_name(self):
		# The user is identified by their email address
		return self.email


	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True


