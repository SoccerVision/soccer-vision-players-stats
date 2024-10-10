# display_stats.py

from PlayersStats.depracted.defender import get_defender_stats
from PlayersStats.depracted.striker import get_striker_stats
from PlayersStats.depracted.midfielder import get_midfielder_stats

def print_stats_table(position, stats):
    print(f"\n{position} Stats:")
    for category, stat_dict in stats.items():
        print(f"\nCategory: {category}")
        print("-" * 30)
        # Determine column widths
        max_stat_name_length = max(len(stat_name) for stat_name in stat_dict.keys())
        max_value_length = max(len(str(value)) for value in stat_dict.values())
        total_width = max_stat_name_length + max_value_length + 7  # For spacing and borders

        # Print header
        print(f"{'Stat'.ljust(max_stat_name_length)} | {'Value'.rjust(max_value_length)}")
        print("-" * total_width)

        # Print each stat
        for stat_name, value in stat_dict.items():
            print(f"{stat_name.ljust(max_stat_name_length)} | {str(value).rjust(max_value_length)}")

def main():
    # Get stats for each position
    defender_stats, defender_averages = get_defender_stats()
    striker_stats, striker_averages = get_striker_stats()
    midfielder_stats, midfielder_averages = get_midfielder_stats()

    # Print stats in table format
    print_stats_table('Defender', defender_stats)
    print_stats_table('Striker', striker_stats)
    print_stats_table('Midfielder', midfielder_stats)

if __name__ == "__main__":
    main()