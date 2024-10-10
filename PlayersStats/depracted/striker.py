# striker.py

import random

def calculate_averages(player_stats):
    averages = {}
    for category, stats in player_stats.items():
        avg = sum(stats.values()) / len(stats)
        averages[category] = round(avg)
    return averages

def generate_striker_stats():
    # Helper function with truncated normal distribution
    def generate_stat(mean, std_dev, min_value=0, max_value=99):
        while True:
            value = random.gauss(mean, std_dev)
            if min_value <= value <= max_value:
                return round(value)

    # Configuration for Striker stats
    stat_config = {
        'Mental': {
            'Aggression': {'mean': 50, 'std_dev': 15, 'min': 10, 'max': 90},
            'Teamwork': {'mean': 50, 'std_dev': 8},
            'Decisions': {'mean': 50, 'std_dev': 6},
            'Composure': {'mean': 60, 'std_dev': 4},
        },
        'Defense': {
            'Tackling': {'mean': 25, 'std_dev': 4},
            'Marking': {'mean': 25, 'std_dev': 4},
            'Positioning': {'mean': 30, 'std_dev': 4},
        },
        'Attack': {
            'Finishing': {'mean': 65, 'std_dev': 4},
            'Long Shots': {'mean': 65, 'std_dev': 4},
            'Off The Ball': {'mean': 65, 'std_dev': 4},
        },
        'Playmaking': {
            'Creative': {'mean': 50, 'std_dev': 4},
            'Passing': {'mean': 50, 'std_dev': 4},
            'Crossing': {'mean': 50, 'std_dev': 4},
        },
        'Athletic': {
            'Physical Power': {'mean': 55, 'std_dev': 8},
            'Ball Control': {'mean': 60, 'std_dev': 4},
            'Dribbling': {'mean': 60, 'std_dev': 4},
            'Jumping': {'mean': 55, 'std_dev': 8},
            'Acceleration': {'mean': 60, 'std_dev': 8},
            'Speed': {'mean': 60, 'std_dev': 8},
        },
    }

    player_stats = {}

    # Generate stats
    for category, stats in stat_config.items():
        category_stats = {}
        for stat_name, params in stats.items():
            mean = params.get('mean', 50)
            std_dev = params.get('std_dev', 4)
            min_value = params.get('min', 0)
            max_value = params.get('max', 99)
            category_stats[stat_name] = generate_stat(mean, std_dev, min_value, max_value)
        player_stats[category] = category_stats

    # Additional calculations
    athletic_stats = player_stats['Athletic']
    athletic_stats['Heading'] = generate_stat(athletic_stats['Jumping'], 4)

    # Balancing logic
    speed_stats = [athletic_stats['Speed'], athletic_stats['Acceleration'], athletic_stats['Dribbling']]
    heading_stats = [athletic_stats['Jumping'], athletic_stats['Heading']]

    if all(stat < 50 for stat in speed_stats):
        athletic_stats['Jumping'] = max(athletic_stats['Jumping'], 65)
        athletic_stats['Heading'] = max(athletic_stats['Heading'], 65)
    elif all(stat < 50 for stat in heading_stats):
        athletic_stats['Speed'] = max(athletic_stats['Speed'], 65)
        athletic_stats['Acceleration'] = max(athletic_stats['Acceleration'], 65)
        athletic_stats['Dribbling'] = max(athletic_stats['Dribbling'], 60)

    if athletic_stats['Jumping'] > 65:
        athletic_stats['Physical Power'] = max(athletic_stats['Physical Power'], 65)

    if athletic_stats['Acceleration'] < 57 or athletic_stats['Speed'] < 57:
        athletic_stats['Physical Power'] = generate_stat(70, 4)

    return player_stats

def get_striker_stats():
    stats = generate_striker_stats()
    averages = calculate_averages(stats)
    return stats, averages