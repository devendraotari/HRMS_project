import uuid
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
		BaseUserManager, AbstractBaseUser
	)

ROLE_CHOICES = (
        ('H', 'HR-admin'),
        ('E', 'Employee'),
		('R','Regular'),
		('S', 'Supervisor'),
    )


class Role(models.Model):
	name = models.CharField(max_length=2,choices=ROLE_CHOICES,unique=True)
	description = models.CharField(max_length=100,blank=True, null=True)
	


# USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'
PHONE_REGEX = "^[0-9]*$"
class CustomUserManager(BaseUserManager):
	def create_user(
		self, 
		username=None, 
		email=None, 
		phone=None, 
		password=None,
		role_name='R'
	):
		user=None
		if not email and not phone:
			raise ValueError('Users must have an email address or phone number')
		
		if username:
			user = self.model(
						username=username,
						email = self.normalize_email(email) if  email else None,
					)
		if email:
			user = self.model(
						username=self.normalize_email(email),
						email = self.normalize_email(email),
						phone = phone
					)
		if phone:
			user = self.model(
						username=phone,
						email = self.normalize_email(email) if  email else None,
						phone = phone
					)
		user.set_password(password)
		role = Role.objects.get_or_create(name=role_name)
		user.role = role
		user.save(using=self._db)
		return user

	def create_superuser(self, username, password=None):
		user = self.create_user(
				username=username,
				email = self.normalize_email(username),				
				password=password
			)
		user.is_admin = True
		user.is_staff = True
		role = Role.objects.get_or_create(name="S")
		user.role = role
		user.save(using=self._db)
		return user



class CustomUser(AbstractBaseUser):
	id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
	username = models.CharField(max_length=255,unique=True)
	email = models.EmailField(
			max_length=255,
			verbose_name='email address',
        	blank=True,
        	null=True,
		)
	phone = models.CharField(
        max_length=12,
        validators=[
            RegexValidator(regex=PHONE_REGEX, message="phone number string not valid")
        ],
        blank=True,
        null=True,
    )

	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	role = models.ForeignKey(Role, related_name="user",blank=True, null=True)
	objects = CustomUserManager()
	
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []


	class Meta:
		ordering = ["username"]
	def clean(self):
		if self.email is None and self.phone is None:
			raise ValidationError({'non_field': 'email or phone number is required for registering.'})
	
	def __str__(self):
		return str(self.id)

	def get_short_name(self):
		# The user is identified by their email address
		return str(self.email)


	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		
		return True


	def has_model_permissions( entity, model, perms, app ):
		for p in perms:
			if not entity.has_perm( "%s.%s_%s" % ( app, p, model.__name__ ) ):
				return False
			return True

