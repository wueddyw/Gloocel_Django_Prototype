from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Person

"""
Serializer for the Person model. Used for the RegisterAPI, but it
was never tested.
"""
class PersonSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        person = Person.objects.create_user(**validated_data)
        return person

    class Meta:
        model = Person

        fields = (
            'user.username',
            'first_name',
            'last_name',
            'email',
            'user.password',
        )

        # Ensures that the username and email are a unique pair
        validators = [
            UniqueTogetherValidator(
                queryset = Person.objects.all(),
                fields = ['user.username', 'email']
            )
        ]
