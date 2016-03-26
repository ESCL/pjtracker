from django.contrib import admin

from .models import Employee, Equipment, EquipmentType, EquipmentTypeLabourType


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('owner', 'identifier', 'full_name', 'company', 'position', 'project',)


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('owner', 'identifier', 'company', 'type', 'project',)


class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ('owner', 'code', 'name', 'parent',)


class EquipmentTypeLabourTypeAdmin(admin.ModelAdmin):
    list_display = ('owner', 'equipment_type', 'labour_type',)


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(EquipmentType, EquipmentTypeAdmin)
admin.site.register(EquipmentTypeLabourType, EquipmentTypeLabourTypeAdmin)
