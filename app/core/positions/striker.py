from app.core.player import Player


class Striker(Player):
    """Kept for backwards compatibility; position data lives in app/core/realism.py."""

    def __init__(self, level='normal', assigned_numbers: set = None, **kwargs):
        super().__init__('striker', level=level, assigned_numbers=assigned_numbers, **kwargs)
