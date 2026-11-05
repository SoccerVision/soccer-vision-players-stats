"""The player model against the real figures in app/core/realism.py (sources there)."""
import random
import statistics

from app.core import realism
from app.core.generator import GenerationOptions, generate_squad
from app.core.player import Player


def _players(level, position, n=600, age=26, seed=1):
    rng = random.Random(seed)
    return [Player(position, level, rng=rng, age=age) for _ in range(n)]


def test_decisions_are_intelligence_loosely_tied_to_the_level():
    # a little better at a higher level, but good players with poor decisions and ordinary ones with fine decisions are common
    weak = [p.stats["mental"]["decisions"] for p in _players("weaker", "midfielder")]
    excellent = [p.stats["mental"]["decisions"] for p in _players("excellent", "midfielder")]
    assert 12 < statistics.mean(excellent) - statistics.mean(weak) < 30
    assert sum(v < 55 for v in excellent) / len(excellent) > 0.08   # excellent players who decide worse than an ordinary one
    assert sum(v > 70 for v in weak) / len(weak) > 0.08             # weak players who decide better than an excellent one on average


def test_excellent_players_are_not_piled_up_at_99_but_some_reach_90():
    for position, category, stat in (("defender", "defense", "tackling"), ("striker", "attack", "finishing"),
                                      ("goalkeeper", "goalkeeping", "reflexes")):
        values = [p.stats[category][stat] for p in _players("excellent", position)]
        assert sum(v == 99 for v in values) / len(values) < 0.02, f"{position} {stat} piled up at 99"
        assert 0.03 < sum(v >= 90 for v in values) / len(values) < 0.35, f"{position} {stat}: 90+ should be rare but there"


def test_a_tall_winger_or_a_good_heading_winger_is_rare_but_possible():
    wingers = _players("normal", "winger", n=3000)
    assert 0 < sum(p.height >= 188 for p in wingers) / len(wingers) < 0.05
    assert 0 < sum(p.stats["athletic"]["heading"] >= 65 for p in wingers) / len(wingers) < 0.10


def test_heading_is_a_skill_not_a_jump():
    players = _players("normal", "defender", n=1500)
    jump = [p.stats["athletic"]["jumping"] for p in players]
    head = [p.stats["athletic"]["heading"] for p in players]
    assert abs(statistics.correlation(jump, head)) < 0.2
    strikers = statistics.mean(p.stats["athletic"]["heading"] for p in _players("normal", "striker"))
    wingers = statistics.mean(p.stats["athletic"]["heading"] for p in _players("normal", "winger"))
    assert strikers > wingers + 10


def test_height_makes_stronger_and_slower_but_not_a_better_jumper():
    rng = random.Random(3)
    players = [Player("defender", "normal", rng=rng, age=26) for _ in range(3000)]
    tall = [p for p in players if p.height >= 192]
    short = [p for p in players if p.height <= 182]

    def avg(group, stat):
        return statistics.mean(p.stats["athletic"][stat] for p in group)
    assert avg(tall, "physical_power") > avg(short, "physical_power") + 8
    assert avg(tall, "acceleration") < avg(short, "acceleration") - 5
    assert abs(avg(tall, "jumping") - avg(short, "jumping")) < 3


def test_better_players_are_more_two_footed():
    def good_weak_foot(level):
        players = _players(level, "midfielder", n=2000)
        return sum(p.weak_foot_stars >= 4 for p in players) / len(players)
    assert good_weak_foot("excellent") > good_weak_foot("normal") + 0.12
    assert good_weak_foot("normal") > good_weak_foot("weaker")


def test_squad_ages_follow_real_first_teams():
    ages = [p.age for seed in range(150) for p in generate_squad(GenerationOptions(seed=seed)).players]
    young = sum(a <= 21 for a in ages) / len(ages)
    old = sum(a >= 34 for a in ages) / len(ages)
    assert 0.14 < young < 0.22 and 0.04 < old < 0.09 and 25 < statistics.mean(ages) < 27


def test_footedness_by_slot():
    players = [p for seed in range(60) for p in
               generate_squad(GenerationOptions(seed=seed, template="formation", formation="4-3-3")).players]

    def left_share(test):
        group = [p for p in players if test(p)]
        return sum(p.preferred_foot["dominant_foot"] == "Left" for p in group) / len(group)
    assert left_share(lambda p: p.position == "fullback" and p.side == "L") > 0.75
    assert 0.35 < left_share(lambda p: p.position == "defender" and p.side == "L") < 0.65
    assert left_share(lambda p: p.position == "winger" and p.side == "L") < 0.32   # most left wingers are right-footed (inverted)
    assert left_share(lambda p: p.position == "goalkeeper") < 0.22


def test_young_players_have_less_stamina():
    young = [p.stamina for p in _players("normal", "midfielder", n=800, age=17)]
    prime = [p.stamina for p in _players("normal", "midfielder", n=800, age=27)]
    assert statistics.mean(young) < 0.85 * statistics.mean(prime)


def test_aggression_is_character_random_for_every_position():
    # a striker can be as aggressive as a centre-back: it is the player's character, 10-90 at random
    for position in ("defender", "winger", "striker"):
        values = [p.stats["mental"]["aggression"] for p in _players("normal", position)]
        assert statistics.pstdev(values) > 18 and max(values) >= 85 and min(values) <= 15


def test_weak_foot_gives_no_bonus_to_other_skills():
    # (the match engine handles the weaker foot itself; a bonus here would count it twice)
    players = _players("normal", "striker", n=1500, seed=5)
    one = [p.stats["attack"]["finishing"] for p in players if p.weak_foot_stars <= 2]
    five = [p.stats["attack"]["finishing"] for p in players if p.weak_foot_stars >= 4]
    assert abs(statistics.mean(one) - statistics.mean(five)) < 3
