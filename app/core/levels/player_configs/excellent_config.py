import random

excellent_adjustments = {
    'mental': {
        'aggression': {'mean': random.randint(10, 90), 'std_dev': 5},
        'teamwork': {'mean': random.randint(10, 90), 'std_dev': 5},
        'decisions': {'mean': random.randint(10, 90), 'std_dev': 5},
        'composure': {'mean': 70, 'std_dev': 6},
    },
    'defense': {
        'tackling': {'mean': 70, 'std_dev': 4},
        'marking': {'mean': 70, 'std_dev': 4},
        'positioning': {'mean': 70, 'std_dev': 4},
    },
    'attack': {
        'finishing': {'mean': 70, 'std_dev': 4},
        'long_shots': {'mean': 70, 'std_dev': 4},
        'off_the_ball': {'mean': 70, 'std_dev': 4},
    },
    'playmaking': {
        'creative': {'mean': 70, 'std_dev': 4},
        'passing': {'mean': 70, 'std_dev': 4},
        'crossing': {'mean': 70, 'std_dev': 4},
    },
    'athletic': {
        'physical_power': {'mean': 75, 'std_dev': 8},
        'ball_control': {'mean': 85, 'std_dev': 4},
        'dribbling': {'mean': 85, 'std_dev': 4},
        'jumping': {'mean': 75, 'std_dev': 8},
        'acceleration': {'mean': 80, 'std_dev': 8},
        'speed': {'mean': 80, 'std_dev': 8},
    },
    'set_pieces': {
        'free_kicks': {'mean': 70, 'std_dev': 15, 'min': 30, 'max': 90},
        'penalty': {'mean': 80, 'std_dev': 15, 'min': 30, 'max': 90},
    },
}
