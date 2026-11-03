import pytest
from fastapi.testclient import TestClient

from app.core.generator import AGE_PROFILES, FORMATIONS, TEMPLATES
from app.main import app

client = TestClient(app)

V1_KEYS = {"id", "name", "shirt_number", "position", "level", "age", "height", "preferred_foot",
           "stamina", "fitness", "nationality", "stats", "averages"}


@pytest.mark.parametrize("path,size", [
    ("/api/team", 22), ("/api/team/weaker", 22), ("/api/team/normal", 18),
    ("/api/team/excellent", 22), ("/api/team/younger", 17),
])
def test_v1_routes_keep_their_shape(path, size):
    response = client.get(path)
    assert response.status_code == 200
    players = response.json()
    assert len(players) == size
    assert V1_KEYS <= set(players[0])
    assert {"dominant_foot", "weak_foot_level"} <= set(players[0]["preferred_foot"])


def test_v1_player_by_index():
    assert client.get("/api/team/player/0").status_code == 200
    assert client.get("/api/team/player/99").status_code == 404


def test_options_lists_everything():
    body = client.get("/api/v2/options").json()
    assert set(body["templates"]) == set(TEMPLATES)
    assert set(body["formations"]) == set(FORMATIONS)
    assert set(body["age_profiles"]) == set(AGE_PROFILES)
    assert "target_man" in body["positions"]["striker"]["roles"]


@pytest.mark.parametrize("params", [
    *({"template": t} for t in TEMPLATES),
    *({"formation": f} for f in FORMATIONS),
    *({"age_profile": a} for a in AGE_PROFILES),
    *({"level": lvl} for lvl in ["weaker", "normal", "excellent", "mixed"]),
    {"min_age": 20, "max_age": 22, "nationality": ["Spain", "Japan"]},
])
def test_v2_get_team_accepts_every_option(params):
    response = client.get("/api/v2/team", params=params)
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["summary"]["count"] == len(body["players"]) > 0


def test_v2_team_is_reproducible_with_seed():
    params = {"formation": "3-5-2", "level": "mixed", "seed": 2024}
    assert client.get("/api/v2/team", params=params).json() == client.get("/api/v2/team", params=params).json()


def test_v2_post_team_custom_counts_and_weights():
    body = client.post("/api/v2/team", json={
        "level": "mixed", "level_weights": {"excellent": 1, "normal": 0, "weaker": 0},
        "positions": {"goalkeeper": 2, "striker": 5}, "seed": 1,
    }).json()
    assert body["summary"]["by_position"] == {"goalkeeper": 2, "striker": 5}
    assert all(p["level"] == "Excellent" for p in body["players"])


def test_v2_seeded_player_matches_team():
    team = client.get("/api/v2/team", params={"formation": "4-3-3", "seed": 7}).json()
    player = client.get("/api/v2/team/7/player/9", params={"formation": "4-3-3"}).json()
    assert player == team["players"][9]
    assert client.get("/api/v2/team/7/player/99", params={"formation": "4-3-3"}).status_code == 404


def test_v2_player_filters_are_applied():
    p = client.get("/api/v2/player", params={
        "position": "winger", "side": "R", "role": "inside_forward", "dominant_foot": "Left",
        "age": 20, "level": "excellent", "seed": 5}).json()
    assert (p["position"], p["side"], p["role"], p["preferred_foot"]["dominant_foot"], p["age"], p["level"]) == \
        ("winger", "R", "inside_forward", "Left", 20, "Excellent")


def test_v2_players_batch():
    body = client.post("/api/v2/players", json={"count": 7, "position": "goalkeeper"}).json()
    assert len(body["players"]) == 7 and all(p["position"] == "goalkeeper" for p in body["players"])


@pytest.mark.parametrize("method,path,kwargs", [
    ("get", "/api/v2/player", {"params": {"position": "goalkeeper", "role": "poacher"}}),
    ("get", "/api/v2/player", {"params": {"position": "striker", "side": "L"}}),
    ("get", "/api/v2/team", {"params": {"min_age": 30, "max_age": 20}}),
    ("get", "/api/v2/team", {"params": {"formation": "9-9-9"}}),
    ("post", "/api/v2/team", {"json": {"positions": {"striker": 100}}}),
    ("post", "/api/v2/players", {"json": {"count": 0}}),
])
def test_v2_invalid_input_is_422(method, path, kwargs):
    assert getattr(client, method)(path, **kwargs).status_code == 422


def test_docs_and_openapi_are_served():
    assert client.get("/docs").status_code == 200
    schema = client.get("/openapi.json").json()
    assert schema["info"]["version"] == "2.0.0"
    assert "/api/v2/team" in schema["paths"]
