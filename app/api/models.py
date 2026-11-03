# app/api/models.py

from typing import Any, Dict

from pydantic import BaseModel, ConfigDict


class PlayerModel(BaseModel):
    id: str
    name: str
    shirt_number: int
    position: str
    level: str
    age: int
    height: int
    preferred_foot: Dict[str, Any]
    stamina: int
    fitness: str
    nationality: str
    stats: Dict[str, Dict[str, int]]
    averages: Dict[str, int]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "688164b0-2ac5-4b8f-abd3-2c62459a356c",
                "name": "John Smith",
                "shirt_number": 10,
                "position": "midfielder",
                "level": "Normal",
                "age": 26,
                "height": 179,
                "preferred_foot": {"dominant_foot": "Right", "weak_foot_level": 2},
                "stamina": 74,
                "fitness": "Moderate",
                "nationality": "CountryA",
                "stats": {
                    "mental": {"aggression": 41, "teamwork": 68, "decisions": 55, "composure": 52},
                    "defense": {"tackling": 49, "marking": 51, "positioning": 50},
                    "attack": {"finishing": 50, "long_shots": 61, "off_the_ball": 56},
                    "playmaking": {"creative": 70, "passing": 73, "crossing": 69},
                    "athletic": {
                        "physical_power": 58,
                        "ball_control": 61,
                        "dribbling": 60,
                        "jumping": 57,
                        "acceleration": 62,
                        "speed": 60,
                        "heading": 58,
                    },
                    "set_pieces": {"free_kicks": 55, "penalty": 63},
                },
                "averages": {
                    "mental": 54,
                    "defense": 50,
                    "attack": 56,
                    "playmaking": 71,
                    "athletic": 59,
                    "set_pieces": 59,
                },
            }
        }
    )
