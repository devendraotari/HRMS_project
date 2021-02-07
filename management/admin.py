from django.contrib import admin

from management.models import Employee, Leave, Notify, Emails, Compose, ViewMail, ContactsDetails

admin.site.register(Employee)
admin.site.register(Leave)
admin.site.register(Notify)
admin.site.register(Emails)
admin.site.register(Compose)
admin.site.register(ViewMail)
admin.site.register(ContactsDetails)
