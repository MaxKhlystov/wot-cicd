from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tanks.views import (
    health,
    TankViewSet, PlayerViewSet, ClanViewSet,
    BattleViewSet, GameMapViewSet, AchievementViewSet,
)

router = DefaultRouter()
router.register(r"tanks", TankViewSet, basename="tank")
router.register(r"players", PlayerViewSet, basename="player")
router.register(r"clans", ClanViewSet, basename="clan")
router.register(r"battles", BattleViewSet, basename="battle")
router.register(r"maps", GameMapViewSet, basename="map")
router.register(r"achievements", AchievementViewSet, basename="achievement")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health", health),
    path("api/", include(router.urls)),
]
