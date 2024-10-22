from app.core.levels.player_configs.weaker_config import weaker_adjustments
from app.core.levels.player_configs.normal_config import normal_adjustments
from app.core.levels.player_configs.excellent_config import excellent_adjustments

goalkeeper_stats = {
    "weaker": {
        **weaker_adjustments,
        'Mental': {
            **weaker_adjustments["Mental"],
            'Composure': {'mean': 35, 'std_dev': 6},
        },
        'Set Pieces': {
            **weaker_adjustments["Set Pieces"],
            'Free Kicks': {'mean': 20, 'std_dev': 5, 'min': 20, 'max': 55},
            'Penalty': {'mean': 20, 'std_dev': 5, 'min': 20, 'max': 55},
        },
        'Goalkeeping': {
            'Aerial Ability': {'mean': 55, 'std_dev': 4},
            'Handling': {'mean': 60, 'std_dev': 4},
            'Kicking': {'mean': 45, 'std_dev': 4},
            'One on One': {'mean': 57, 'std_dev': 4},
            'Reflexes': {'mean': 42, 'std_dev': 4},
        },
        'Athletic': {
            **weaker_adjustments["Athletic"],
            'Physical Power': {'mean': 55, 'std_dev': 8},
            'Ball Control': {'mean': 35, 'std_dev': 4},
            'Dribbling': {'mean': 25, 'std_dev': 4},
            'Jumping': {'mean': 55, 'std_dev': 8},
            'Acceleration': {'mean': 40, 'std_dev': 8},
            'Speed': {'mean': 40, 'std_dev': 8},
        },
    },
    "normal": {
        **normal_adjustments,
        'Set Pieces': {
            **normal_adjustments["Set Pieces"],
            'Free Kicks': {'mean': 30, 'std_dev': 5, 'min': 20, 'max': 50},
            'Penalty': {'mean': 30, 'std_dev': 5, 'min': 20, 'max': 50},
        },
        "Goalkeeping": {
            'Aerial Ability': {'mean': 70, 'std_dev': 4},
            'Handling': {'mean': 75, 'std_dev': 4},
            'Kicking': {'mean': 60, 'std_dev': 4},
            'One on One': {'mean': 72, 'std_dev': 4},
            'Reflexes': {'mean': 75, 'std_dev': 4},
        },
        'Athletic': {
            **normal_adjustments["Athletic"],
            'Physical Power': {'mean': 70, 'std_dev': 8},
            'Ball Control': {'mean': 50, 'std_dev': 4},
            'Dribbling': {'mean': 40, 'std_dev': 4},
            'Jumping': {'mean': 70, 'std_dev': 8},
            'Acceleration': {'mean': 55, 'std_dev': 8},
            'Speed': {'mean': 55, 'std_dev': 8},
        },
    },
    "excellent": {
        **excellent_adjustments,
        'Goalkeeping': {
            'Aerial Ability': {'mean': 90, 'std_dev': 4},
            'Handling': {'mean': 95, 'std_dev': 4},
            'Kicking': {'mean': 80, 'std_dev': 4},
            'One on One': {'mean': 92, 'std_dev': 4},
            'Reflexes': {'mean': 95, 'std_dev': 4},
        },
        "Set Pieces": {
            **excellent_adjustments["Set Pieces"],
            'Free Kicks': {'mean': 50, 'std_dev': 5, 'min': 20, 'max': 70},
            'Penalty': {'mean': 50, 'std_dev': 5, 'min': 20, 'max': 70},
        },
        'Athletic': {
            **excellent_adjustments["Athletic"],
            'Physical Power': {'mean': 90, 'std_dev': 8},
            'Ball Control': {'mean': 70, 'std_dev': 4},
            'Dribbling': {'mean': 60, 'std_dev': 4},
            'Jumping': {'mean': 90, 'std_dev': 8},
            'Acceleration': {'mean': 75, 'std_dev': 8},
            'Speed': {'mean': 75, 'std_dev': 8},
        },
    }
}
