"""v1 wrapper kept for backwards compatibility. See app/core/generator.py."""
from app.core.generator import GenerationOptions, generate_squad


def generate_excellent_team():
    return generate_squad(GenerationOptions(level='excellent', template='legacy', age_profile='legacy', legacy_excellent_min_age=True)).players
