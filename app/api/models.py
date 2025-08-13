# app/core/models.py

from pydantic import BaseModel
from typing import Dict, Any

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

    class Config:
        schema_extra = {
            "example": {
                "id": '688164b0-2ac5-4b8f-abd3-2c62459a356c',
                "name": "John Smith",
                "shirt_number": 10,
                "level":"Weaker | Normal | Excellent",
                "position": "Midfielder",
                "age": 28,
                "height": 180,
                "preferred_foot": {
                    "dominant_foot": "Right",
                    "weak_foot_level": 2
                },
                "stamina": 85,
                "fitness": "Peak",
                "nationality": "CountryA",
                "stats": {
                    "Mental": {
                        "Aggression": 75,
                        "Composure": 80,
                        "Decisions": 78,
                        "Teamwork": 82
                    },
                    "Athletic": {
                        "Acceleration": 85,
                        "ball_control": 88,
                        "Dribbling": 90,
                        "Heading": 70,
                        "Jumping": 75,
                        "physical_power": 80,
                        "Speed": 87
                    },
                    "Defense": {
                        "Tackling": 65,
                        "Marking": 70,
                        "Positioning": 75
                    },
                    "Attack": {
                        "Finishing": 60,
                        "long_shots": 62,
                        "off_the_ball": 68
                    },
                    "Playmaking": {
                        "Creative": 72,
                        "Passing": 80,
                        "Crossing": 75
                    },
                    "Set Pieces": {
                        "free_kicks": 55,
                        "Penalty": 60
                    }
                },
                "averages": {
                    "Mental": 79,
                    "Athletic": 83,
                    "Defense": 70,
                    "Attack": 63,
                    "Playmaking": 76,
                    "Set Pieces": 57
                }
            }
        }