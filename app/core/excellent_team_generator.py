import random
from app.core.positions.goalkeeper import Goalkeeper
from app.core.positions.defender import Defender
from app.core.positions.fullback import Fullback
from app.core.positions.striker import Striker
from app.core.positions.winger import Winger
from app.core.positions.midfielder import Midfielder

POSITIONS = [Goalkeeper, Defender, Fullback, Striker, Winger, Midfielder]


def generate_excellent_team():
    team = []
    assigned_numbers = set()

    def generate_player(position_class, count, ensure_foot=None, age_range=None):
        for _ in range(count):
            extra = {'dominant_foot': ensure_foot} if ensure_foot else {}
            while True:
                player = position_class(level='excellent', assigned_numbers=assigned_numbers, **extra)
                if age_range == 'young':
                    if 18 <= player.age <= 21:
                        break
                elif age_range == 'old':
                    if player.age >= 29:
                        break
                elif player.level == 'excellent' and player.age <= 27:
                    continue  # Ensure excellent players are above age 27
                else:
                    break
            # Reserve the shirt number only once the player is accepted
            assigned_numbers.add(player.shirt_number)
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

    # Randomly select positions for young and old players
    for _ in range(2):
        position_class = random.choice(POSITIONS)
        generate_player(position_class, 1, age_range='young')

    for _ in range(2):
        position_class = random.choice(POSITIONS)
        generate_player(position_class, 1, age_range='old')

    return team
