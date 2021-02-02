from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from core.profile.models import UserProfile
from core.models import CustomUser

admin.site.register(CustomUser)
admin.site.register(UserProfile)

