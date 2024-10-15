# app/api/endpoints.py

from fastapi import HTTPException
from fastapi import APIRouter
from app.core.team_generator import generate_team
from app.core.models import PlayerModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

router = APIRouter()

# Define the allowed origins
origins = [
    "https://soccersimulator.github.io",  # Your GitHub Pages URL
]

# Add CORS middleware to allow requests from your GitHub Pages site
router.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows only specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@router.get("/team", response_model=List[PlayerModel], summary="Generate a team", description="Generates a soccer team and returns it as JSON.")
async def get_team():
    team = generate_team()
    team_data = [player.to_dict() for player in team]
    return team_data

@router.get("/team/player/{player_id}", summary="Get player by ID")
async def get_player(player_id: int):
    team = generate_team()
    if 0 <= player_id < len(team):
        player = team[player_id]
        return player.to_dict()
    else:
        raise HTTPException(status_code=404, detail="Player not found")

# Dummy endpoint for UptimeRobot HEAD request
@router.head("/uptime-check")
async def uptime_check():
    return {"message": "Uptime check"}