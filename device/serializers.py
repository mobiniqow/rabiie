from rest_framework import serializers
from .models import Relay12, Relay6


class Relay6Serializer(serializers.ModelSerializer):
    class Meta:
        model = Relay6
        fields = '__all__'
        read_only_fields = ("id", "product_id", "user")


class Relay12Serializer(serializers.ModelSerializer):
    class Meta:
        model = Relay12
        fields = '__all__'
        read_only_fields = ("id", "product_id", "user")
