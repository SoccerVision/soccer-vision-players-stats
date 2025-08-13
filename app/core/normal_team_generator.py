import random
from app.core.positions.goalkeeper import Goalkeeper
from app.core.positions.defender import Defender
from app.core.positions.fullback import Fullback
from app.core.positions.striker import Striker
from app.core.positions.winger import Winger
from app.core.positions.midfielder import Midfielder

def generate_normal_team():
    team = []
    assigned_numbers = set()

    def generate_player(position_class, count, ensure_foot=None):
        for _ in range(count):
            player = position_class(level='normal', assigned_numbers=assigned_numbers)
            # Ensure at least one left-footed and one right-footed fullback
            if ensure_foot:
                while player.preferred_foot['dominant_foot'] != ensure_foot:
                    player = position_class(level='normal', assigned_numbers=assigned_numbers)
                ensure_foot = None  # Only ensure foot for one player
            team.append(player)

    # Generate players for each position
    generate_player(Goalkeeper, 2)
    generate_player(Defender, 3)
    generate_player(Fullback, 1, ensure_foot='Left')  # Ensure at least one left-footed fullback
    generate_player(Fullback, 1, ensure_foot='Right')  # Ensure at least one right-footed fullback
    generate_player(Fullback, 2)  # Generate the rest of the fullbacks
    generate_player(Striker, 3)
    generate_player(Winger, 2)
    generate_player(Midfielder, 4)

    return team
