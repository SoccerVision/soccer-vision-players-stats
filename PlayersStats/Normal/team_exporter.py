# team_exporter.py

import json
from .team_generator import generate_team

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
            'Averages': player.averages  # Include the averages
        }
        team_data.append(player_info)

    # Export to JSON file
    with open(filename, 'w') as json_file:
        json.dump(team_data, json_file, indent=4)

if __name__ == "__main__":
    team = generate_team()
    export_team_to_json(team, filename='team.json')
    print(f"Team exported to {filename}")