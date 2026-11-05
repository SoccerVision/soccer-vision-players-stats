# app/api/endpoints.py

from fastapi import HTTPException
from fastapi import APIRouter
from typing import List

from app.api.models import PlayerModel
from app.version import V1_TAG
from app.core.team_generator import generate_team
from app.core.weak_team_generator import generate_weak_team
from app.core.normal_team_generator import generate_normal_team
from app.core.excellent_team_generator import generate_excellent_team
from app.core.younger_team_generator import generate_young_team

router = APIRouter(tags=[V1_TAG])


@router.get("/team", response_model=List[PlayerModel], summary="Generate a team",
            description="Generates a soccer team and returns it as JSON.")
def get_team():
    team = generate_team()
    team_data = [player.to_dict() for player in team]
    return team_data


@router.get("/team/weaker", response_model=List[PlayerModel], summary="Generate a weaker team",
            description="Generates a weaker soccer team and returns it as JSON.")
def get_weaker_team():
    team = generate_weak_team()
    team_data = [player.to_dict() for player in team]
    return team_data


@router.get("/team/normal", response_model=List[PlayerModel], summary="Generate a normal team",
            description="Generates a normal soccer team and returns it as JSON.")
def get_normal_team():
    team = generate_normal_team()
    team_data = [player.to_dict() for player in team]
    return team_data


@router.get("/team/excellent", response_model=List[PlayerModel], summary="Generate a excellent team",
            description="Generates a excellent soccer team and returns it as JSON.")
def get_excellent_team():
    team = generate_excellent_team()
    team_data = [player.to_dict() for player in team]
    return team_data


@router.get("/team/younger", response_model=List[PlayerModel], summary="Generate a young team",
            description="Generates a young soccer team and returns it as JSON.")
def get_young_team():
    team = generate_young_team()
    team_data = [player.to_dict() for player in team]
    return team_data


@router.get("/team/player/{player_id}", response_model=PlayerModel, summary="Get player by index",
            description="Returns player `player_id` (0-based index) from a freshly generated normal team. "
                        "Random on every call; use `/api/v2/team/{seed}/player/{index}` for a stable result.")
def get_player(player_id: int):
    team = generate_normal_team()
    if 0 <= player_id < len(team):
        player = team[player_id]
        return player.to_dict()
    else:
        raise HTTPException(status_code=404, detail="Player not found")


# Dummy endpoint for UptimeRobot HEAD request
@router.head("/uptime-check", include_in_schema=False)
async def uptime_check():
    return {"message": "Uptime check"}
