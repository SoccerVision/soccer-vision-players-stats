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
            "Defender": defender_stats["weaker"],
            "Fullback": fullback_stats["weaker"],
            "Goalkeeper": goalkeeper_stats["weaker"],
            "Midfielder": midfielder_stats["weaker"],
            "Striker": striker_stats["weaker"],
            "Winger": winger_stats["weaker"],
        },
        "normal": {
            "Defender": defender_stats["normal"],
            "Fullback": fullback_stats["normal"],
            "Goalkeeper": goalkeeper_stats["normal"],
            "Midfielder": midfielder_stats["normal"],
            "Striker": striker_stats["normal"],
            "Winger": winger_stats["normal"],
        },
        "excellent": {
            "Defender": defender_stats["excellent"],
            "Fullback": fullback_stats["excellent"],
            "Goalkeeper": goalkeeper_stats["excellent"],
            "Midfielder": midfielder_stats["excellent"],
            "Striker": striker_stats["excellent"],
            "Winger": winger_stats["excellent"],
        }
    }
}
