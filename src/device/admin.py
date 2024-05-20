from django.contrib import admin
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
 list_display = ("device_name", "device_type", "api_key", "door")
