import pytest
from rest_framework.test import APIClient

from .models import GameMap, Tank


@pytest.fixture
def api():
    return APIClient()


@pytest.fixture
def tank():
    return Tank.objects.create(
        name="T-34-85",
        nation="USSR",
        tank_type="MT",
        tier=6,
        hp=960,
        damage=200,
    )


@pytest.fixture
def game_map():
    return GameMap.objects.create(
        name="Prokhorovka",
        mode="Standard battle",
        size_km=1.2,
    )


@pytest.mark.django_db
def test_health(api):
    response = api.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "catalog",
    }


@pytest.mark.django_db
def test_tank_create(api):
    response = api.post(
        "/api/tanks/",
        {
            "name": "IS-7",
            "nation": "USSR",
            "tier": 10,
            "damage": 500,
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.json()["name"] == "IS-7"


@pytest.mark.django_db
def test_tank_list(api, tank):
    response = api.get("/api/tanks/")

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_tank_update(api, tank):
    response = api.patch(
        f"/api/tanks/{tank.id}/",
        {"hp": 1100},
        format="json",
    )

    assert response.status_code == 200
    assert response.json()["hp"] == 1100


@pytest.mark.django_db
def test_tank_delete(api, tank):
    response = api.delete(f"/api/tanks/{tank.id}/")

    assert response.status_code == 204
    assert Tank.objects.count() == 0


@pytest.mark.django_db
def test_tank_search(api, tank):
    response = api.get("/api/tanks/?search=T-34")

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_map_create(api):
    response = api.post(
        "/api/maps/",
        {
            "name": "Himmelsdorf",
            "mode": "Standard battle",
        },
        format="json",
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_map_list(api, game_map):
    response = api.get("/api/maps/")

    assert response.status_code == 200
    assert response.json()[0]["name"] == "Prokhorovka"