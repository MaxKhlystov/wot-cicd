from rest_framework import serializers
from .models import Tank, Player, Clan, Battle, GameMap, Achievement


class TankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tank
        fields = "__all__"


class ClanSerializer(serializers.ModelSerializer):
    players_count = serializers.IntegerField(source="players.count", read_only=True)

    class Meta:
        model = Clan
        fields = "__all__"


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"


class GameMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameMap
        fields = "__all__"


class BattleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battle
        fields = "__all__"


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = "__all__"
