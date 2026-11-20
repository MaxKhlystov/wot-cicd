from django.http import JsonResponse
from rest_framework import filters, viewsets

from .models import GameMap, Tank
from .serializers import GameMapSerializer, TankSerializer


def health(request):
    return JsonResponse({
        "status": "ok",
        "service": "catalog",
    })


class TankViewSet(viewsets.ModelViewSet):
    queryset = Tank.objects.all()
    serializer_class = TankSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "nation"]


class GameMapViewSet(viewsets.ModelViewSet):
    queryset = GameMap.objects.all()
    serializer_class = GameMapSerializer