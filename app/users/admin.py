from django.contrib import admin

from .models import Invitation, LdapGroup, LdapUser

# Register your models here.
admin.site.register(Invitation)
admin.site.register(LdapGroup)
admin.site.register(LdapUser)