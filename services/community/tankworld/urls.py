from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tanks.views import AchievementViewSet, ClanViewSet, PlayerViewSet, health


router = DefaultRouter()
router.register(r"players", PlayerViewSet, basename="player")
router.register(r"clans", ClanViewSet, basename="clan")
router.register(r"achievements", AchievementViewSet, basename="achievement")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health", health),
    path("api/", include(router.urls)),
]
