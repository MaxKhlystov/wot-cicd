import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Tank, Player, Clan, GameMap, Battle, Achievement


@pytest.fixture
def api():
    return APIClient()


@pytest.fixture
def tank():
    return Tank.objects.create(name="T-34-85", nation="СССР", tank_type="MT", tier=6, hp=960, damage=200)


@pytest.fixture
def player():
    return Player.objects.create(nickname="Krasnoarmeets", level=10, experience=50000)


@pytest.fixture
def clan():
    return Clan.objects.create(tag="IRK", name="Иркутские волки")


@pytest.fixture
def game_map():
    return GameMap.objects.create(name="Харьков", mode="Стандартный бой", size_km=1.2)


# ---------- Health ----------

@pytest.mark.django_db
def test_health(api):
    r = api.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


# ---------- TANKS CRUD (5) ----------

@pytest.mark.django_db
def test_tank_create(api):
    r = api.post("/api/tanks/", {"name": "IS-7", "nation": "СССР", "tier": 10, "damage": 500}, format="json")
    assert r.status_code == 201
    assert r.json()["name"] == "IS-7"


@pytest.mark.django_db
def test_tank_list(api, tank):
    r = api.get("/api/tanks/")
    assert r.status_code == 200
    assert len(r.json()) == 1


@pytest.mark.django_db
def test_tank_retrieve(api, tank):
    r = api.get(f"/api/tanks/{tank.id}/")
    assert r.status_code == 200
    assert r.json()["name"] == "T-34-85"


@pytest.mark.django_db
def test_tank_update(api, tank):
    r = api.put(f"/api/tanks/{tank.id}/", {"name": "T-34-85", "nation": "СССР", "tank_type": "MT",
                                          "tier": 6, "hp": 1100, "damage": 220}, format="json")
    assert r.status_code == 200
    assert r.json()["hp"] == 1100


@pytest.mark.django_db
def test_tank_delete(api, tank):
    r = api.delete(f"/api/tanks/{tank.id}/")
    assert r.status_code == 204
    assert Tank.objects.count() == 0


# ---------- PLAYERS CRUD (5) ----------

@pytest.mark.django_db
def test_player_create(api):
    r = api.post("/api/players/", {"nickname": "Tankist_99", "level": 5}, format="json")
    assert r.status_code == 201


@pytest.mark.django_db
def test_player_list(api, player):
    r = api.get("/api/players/")
    assert r.status_code == 200
    assert r.json()[0]["nickname"] == "Krasnoarmeets"


@pytest.mark.django_db
def test_player_retrieve(api, player):
    r = api.get(f"/api/players/{player.id}/")
    assert r.status_code == 200


@pytest.mark.django_db
def test_player_update(api, player):
    r = api.patch(f"/api/players/{player.id}/", {"level": 11}, format="json")
    assert r.status_code == 200
    assert r.json()["level"] == 11


@pytest.mark.django_db
def test_player_delete(api, player):
    r = api.delete(f"/api/players/{player.id}/")
    assert r.status_code == 204


# ---------- CLANS CRUD (5) ----------

@pytest.mark.django_db
def test_clan_create(api):
    r = api.post("/api/clans/", {"tag": "BAIK", "name": "Байкальские медведи"}, format="json")
    assert r.status_code == 201


@pytest.mark.django_db
def test_clan_list(api, clan):
    r = api.get("/api/clans/")
    assert r.status_code == 200


@pytest.mark.django_db
def test_clan_retrieve(api, clan):
    r = api.get(f"/api/clans/{clan.id}/")
    assert r.json()["tag"] == "IRK"


@pytest.mark.django_db
def test_clan_update(api, clan):
    r = api.patch(f"/api/clans/{clan.id}/", {"rating": 1500}, format="json")
    assert r.status_code == 200
    assert r.json()["rating"] == 1500


@pytest.mark.django_db
def test_clan_delete(api, clan):
    r = api.delete(f"/api/clans/{clan.id}/")
    assert r.status_code == 204


# ---------- MAPS CRUD (4) ----------

@pytest.mark.django_db
def test_map_create(api):
    r = api.post("/api/maps/", {"name": "Прохоровка", "mode": "Встречный бой"}, format="json")
    assert r.status_code == 201


@pytest.mark.django_db
def test_map_list(api, game_map):
    r = api.get("/api/maps/")
    assert r.status_code == 200


@pytest.mark.django_db
def test_map_update(api, game_map):
    r = api.patch(f"/api/maps/{game_map.id}/", {"max_players": 24}, format="json")
    assert r.status_code == 200


@pytest.mark.django_db
def test_map_delete(api, game_map):
    r = api.delete(f"/api/maps/{game_map.id}/")
    assert r.status_code == 204


# ---------- BATTLES CRUD (4) ----------

@pytest.mark.django_db
def test_battle_create(api, game_map, player):
    r = api.post("/api/battles/", {"map": game_map.id, "players": [player.id], "status": "planned"}, format="json")
    assert r.status_code == 201


@pytest.mark.django_db
def test_battle_list(api, game_map, player):
    Battle.objects.create(map=game_map)
    r = api.get("/api/battles/")
    assert r.status_code == 200


@pytest.mark.django_db
def test_battle_update_status(api, game_map):
    b = Battle.objects.create(map=game_map)
    r = api.patch(f"/api/battles/{b.id}/", {"status": "finished", "result": "victory"}, format="json")
    assert r.status_code == 200
    assert r.json()["result"] == "victory"


@pytest.mark.django_db
def test_battle_delete(api, game_map):
    b = Battle.objects.create(map=game_map)
    r = api.delete(f"/api/battles/{b.id}/")
    assert r.status_code == 204


# ---------- ACHIEVEMENTS CRUD (4) ----------

@pytest.mark.django_db
def test_achievement_create(api):
    r = api.post("/api/achievements/", {"code": "first_blood", "title": "Первая кровь"}, format="json")
    assert r.status_code == 201


@pytest.mark.django_db
def test_achievement_list(api):
    Achievement.objects.create(code="veteran", title="Ветеран")
    r = api.get("/api/achievements/")
    assert r.status_code == 200


@pytest.mark.django_db
def test_achievement_assign_to_player(api, player):
    a = Achievement.objects.create(code="sniper", title="Снайпер")
    r = api.patch(f"/api/achievements/{a.id}/", {"players": [player.id]}, format="json")
    assert r.status_code == 200
    assert player in a.players.all()


@pytest.mark.django_db
def test_achievement_delete(api):
    a = Achievement.objects.create(code="temp", title="Временная")
    r = api.delete(f"/api/achievements/{a.id}/")
    assert r.status_code == 204


# ---------- Negative / search ----------

@pytest.mark.django_db
def test_tank_search(api, tank):
    r = api.get("/api/tanks/?search=T-34")
    assert r.status_code == 200
    assert len(r.json()) == 1


@pytest.mark.django_db
def test_404_on_missing_tank(api):
    r = api.get("/api/tanks/999999/")
    assert r.status_code == 404
