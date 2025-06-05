import os
import json

def get_all_seasons(base_dir="Seasons"):
    seasons = [s for s in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, s))]
    # Sort seasons chronologically using the first year
    return sorted(seasons, key=lambda s: int(s.split("-")[0]))

def load_previous_appearances(player_name, seasons_before, base_dir="Seasons"):
    for season in seasons_before:
        stats_folder = os.path.join(base_dir, season, "PlayerStats")
        if not os.path.exists(stats_folder):
            continue
        for fname in os.listdir(stats_folder):
            if not fname.endswith(".json"):
                continue
            try:
                with open(os.path.join(stats_folder, fname), "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data.get("PLAYER_NAME") == player_name:
                        gp = data.get("GP", 0)
                        if isinstance(gp, str):
                            gp = int(gp)
                        if gp > 0:
                            return True
            except Exception as e:
                print(f"Error reading {fname} in {season}: {e}")
    return False

def tag_rookie_status(base_dir="Seasons"):
    all_seasons = get_all_seasons(base_dir)

    for i, current_season in enumerate(all_seasons):
        stats_folder = os.path.join(base_dir, current_season, "PlayerStats")
        if not os.path.exists(stats_folder):
            continue
        print(f"🔍 Checking rookies in: {current_season}")
        for fname in os.listdir(stats_folder):
            if not fname.endswith(".json"):
                continue
            path = os.path.join(stats_folder, fname)
            try:
                with open(path, "r+", encoding="utf-8") as f:
                    data = json.load(f)
                    name = data.get("PLAYER_NAME")
                    if not name:
                        continue
                    played_before = load_previous_appearances(name, all_seasons[:i], base_dir)
                    data["Rookie"] = not played_before
                    f.seek(0)
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    f.truncate()
            except Exception as e:
                print(f"⚠️ Failed to update {fname}: {e}")



def dry_run_tag_rookie_status(base_dir="Seasons"):
    all_seasons = get_all_seasons(base_dir)

    for i, current_season in enumerate(all_seasons):
        stats_folder = os.path.join(base_dir, current_season, "PlayerStats")
        if not os.path.exists(stats_folder):
            continue
        print(f"\n🔍 DRY RUN - Checking rookies in: {current_season}")
        for fname in os.listdir(stats_folder):
            if not fname.endswith(".json"):
                continue
            path = os.path.join(stats_folder, fname)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    name = data.get("PLAYER_NAME")
                    if not name:
                        continue
                    played_before = load_previous_appearances(name, all_seasons[:i], base_dir)
                    rookie = not played_before
                    print(f" - {name}: {'Rookie ✅' if rookie else 'Not Rookie ❌'}")
            except Exception as e:
                print(f"⚠️ Failed to read {fname}: {e}")

if __name__ == "__main__":
    tag_rookie_status()
