from app.core.player import Player


class Fullback(Player):
    """Kept for backwards compatibility; position data lives in app/core/realism.py."""

    def __init__(self, level='normal', dominant_foot=None, assigned_numbers: set = None, **kwargs):
        super().__init__('fullback', level=level, assigned_numbers=assigned_numbers,
                         dominant_foot=dominant_foot, **kwargs)
