from django.http import JsonResponse
from rest_framework import viewsets, filters
from .models import Tank, Player, Clan, Battle, GameMap, Achievement
from .serializers import (
    TankSerializer, PlayerSerializer, ClanSerializer,
    BattleSerializer, GameMapSerializer, AchievementSerializer,
)


def health(request):
    return JsonResponse({"status": "ok", "game": "tankworld"})


class TankViewSet(viewsets.ModelViewSet):
    queryset = Tank.objects.all()
    serializer_class = TankSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "nation"]


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["nickname"]


class ClanViewSet(viewsets.ModelViewSet):
    queryset = Clan.objects.all()
    serializer_class = ClanSerializer


class BattleViewSet(viewsets.ModelViewSet):
    queryset = Battle.objects.all()
    serializer_class = BattleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["status", "result"]


class GameMapViewSet(viewsets.ModelViewSet):
    queryset = GameMap.objects.all()
    serializer_class = GameMapSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
