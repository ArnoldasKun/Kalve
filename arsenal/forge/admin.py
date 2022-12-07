from django.contrib import admin
from . import models


class ArmorOrderInline(admin.TabularInline):
    model = models.ArmorOrder
    extra = 0
    can_delete = False


class ArmorAdmin(admin.ModelAdmin):
    list_display = ('title', 'blacksmith', 'display_armor_type')
    inlines = (ArmorOrderInline, )


class ArmorOrderAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'armor', 'status', 'due_back', 'client')
    list_filter = ('status', 'due_back')
    readonly_fields = ('unique_id', 'is_overdue' )
    search_fields = ('unique_id', 'armor__title', 'armor__blacksmith__last_name__exact', 'client__last_name')
    list_editable = ('status', 'due_back', 'client')

    fieldsets = (
        ('General', {'fields': ('unique_id', 'armor')}),
        ('Availability', {'fields': (('status', 'due_back', 'is_overdue'), 'client')}),
    )


class BlacksmithAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'display_armors')
    list_display_links = ('last_name', )


admin.site.register(models.Blacksmith, BlacksmithAdmin)
admin.site.register(models.ArmorType)
admin.site.register(models.Armor, ArmorAdmin)
admin.site.register(models.ArmorOrder, ArmorOrderAdmin)
