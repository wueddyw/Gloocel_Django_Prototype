from django.contrib import admin
from .models import Door

@admin.register(Door)
class DoorAdmin(admin.ModelAdmin):
 list_display = ("door_name", "door_type", "location", "message")
