from django.contrib import admin
from . import models


admin.site.register(models.Blacksmith)
admin.site.register(models.ArmorType)
admin.site.register(models.Armor)
admin.site.register(models.ArmorOrder)
