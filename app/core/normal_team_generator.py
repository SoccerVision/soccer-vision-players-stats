"""v1 wrapper kept for backwards compatibility. See app/core/generator.py."""
from app.core.generator import GenerationOptions, generate_squad


def generate_normal_team():
    return generate_squad(GenerationOptions(level='normal', template='legacy_core', age_profile='legacy')).players
