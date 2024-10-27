import random
from app.core.positions.goalkeeper import Goalkeeper
from app.core.positions.defender import Defender
from app.core.positions.fullback import Fullback
from app.core.positions.striker import Striker
from app.core.positions.winger import Winger
from app.core.positions.midfielder import Midfielder

POSITIONS = [Goalkeeper, Defender, Fullback, Striker, Winger, Midfielder]

def generate_young_team():
    team = []
    assigned_numbers = set()

    def generate_player(position_class, count):
        for _ in range(count):
            player = position_class(level=get_player_level().lower(), assigned_numbers=assigned_numbers)
            # Directly set player age to be within the young age range (16-19 years old)
            player.age = random.randint(16, 19)
            # Adjust stats for young player based on their level and age
            adjust_young_player_stats(player)
            # Recalculate average stats for the player
            update_player_average_stats(player)
            team.append(player)

    # Generate young players for each position
    generate_player(Goalkeeper, 2)
    generate_player(Defender, 3)
    generate_player(Fullback, 3)
    generate_player(Striker, 3)
    generate_player(Winger, 2)
    generate_player(Midfielder, 4)

    return team

def adjust_young_player_stats(player):
    # Set base stats based on the player's level
    if player.level == 'weaker':
        base_stat_min, base_stat_max = 30, 40
    elif player.level == 'normal':
        base_stat_min, base_stat_max = 40, 50
    else:  # excellent level
        base_stat_min, base_stat_max = 50, 70

    # Set player's stats within the given range and adjust by age
    for stat_category in player.stats:
        for stat_name in player.stats[stat_category]:
            player.stats[stat_category][stat_name] = random.randint(base_stat_min, base_stat_max)
            # Ensure the highest stats (70) are for 19-year-olds and are rare
            if player.stats[stat_category][stat_name] == 70:
                player.age = 19  # Set age to 19 for highest stat
                if random.random() > 0.1:  # 10% chance to keep the stat at 70
                    player.stats[stat_category][stat_name] = random.randint(base_stat_min, base_stat_max - 1)

def update_player_average_stats(player):
    # Recalculate the average stats for each category
    player.averages = {}
    for stat_category in player.stats:
        total_stats = 0
        stat_count = 0
        for stat_name in player.stats[stat_category]:
            total_stats += player.stats[stat_category][stat_name]
            stat_count += 1
        player.averages[stat_category] = round(total_stats / stat_count) if stat_count > 0 else 0

def get_player_level():
    random_number = random.randint(1, 50)
    if random_number == 1:
        return 'excellent'
    elif 2 <= random_number <= 6:
        return 'weaker'
    else:
        return 'normal'
