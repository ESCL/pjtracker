from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Account, UserProfile


class AccountAdmin(admin.ModelAdmin):
    pass


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserWithProfileAdmin(UserAdmin):
    inlines = (UserProfileInline,)


admin.site.register(Account, AccountAdmin)
admin.site.unregister(User)
admin.site.register(User, UserWithProfileAdmin)
