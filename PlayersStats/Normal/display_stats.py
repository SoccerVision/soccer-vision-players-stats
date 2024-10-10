# PlayersStats/Normal/display_stats.py

from .defender import Defender
from .midfielder import Midfielder
from .striker import Striker
from .fullback import FullBack
from .winger import Winger
from .goalkeeper import Goalkeeper

def print_position_table(position_name, players):
    # ANSI color codes
    RESET = '\033[0m'
    BOLD = '\033[1m'
    CATEGORY_COLOR = '\033[1;34m'  # Bold Blue
    AVERAGE_COLOR = '\033[1;32m'   # Bold Green

    # Collect all stat names and categories
    all_stats = []
    all_categories = []
    stat_category_map = {}

    for player in players:
        for category, stats in player.stats.items():
            if category not in all_categories:
                all_categories.append(category)
            for stat in stats:
                if stat not in all_stats:
                    all_stats.append(stat)
                stat_category_map[stat] = category

    # Sort stats by category
    all_stats_sorted = sorted(all_stats, key=lambda x: (all_categories.index(stat_category_map[x]), x))

    # Header
    print(f"\nPosition: {position_name}")
    header = ['Stat'] + [f"Player {i+1}" for i in range(len(players))]
    print("-" * (len(header) * 20))
    print("{:<20}".format(header[0]), end='')
    for h in header[1:]:
        print("{:>20}".format(h), end='')
    print()
    print("-" * (len(header) * 20))

    # Print basic info
    info_labels = ['Age', 'Height (cm)', 'Dominant Foot', 'Weak Foot Level', 'Stamina', 'Fitness', 'Nationality']
    for label in info_labels:
        print("{:<20}".format(label), end='')
        values = []
        for player in players:
            # Handle 'Dominant Foot' and 'Weak Foot Level' separately
            if label in ['Dominant Foot', 'Weak Foot Level']:
                value = player.preferred_foot[label]
            else:
                attr_name = label.replace(' (cm)', '').replace(' ', '_').lower()
                value = getattr(player, attr_name)
            values.append(value)
            print("{:>20}".format(str(value)), end='')
        print()
    print("-" * (len(header) * 20))

    # Print stats and calculate per-player category averages
    current_category = ''
    category_stats = {}
    for stat in all_stats_sorted:
        category = stat_category_map[stat]
        if category != current_category:
            if current_category != '':
                # After finishing a category, print the per-player averages
                average_label = f"Average {current_category}"
                print(f"{AVERAGE_COLOR}{average_label:<20}{RESET}", end='')
                for player_index in range(len(players)):
                    player_total = category_stats[player_index]['total']
                    player_count = category_stats[player_index]['count']
                    avg = round(player_total / player_count)
                    print("{:>20}".format(avg), end='')
                print()
            current_category = category
            # Initialize per-player totals and counts for the new category
            category_stats = {i: {'total': 0, 'count': 0} for i in range(len(players))}
            # Print category header with color
            print(f"\n{CATEGORY_COLOR}[{category}]{RESET}")
        print("{:<20}".format(stat), end='')
        for idx, player in enumerate(players):
            value = player.stats.get(category, {}).get(stat, 0)
            print("{:>20}".format(str(value)), end='')
            # Accumulate totals and counts for each player
            category_stats[idx]['total'] += value
            category_stats[idx]['count'] += 1
        print()
    # Print average for the last category
    if current_category != '':
        average_label = f"Average {current_category}"
        print(f"{AVERAGE_COLOR}{average_label:<20}{RESET}", end='')
        for player_index in range(len(players)):
            player_total = category_stats[player_index]['total']
            player_count = category_stats[player_index]['count']
            avg = round(player_total / player_count)
            print("{:>20}".format(avg), end='')
        print()

    print("=" * (len(header) * 20))

def main():
    positions = {
        'Defender': Defender,
        'Midfielder': Midfielder,
        'Striker': Striker,
        'FullBack': FullBack,
        'Winger': Winger,
        'Goalkeeper': Goalkeeper,
    }

    for position_name, position_class in positions.items():
        # Generate three players for each position
        players = [position_class() for _ in range(3)]
        print_position_table(position_name, players)

if __name__ == "__main__":
    main()