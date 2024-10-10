# team_printer.py

from .team_generator import generate_team

def print_team(team):
    print("\nTeam Roster:")
    print("=" * 80)
    for idx, player in enumerate(team, start=1):
        print(f"Player {idx}: {player.position}")
        print(f"Age: {player.age}")
        print(f"Height: {player.height} cm")
        print(f"Preferred Foot: {player.preferred_foot['Dominant Foot']}")
        print(f"Weak Foot Level: {player.preferred_foot['Weak Foot Level']}")
        print(f"Stamina: {player.stamina}")
        print(f"Fitness: {player.fitness}")
        print(f"Nationality: {player.nationality}")
        print("Averages:")
        for category, avg in player.averages.items():
            print(f"  {category}: {avg}")
        print("Stats:")
        for category, stats in player.stats.items():
            print(f"  [{category}]")
            for stat_name, value in stats.items():
                print(f"    {stat_name}: {value}")
        print("-" * 80)
    print("=" * 80)

if __name__ == "__main__":
    team = generate_team()
    print_team(team)