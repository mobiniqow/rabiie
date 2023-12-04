from rest_framework import serializers

from user_relations.models import UserChild


class UserChildSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserChild
        fields = "__all__"
