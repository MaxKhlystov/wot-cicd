from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tanks.views import GameMapViewSet, TankViewSet, health


router = DefaultRouter()
router.register(r"tanks", TankViewSet, basename="tank")
router.register(r"maps", GameMapViewSet, basename="map")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health", health),
    path("api/", include(router.urls)),
]