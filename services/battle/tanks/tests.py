import pytest
from rest_framework.test import APIClient

from .models import Battle


@pytest.fixture
def api():
    return APIClient()


@pytest.fixture
def battle():
    return Battle.objects.create(map_id=3, player_ids=[10, 11])


@pytest.mark.django_db
def test_health(api):
    response = api.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "battle"}


@pytest.mark.django_db
def test_battle_create(api):
    response = api.post(
        "/api/battles/",
        {"map_id": 2, "player_ids": [4, 5], "status": "planned"},
        format="json",
    )
    assert response.status_code == 201
    assert response.json()["player_ids"] == [4, 5]


@pytest.mark.django_db
def test_battle_list(api, battle):
    response = api.get("/api/battles/")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_battle_update(api, battle):
    response = api.patch(
        f"/api/battles/{battle.id}/",
        {"status": "finished", "result": "victory"},
        format="json",
    )
    assert response.status_code == 200
    assert response.json()["result"] == "victory"


@pytest.mark.django_db
def test_battle_search(api, battle):
    response = api.get("/api/battles/?search=planned")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_battle_delete(api, battle):
    response = api.delete(f"/api/battles/{battle.id}/")
    assert response.status_code == 204
    assert Battle.objects.count() == 0
