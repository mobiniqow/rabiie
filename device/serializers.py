from rest_framework import serializers
from .models import Relay12, Relay6


class Relay6Serializer(serializers.ModelSerializer):
    class Meta:
        model = Relay6
        fields = '__all__'


class Relay12Serializer(serializers.ModelSerializer):
    class Meta:
        model = Relay12
        fields = '__all__'
