from django.http import JsonResponse
from rest_framework import filters, viewsets

from .models import Achievement, Clan, Player
from .serializers import AchievementSerializer, ClanSerializer, PlayerSerializer


def health(request):
    return JsonResponse({"status": "ok", "service": "community"})


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["nickname"]


class ClanViewSet(viewsets.ModelViewSet):
    queryset = Clan.objects.all()
    serializer_class = ClanSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
