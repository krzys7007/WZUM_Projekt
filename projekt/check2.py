import os
import json

def load_player_stats_names(player_stats_folder):
    player_names = set()
    for filename in os.listdir(player_stats_folder):
        if filename.endswith(".json"):
            filepath = os.path.join(player_stats_folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    name = data.get("PLAYER_NAME")
                    if name:
                        player_names.add(name.strip())
                except Exception as e:
                    print(f"Failed to parse {filepath}: {e}")
    return player_names

def load_players_from_season_data(season_data_path):
    with open(season_data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Combine all-nba + all-rookie
    all_players = set()
    for team in data["all-nba"].values():
        all_players.update(player.strip() for player in team)
    for team in data["all-rookie"].values():
        all_players.update(player.strip() for player in team)

    return all_players

def check_missing_players(season_folder):
    season_data_path = os.path.join(season_folder, "season_data.json")
    player_stats_folder = os.path.join(season_folder, "PlayerStats")

    if not os.path.exists(season_data_path):
        print(f"Missing: {season_data_path}")
        return
    if not os.path.exists(player_stats_folder):
        print(f"Missing: {player_stats_folder}")
        return

    expected_players = load_players_from_season_data(season_data_path)
    available_players = load_player_stats_names(player_stats_folder)

    for player in sorted(expected_players):
        if player not in available_players:
            print(f"🚫 Missing in {season_folder}: {player}")

if __name__ == "__main__":
    base_dir = "Seasons"
    for season in os.listdir(base_dir):
        season_path = os.path.join(base_dir, season)
        if os.path.isdir(season_path):
            check_missing_players(season_path)
