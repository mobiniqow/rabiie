from rest_framework import serializers
from .models import EVENT


class EVENTSerializer(serializers.ModelSerializer):
    class Meta:
        model = EVENT
        fields = '__all__'
