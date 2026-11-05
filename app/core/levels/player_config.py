# app/core/levels/player_config.py

from .player_configs.weaker_config import weaker_adjustments
from .player_configs.normal_config import normal_adjustments
from .player_configs.excellent_config import excellent_adjustments

from .player_configs.positions.defender_config import defender_stats
from .player_configs.positions.fullback_config import fullback_stats
from .player_configs.positions.goalkeeper_config import goalkeeper_stats
from .player_configs.positions.midfielder_config import midfielder_stats
from .player_configs.positions.striker_config import striker_stats
from .player_configs.positions.winger_config import winger_stats

def _soften_top(config, pivot=75):
    """The excellent level: every mean above `pivot` is pulled half way down to it (95 -> 85, 90 -> 82.5, 80 -> 77.5).
    FIFA 23 players rated 78+ average about 83 in the key skill of their position (GAME); configs of 90-95 put a quarter to
    two fifths of the excellent players' key skills at the 99 ceiling, so no star stood out from another. The spread and the
    role bonuses still take the best to 90+ - rare, as Messi, Ronaldo and Neymar are."""
    out = {}
    for category, stats in config.items():
        out[category] = {}
        for name, params in stats.items():
            params = dict(params)
            if 'mean' in params and params['mean'] > pivot:
                params['mean'] = round(pivot + (params['mean'] - pivot) / 2, 1)
            out[category][name] = params
    return out


player_config = {
    "levels": {
        "weaker": weaker_adjustments,
        "normal": normal_adjustments,
        "excellent": excellent_adjustments,
    },
    "positions": {
        "weaker": {
            "defender": defender_stats["weaker"],
            "fullback": fullback_stats["weaker"],
            "goalkeeper": goalkeeper_stats["weaker"],
            "midfielder": midfielder_stats["weaker"],
            "striker": striker_stats["weaker"],
            "winger": winger_stats["weaker"],
        },
        "normal": {
            "defender": defender_stats["normal"],
            "fullback": fullback_stats["normal"],
            "goalkeeper": goalkeeper_stats["normal"],
            "midfielder": midfielder_stats["normal"],
            "striker": striker_stats["normal"],
            "winger": winger_stats["normal"],
        },
        "excellent": {
            "defender": _soften_top(defender_stats["excellent"]),
            "fullback": _soften_top(fullback_stats["excellent"]),
            "goalkeeper": _soften_top(goalkeeper_stats["excellent"]),
            "midfielder": _soften_top(midfielder_stats["excellent"]),
            "striker": _soften_top(striker_stats["excellent"]),
            "winger": _soften_top(winger_stats["excellent"]),
        }
    }
}
