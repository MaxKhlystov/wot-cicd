from rest_framework import serializers

from .models import GameMap, Tank


class TankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tank
        fields = "__all__"


class GameMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameMap
        fields = "__all__"