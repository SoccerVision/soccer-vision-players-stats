# app/core/models.py

from pydantic import BaseModel
from typing import Dict, Any

class PlayerModel(BaseModel):
    ID: str
    Name: str
    Shirt_Number: int
    Position: str
    Age: int
    Height: int
    Preferred_Foot: Dict[str, Any]
    Stamina: int
    Fitness: str
    Nationality: str
    Stats: Dict[str, Dict[str, int]]
    Averages: Dict[str, int]

    class Config:
        schema_extra = {
            "example": {
                "ID": '688164b0-2ac5-4b8f-abd3-2c62459a356c',
                "Name": "John Smith",
                "Shirt_Number": 10,
                "Position": "Midfielder",
                "Age": 28,
                "Height": 180,
                "Preferred_Foot": {
                    "Dominant Foot": "Right",
                    "Weak Foot Level": 2
                },
                "Stamina": 85,
                "Fitness": "Peak",
                "Nationality": "CountryA",
                "Stats": {
                    "Mental": {
                        "Aggression": 75,
                        "Composure": 80,
                        "Decisions": 78,
                        "Teamwork": 82
                    },
                    "Athletic": {
                        "Acceleration": 85,
                        "Ball Control": 88,
                        "Dribbling": 90,
                        "Heading": 70,
                        "Jumping": 75,
                        "Physical Power": 80,
                        "Speed": 87
                    },
                    "Defense": {
                        "Tackling": 65,
                        "Marking": 70,
                        "Positioning": 75
                    },
                    "Attack": {
                        "Finishing": 60,
                        "Long Shots": 62,
                        "Off The Ball": 68
                    },
                    "Playmaking": {
                        "Creative": 72,
                        "Passing": 80,
                        "Crossing": 75
                    },
                    "Set Pieces": {
                        "Free Kicks": 55,
                        "Penalty": 60
                    }
                },
                "Averages": {
                    "Mental": 79,
                    "Athletic": 83,
                    "Defense": 70,
                    "Attack": 63,
                    "Playmaking": 76,
                    "Set Pieces": 57
                }
            }
        }