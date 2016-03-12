from django.contrib import admin

from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'event_target', 'event_type', 'timestamp',
                    'status',)


admin.site.register(Notification, NotificationAdmin)
