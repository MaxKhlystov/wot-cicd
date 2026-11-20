import pytest
from rest_framework.test import APIClient

from .models import Achievement, Clan, Player


@pytest.fixture
def api():
    return APIClient()


@pytest.fixture
def clan():
    return Clan.objects.create(tag="IRK", name="Irkutsk Wolves")


@pytest.fixture
def player(clan):
    return Player.objects.create(nickname="Tankist", level=10, clan=clan)


@pytest.mark.django_db
def test_health(api):
    response = api.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "community"}


@pytest.mark.django_db
def test_clan_create(api):
    response = api.post("/api/clans/", {"tag": "BAIK", "name": "Baikal"}, format="json")
    assert response.status_code == 201


@pytest.mark.django_db
def test_clan_players_count(api, clan, player):
    response = api.get(f"/api/clans/{clan.id}/")
    assert response.status_code == 200
    assert response.json()["players_count"] == 1


@pytest.mark.django_db
def test_player_create(api):
    response = api.post(
        "/api/players/",
        {"nickname": "NewPlayer", "level": 5, "favorite_tank_id": 7},
        format="json",
    )
    assert response.status_code == 201
    assert response.json()["favorite_tank_id"] == 7


@pytest.mark.django_db
def test_player_search(api, player):
    response = api.get("/api/players/?search=Tank")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_player_update(api, player):
    response = api.patch(f"/api/players/{player.id}/", {"level": 11}, format="json")
    assert response.status_code == 200
    assert response.json()["level"] == 11


@pytest.mark.django_db
def test_achievement_create(api):
    response = api.post(
        "/api/achievements/",
        {"code": "sniper", "title": "Sniper"},
        format="json",
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_achievement_assign(api, player):
    achievement = Achievement.objects.create(code="veteran", title="Veteran")
    response = api.patch(
        f"/api/achievements/{achievement.id}/",
        {"players": [player.id]},
        format="json",
    )
    assert response.status_code == 200
    assert player in achievement.players.all()
