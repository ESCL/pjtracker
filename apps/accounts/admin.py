from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase

from .models import Account, User


class AccountAdmin(admin.ModelAdmin):
    pass


class UserAdmin(UserAdminBase):
    pass


admin.site.register(Account, AccountAdmin)
admin.site.register(User, UserAdmin)
