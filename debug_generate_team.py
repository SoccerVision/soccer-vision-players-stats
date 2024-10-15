from app.core.team_generator import generate_team  # Assuming your file structure

def debug_generate_team():
    print("Generating team...")
    
    # Call the generate_team function
    team = generate_team()
    
    # Print each player's details
    for player in team:
        print(player.to_dict())  # Assuming player has a `to_dict()` method to get all details

if __name__ == "__main__":
    debug_generate_team()