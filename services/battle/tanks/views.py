from django.http import JsonResponse
from rest_framework import filters, viewsets

from .models import Battle
from .serializers import BattleSerializer


def health(request):
    return JsonResponse({"status": "ok", "service": "battle"})


class BattleViewSet(viewsets.ModelViewSet):
    queryset = Battle.objects.all()
    serializer_class = BattleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["status", "result"]
