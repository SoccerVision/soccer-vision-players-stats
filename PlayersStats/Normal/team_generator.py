# team_generator.py

import random
from PlayersStats.Normal.defender import Defender
from PlayersStats.Normal.midfielder import Midfielder
from PlayersStats.Normal.striker import Striker
from PlayersStats.Normal.fullback import FullBack
from PlayersStats.Normal.winger import Winger
from PlayersStats.Normal.goalkeeper import Goalkeeper
from .team_exporter import export_team_to_json
from .team_printer import print_team

def generate_team():
    team = []

    # Generate Goalkeepers
    goalkeepers = [Goalkeeper() for _ in range(2)]
    team.extend(goalkeepers)

    # Randomly choose 3 or 4 Defenders
    num_defenders = random.choice([3, 4])
    defenders = [Defender() for _ in range(num_defenders)]
    team.extend(defenders)

    # Generate FullBacks
    fullbacks = []

    # Ensure at least one left-footed and one right-footed fullback
    fullbacks.append(FullBack(dominant_foot='Right'))
    fullbacks.append(FullBack(dominant_foot='Left'))

    # Generate remaining fullbacks (4 total)
    num_remaining_fullbacks = 4 - 2
    for _ in range(num_remaining_fullbacks):
        fullbacks.append(FullBack())

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

if __name__ == "__main__":
    team = generate_team()
    export_team_to_json(team, filename='team.json')
    print_team(team)