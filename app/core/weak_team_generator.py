"""v1 wrapper kept for backwards compatibility. See app/core/generator.py."""
from app.core.generator import GenerationOptions, generate_squad


def generate_weak_team():
    return generate_squad(GenerationOptions(level='weaker', template='legacy', age_profile='legacy', legacy_excellent_min_age=True)).players
