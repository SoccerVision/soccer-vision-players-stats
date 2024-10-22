import random

excellent_adjustments = {
    'Mental': {
        'Aggression': {'mean': random.randint(10, 90), 'std_dev': 5},
        'Teamwork': {'mean': random.randint(10, 90), 'std_dev': 5},
        'Decisions': {'mean': random.randint(10, 90), 'std_dev': 5},
        'Composure': {'mean': 70, 'std_dev': 6},
    },
    'Defense': {
        'Tackling': {'mean': 70, 'std_dev': 4},
        'Marking': {'mean': 70, 'std_dev': 4},
        'Positioning': {'mean': 70, 'std_dev': 4},
    },
    'Attack': {
        'Finishing': {'mean': 70, 'std_dev': 4},
        'Long Shots': {'mean': 70, 'std_dev': 4},
        'Off The Ball': {'mean': 70, 'std_dev': 4},
    },
    'Playmaking': {
        'Creative': {'mean': 70, 'std_dev': 4},
        'Passing': {'mean': 70, 'std_dev': 4},
        'Crossing': {'mean': 70, 'std_dev': 4},
    },
    'Athletic': {
        'Physical Power': {'mean': 75, 'std_dev': 8},
        'Ball Control': {'mean': 85, 'std_dev': 4},
        'Dribbling': {'mean': 85, 'std_dev': 4},
        'Jumping': {'mean': 75, 'std_dev': 8},
        'Acceleration': {'mean': 80, 'std_dev': 8},
        'Speed': {'mean': 80, 'std_dev': 8},
    },
    'Set Pieces': {
        'Free Kicks': {'mean': 70, 'std_dev': 15, 'min': 30, 'max': 90},
        'Penalty': {'mean': 80, 'std_dev': 15, 'min': 30, 'max': 90},
    },
}
