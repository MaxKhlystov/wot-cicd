from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tanks.views import BattleViewSet, health


router = DefaultRouter()
router.register(r"battles", BattleViewSet, basename="battle")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health", health),
    path("api/", include(router.urls)),
]
