import os
import json

def load_rookies_from_season_data(season_data_path):
    with open(season_data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    rookies = set()
    for team in data.get("all-rookie", {}).values():
        rookies.update(player.strip() for player in team)
    return rookies

def check_rookie_tags(season_folder):
    season_data_path = os.path.join(season_folder, "season_data.json")
    player_stats_folder = os.path.join(season_folder, "PlayerStats")

    if not os.path.exists(season_data_path):
        print(f"❌ Missing: {season_data_path}")
        return
    if not os.path.exists(player_stats_folder):
        print(f"❌ Missing: {player_stats_folder}")
        return

    rookie_names = load_rookies_from_season_data(season_data_path)

    print(f"\n🔎 Checking rookie tags in: {season_folder}")
    for rookie_name in sorted(rookie_names):
        found = False
        for fname in os.listdir(player_stats_folder):
            if not fname.endswith(".json"):
                continue
            fpath = os.path.join(player_stats_folder, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data.get("PLAYER_NAME", "").strip() == rookie_name:
                        found = True
                        if data.get("Rookie") is not True:
                            print(f"🚫 Rookie tag missing or incorrect for: {rookie_name}")
                        break
            except Exception as e:
                print(f"⚠️ Error reading {fpath}: {e}")
        if not found:
            print(f"🚫 Rookie not found in PlayerStats: {rookie_name}")

if __name__ == "__main__":
    base_dir = "Seasons"
    for season in os.listdir(base_dir):
        season_path = os.path.join(base_dir, season)
        if os.path.isdir(season_path):
            check_rookie_tags(season_path)
