from rest_framework import serializers
from .models import Device

class DeviceSerializer(serializers.ModelSerializer):
 
 class Meta:
  model = Device
  fields = ('device_name', 'device_type', 'api_key')
