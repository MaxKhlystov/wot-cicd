from rest_framework import serializers

from .models import Achievement, Clan, Player


class ClanSerializer(serializers.ModelSerializer):
    players_count = serializers.IntegerField(source="players.count", read_only=True)

    class Meta:
        model = Clan
        fields = "__all__"


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = "__all__"
