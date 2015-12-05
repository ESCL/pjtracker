from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase

from .models import Account, User
from .forms import AdminUserCreationForm


class AccountAdmin(admin.ModelAdmin):
    pass


class UserAdmin(UserAdminBase):
    list_display = ('username', 'owner', 'email', 'first_name', 'last_name', 'is_staff',)
    add_form = AdminUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'owner', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'owner', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(Account, AccountAdmin)
admin.site.register(User, UserAdmin)
