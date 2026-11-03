import statistics

import pytest

from app.core import realism
from app.core.excellent_team_generator import generate_excellent_team
from app.core.generator import (AGE_PROFILES, FORMATIONS, TEMPLATES, GenerationOptions, generate_players,
                                generate_squad, squad_summary)
from app.core.levels.player_config import player_config
from app.core.normal_team_generator import generate_normal_team
from app.core.team_generator import generate_team
from app.core.weak_team_generator import generate_weak_team
from app.core.younger_team_generator import generate_young_team


def assert_valid_squad(players):
    numbers = [p.shirt_number for p in players]
    assert len(numbers) == len(set(numbers)), "duplicate shirt numbers"
    assert all(1 <= n <= 99 for n in numbers)
    for p in players:
        for values in p.stats.values():
            assert all(1 <= v <= 99 for v in values.values())
        assert 1 <= p.overall <= 99


@pytest.mark.parametrize("generator,size", [
    (generate_team, 22), (generate_weak_team, 22), (generate_normal_team, 18),
    (generate_excellent_team, 22), (generate_young_team, 17),
])
def test_v1_generators_never_hang_and_stay_valid(generator, size):
    # The excellent team used to hang on ~35% of calls (shirt numbers ran out)
    for _ in range(200):
        team = generator()
        assert len(team) == size
        assert_valid_squad(team)


def test_v1_excellent_rule_and_young_ages():
    team = generate_excellent_team()
    core, extras = team[:18], team[18:]
    assert all(p.age >= 28 for p in core)
    assert [18 <= p.age <= 21 for p in extras[:2]] == [True, True]
    assert all(16 <= p.age <= 19 for p in generate_young_team())


@pytest.mark.parametrize("template", sorted(TEMPLATES))
@pytest.mark.parametrize("level", [*realism.LEVELS, "mixed"])
def test_every_template_and_level(template, level):
    for seed in range(20):
        squad = generate_squad(GenerationOptions(template=template, level=level, seed=seed))
        assert_valid_squad(squad.players)


@pytest.mark.parametrize("formation", sorted(FORMATIONS))
def test_formations_build_xi_plus_bench(formation):
    players = generate_squad(GenerationOptions(formation=formation, seed=1)).players
    starters = [p for p in players if p.squad_role == "starter"]
    assert len(players) == 23 and len(starters) == 11
    assert sum(p.position == "goalkeeper" for p in starters) == 1
    assert sum(p.position == "goalkeeper" for p in players) == 3
    assert next(p for p in starters if p.position == "goalkeeper").shirt_number == 1


@pytest.mark.parametrize("profile", sorted(AGE_PROFILES))
def test_age_profiles_respected(profile):
    low, high, _ = AGE_PROFILES[profile]
    players = generate_squad(GenerationOptions(age_profile=profile, seed=5)).players
    assert all(low <= p.age <= high for p in players)


def test_same_seed_same_squad_and_different_seed_differs():
    a = generate_squad(GenerationOptions(level="mixed", formation="4-2-3-1", seed=123))
    b = generate_squad(GenerationOptions(level="mixed", formation="4-2-3-1", seed=123))
    c = generate_squad(GenerationOptions(level="mixed", formation="4-2-3-1", seed=124))
    assert [p.to_dict() for p in a.players] == [p.to_dict() for p in b.players]
    assert [p.to_dict() for p in a.players] != [p.to_dict() for p in c.players]


def test_mental_stats_vary_between_players():
    # These were drawn once per process before the fix
    players = generate_players(GenerationOptions(seed=9), 60, position="midfielder").players
    assert statistics.pstdev(p.stats["mental"]["aggression"] for p in players) > 10


@pytest.mark.parametrize("position,category,stat", [
    ("striker", "attack", "finishing"),
    ("defender", "defense", "tackling"),
    ("winger", "playmaking", "crossing"),
    ("goalkeeper", "goalkeeping", "reflexes"),
])
@pytest.mark.parametrize("level", realism.LEVELS)
def test_position_identity_is_kept(position, category, stat, level):
    # Post-processing must not flatten position configs (it did before for physical_power/jumping)
    players = generate_players(GenerationOptions(level=level, age_profile="prime", seed=11), 60,
                               position=position).players
    players += generate_players(GenerationOptions(level=level, age_profile="prime", seed=12), 60,
                                position=position).players
    expected = player_config["positions"][level][position][category][stat]["mean"]
    actual = statistics.mean(p.stats[category][stat] for p in players)
    assert abs(actual - expected) <= 4, f"{position} {stat}: config {expected}, got {actual:.1f}"


def test_excellent_fullback_beats_normal():
    def avg_speed(level):
        players = generate_players(GenerationOptions(level=level, age_profile="prime", seed=3), 60,
                                   position="fullback").players
        return statistics.mean(p.stats["athletic"]["speed"] for p in players)
    assert avg_speed("excellent") > avg_speed("normal") + 8


def test_age_curve_pace_declines_intelligence_grows():
    prime = generate_players(GenerationOptions(seed=4), 60, position="midfielder", age=26).players
    veteran = generate_players(GenerationOptions(seed=4), 60, position="midfielder", age=34).players

    def avg(players, category, stat):
        return statistics.mean(p.stats[category][stat] for p in players)
    assert avg(veteran, "athletic", "speed") < avg(prime, "athletic", "speed") - 4
    assert avg(veteran, "mental", "composure") >= avg(prime, "mental", "composure")


def test_goalkeepers_have_goalkeeping_not_outfield_categories():
    gk = generate_players(GenerationOptions(seed=2), 1, position="goalkeeper").players[0]
    assert "goalkeeping" in gk.stats
    assert not {"attack", "defense", "playmaking"} & set(gk.stats)


def test_left_footed_share_is_realistic():
    players = [p for seed in range(100) for p in generate_squad(GenerationOptions(seed=seed)).players]
    share = squad_summary(players)["left_footed"] / len(players)
    assert 0.18 <= share <= 0.32


def test_left_back_is_usually_left_footed():
    players = generate_players(GenerationOptions(seed=8), 60, position="fullback", side="L").players
    assert sum(p.preferred_foot["dominant_foot"] == "Left" for p in players) / len(players) > 0.65


def test_potential_only_for_young_players():
    young = generate_players(GenerationOptions(seed=6), 20, age=19).players
    old = generate_players(GenerationOptions(seed=6), 20, age=30).players
    assert all(p.potential is not None and p.potential >= p.overall for p in young)
    assert all(p.potential is None for p in old)


@pytest.mark.parametrize("options,match", [
    (dict(template="nope"), "Unknown template"),
    (dict(formation="2-2-6"), "Unknown formation"),
    (dict(positions={"libero": 2}), "Unknown positions"),
    (dict(positions={"striker": 61}), "too large"),
    (dict(level="legendary"), "Unknown level"),
    (dict(min_age=30, max_age=20), "Invalid age range"),
    (dict(level="mixed", level_weights={"normal": 0}), "level_weights"),
])
def test_invalid_options_raise_value_error(options, match):
    with pytest.raises(ValueError, match=match):
        generate_squad(GenerationOptions(**options))
