# main.py

from team_generator import generate_team
from team_exporter import export_team_to_json
from team_printer import print_team

def main():
    team = generate_team()
    export_team_to_json(team, filename='team.json')
    print_team(team)

if __name__ == "__main__":
    main()