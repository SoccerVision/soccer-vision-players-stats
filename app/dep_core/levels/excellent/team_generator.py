# app/core/levels/excellent/team_generator.py

import random
from app.dep_core.levels.excellent.positions.defender import Defender
from app.dep_core.levels.excellent.positions.midfielder import Midfielder
from app.dep_core.levels.excellent.positions.striker import Striker
from app.dep_core.levels.excellent.positions.fullback import FullBack
from app.dep_core.levels.excellent.positions.winger import Winger
from app.dep_core.levels.excellent.positions.goalkeeper import Goalkeeper

def generate_excellent_team():
    team = []
    assigned_numbers = set()  # Set to keep track of assigned shirt numbers

    # Generate Goalkeepers
    goalkeepers = [Goalkeeper(assigned_numbers=assigned_numbers) for _ in range(2)]
    team.extend(goalkeepers)

    # Randomly choose 3 or 4 Defenders
    num_defenders = random.choice([3, 4])
    defenders = [Defender(assigned_numbers=assigned_numbers) for _ in range(num_defenders)]
    team.extend(defenders)

    # Generate FullBacks
    fullbacks = []

    # Ensure at least one left-footed and one right-footed fullback
    fullbacks.append(FullBack(dominant_foot='Right', assigned_numbers=assigned_numbers))
    fullbacks.append(FullBack(dominant_foot='Left', assigned_numbers=assigned_numbers))

    # Generate remaining fullbacks (4 total)
    num_remaining_fullbacks = 4 - 2
    for _ in range(num_remaining_fullbacks):
        fullbacks.append(FullBack(assigned_numbers=assigned_numbers))

    team.extend(fullbacks)

    # Generate 6 Midfielders
    midfielders = [Midfielder(assigned_numbers=assigned_numbers) for _ in range(6)]
    team.extend(midfielders)

    # Randomly choose 2 or 3 Strikers
    num_strikers = random.choice([2, 3])
    strikers = [Striker(assigned_numbers=assigned_numbers) for _ in range(num_strikers)]
    team.extend(strikers)

    # Generate 2 Wingers
    wingers = [Winger(assigned_numbers=assigned_numbers) for _ in range(2)]
    team.extend(wingers)

    # Ensure total number of players is 20
    total_players = len(team)
    if total_players != 20:
        # Adjust the number of midfielders to make total 20
        midfielders_needed = 20 - total_players
        if midfielders_needed > 0:
            additional_midfielders = [Midfielder(assigned_numbers=assigned_numbers) for _ in range(midfielders_needed)]
            team.extend(additional_midfielders)
        elif midfielders_needed < 0:
            # Remove excess midfielders
            team = [player for player in team if player.position != 'Midfielder'] + midfielders[:midfielders_needed]

    return team

if __name__ == "__main__":
    team = generate_excellent_team()
