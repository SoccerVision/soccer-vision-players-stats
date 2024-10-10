# PlayersStats/Normal/generate_team.py

import json
import random
from .defender import Defender
from .midfielder import Midfielder
from .striker import Striker
from .fullback import FullBack
from .winger import Winger
from .goalkeeper import Goalkeeper

def generate_team():
    team = []

    # Generate Goalkeepers
    goalkeepers = [Goalkeeper() for _ in range(2)]
    team.extend(goalkeepers)

    # Randomly choose 3 or 4 Defenders
    num_defenders = random.choice([3, 4])
    defenders = [Defender() for _ in range(num_defenders)]
    team.extend(defenders)

    # Generate 4 FullBacks
    fullbacks = [FullBack() for _ in range(4)]
    team.extend(fullbacks)

    # Generate 6 Midfielders
    midfielders = [Midfielder() for _ in range(6)]
    team.extend(midfielders)

    # Randomly choose 2 or 3 Strikers
    num_strikers = random.choice([2, 3])
    strikers = [Striker() for _ in range(num_strikers)]
    team.extend(strikers)

    # Generate 2 Wingers
    wingers = [Winger() for _ in range(2)]
    team.extend(wingers)

    # Ensure total number of players is 20
    total_players = len(team)
    if total_players != 20:
        # Adjust the number of midfielders to make total 20
        midfielders_needed = 20 - total_players
        if midfielders_needed > 0:
            additional_midfielders = [Midfielder() for _ in range(midfielders_needed)]
            team.extend(additional_midfielders)
        elif midfielders_needed < 0:
            # Remove excess midfielders
            team = [player for player in team if player.position != 'Midfielder'] + midfielders[:midfielders_needed]

    return team

def export_team_to_json(team, filename='team.json'):
    # Convert team data to serializable format
    team_data = []
    for player in team:
        player_info = {
            'Position': player.position,
            'Age': player.age,
            'Height': player.height,
            'Preferred Foot': player.preferred_foot,
            'Stamina': player.stamina,
            'Fitness': player.fitness,
            'Nationality': player.nationality,
            'Stats': player.stats,
        }
        team_data.append(player_info)

    # Export to JSON file
    with open(filename, 'w') as json_file:
        json.dump(team_data, json_file, indent=4)

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
        print("Stats:")
        for category, stats in player.stats.items():
            print(f"  [{category}]")
            for stat_name, value in stats.items():
                print(f"    {stat_name}: {value}")
        print("-" * 80)
    print("=" * 80)

def main():
    team = generate_team()
    export_team_to_json(team)
    print_team(team)

if __name__ == "__main__":
    main()