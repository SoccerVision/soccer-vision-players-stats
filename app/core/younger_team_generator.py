"""v1 wrapper kept for backwards compatibility. See app/core/generator.py."""
from app.core.generator import GenerationOptions, generate_squad


def generate_young_team():
    return generate_squad(GenerationOptions(level='mixed', template='youth', age_profile='youth')).players
