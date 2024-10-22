import random

weaker_adjustments = {
    'Mental': {
        'Aggression': {'mean': random.randint(10, 90), 'std_dev': 5},
        'Teamwork': {'mean': random.randint(10, 90), 'std_dev': 5},
        'Decisions': {'mean': random.randint(10, 90), 'std_dev': 5},
        'Composure': {'mean': 35, 'std_dev': 6},
    },
    'Defense': {
        'Tackling': {'mean': 35, 'std_dev': 4},
        'Marking': {'mean': 35, 'std_dev': 4},
        'Positioning': {'mean': 35, 'std_dev': 4},
    },
    'Attack': {
        'Finishing': {'mean': 35, 'std_dev': 4},
        'Long Shots': {'mean': 35, 'std_dev': 4},
        'Off The Ball': {'mean': 35, 'std_dev': 4},
    },
    'Playmaking': {
        'Creative': {'mean': 35, 'std_dev': 4},
        'Passing': {'mean': 35, 'std_dev': 4},
        'Crossing': {'mean': 35, 'std_dev': 4},
    },
    'Athletic': {
        'Physical Power': {'mean': 40, 'std_dev': 8},
        'Ball Control': {'mean': 45, 'std_dev': 4},
        'Dribbling': {'mean': 45, 'std_dev': 4},
        'Jumping': {'mean': 40, 'std_dev': 8},
        'Acceleration': {'mean': 45, 'std_dev': 8},
        'Speed': {'mean': 45, 'std_dev': 8},
    },
    'Set Pieces': {
        'Free Kicks': {'mean': 15, 'std_dev': 15, 'min': 30, 'max': 90},
        'Penalty': {'mean': 45, 'std_dev': 15, 'min': 30, 'max': 90},
    },
}