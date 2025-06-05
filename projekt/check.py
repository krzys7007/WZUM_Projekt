import os
import json

def load_player_stats_names(player_stats_dir):
    """Return a set of player names found in PlayerStats/*.json"""
    player_names = set()

    for filename in os.listdir(player_stats_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(player_stats_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    name = data.get("PLAYER_NAME")
                    if name:
                        player_names.add(name)
            except Exception as e:
                print(f"⚠️ Error reading {filepath}: {e}")

    return player_names

def extract_season_players(season_data_path):
    """Return a set of all player names in season_data.json"""
    with open(season_data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    players = set()

    # All-NBA
    nba_teams = data.get("all-nba", {})
    for team in nba_teams.values():
        players.update(team)

    # All-Rookie
    rookie_teams = data.get("all-rookie", {})
    for team in rookie_teams.values():
        players.update(team)

    return players

def check_missing_players(seasons_dir):
    for season in os.listdir(seasons_dir):
        season_path = os.path.join(seasons_dir, season)
        if not os.path.isdir(season_path):
            continue

        season_data_path = os.path.join(season_path, "season_data.json")
        player_stats_path = os.path.join(season_path, "PlayerStats")

        if not os.path.exists(season_data_path) or not os.path.exists(player_stats_path):
            continue

        print(f"\n🔍 Checking season: {season}")

        season_players = extract_season_players(season_data_path)
        stats_players = load_player_stats_names(player_stats_path)

        for player in sorted(season_players):
            if player not in stats_players:
                print(f"❌ Missing: {player}")

if __name__ == "__main__":
    check_missing_players("Seasons")
