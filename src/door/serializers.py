from location.serializers import LocationSerializer
from rest_framework import serializers
from .models import Door

class DoorSerializer(serializers.ModelSerializer):

    location = LocationSerializer()

    class Meta:
        model = Door

        fields = (
            'id',
            'door_name',
            'door_type',
            'location'
        )