from django.contrib import admin

from .models import (Employee, Equipment, EquipmentType,
                     EquipmentTypeLabourType, ResourceCategory)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'full_name', 'company',
                    'position', 'owner',)


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'company', 'type', 'owner',)


class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'parent', 'owner',)


class EquipmentTypeLabourTypeAdmin(admin.ModelAdmin):
    list_display = ('equipment_type', 'labour_type', 'owner',)


class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'resource_type', 'owner',)


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(EquipmentType, EquipmentTypeAdmin)
admin.site.register(EquipmentTypeLabourType, EquipmentTypeLabourTypeAdmin)
admin.site.register(ResourceCategory, ResourceCategoryAdmin)
