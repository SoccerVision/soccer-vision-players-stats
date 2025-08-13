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
            "defender": defender_stats["excellent"],
            "fullback": fullback_stats["excellent"],
            "goalkeeper": goalkeeper_stats["excellent"],
            "midfielder": midfielder_stats["excellent"],
            "striker": striker_stats["excellent"],
            "winger": winger_stats["excellent"],
        }
    }
}
