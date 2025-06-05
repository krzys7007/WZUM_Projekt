import os
import json
import re
from collections import defaultdict

def parse_all_nba_file(file_path):
    teams_per_season = defaultdict(lambda: {
        "first-all-nba": [],
        "secound-all-nba": [],
        "third-all-nba": []
    })

    # Match names followed by a position like "Nikola Jokic C"
    position_pattern = re.compile(r"([A-Z][a-zA-Z.'\- ]+?)\s+[CFG]")

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 10:
                continue

            season = parts[0]
            team_label = parts[2]
            player_section = " ".join(parts[4:])

            players = position_pattern.findall(player_section)

            if team_label == "1st":
                key = "first-all-nba"
            elif team_label == "2nd":
                key = "secound-all-nba"
            elif team_label == "3rd":
                key = "third-all-nba"
            else:
                continue

            teams_per_season[season][key] = players

    return teams_per_season

def save_season_jsons(all_data):
    for season, teams in all_data.items():
        folder = os.path.join("Seasons", season)
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, "season_data.json")

        data = {
            "season": season,
            "all-nba": {
                "first-all-nba": teams["first-all-nba"],
                "secound-all-nba": teams["secound-all-nba"],
                "third-all-nba": teams["third-all-nba"]
            },
            "all-rookie": {
                "first-all-rookie": [],
                "secound-all-rookie": []
            }
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved: {path}")

if __name__ == "__main__":
    parsed = parse_all_nba_file("All-Time.txt")
    save_season_jsons(parsed)
