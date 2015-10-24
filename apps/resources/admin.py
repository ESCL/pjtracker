from django.contrib import admin

from .models import Employee, Equipment, EquipmentType


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'full_name', 'nationality', 'company',
                    'project', 'position', 'location', 'lodging')


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'company', 'project', 'type', 'location',
                    'storage')


class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(EquipmentType, EquipmentTypeAdmin)
