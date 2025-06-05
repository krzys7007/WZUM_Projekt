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

    # Match any name ending before a position letter
    pattern = re.compile(r"([A-Z][a-zA-Z.'\-]+(?:\s+[A-Z][a-zA-Z.'\-]+)*)\s+[CFG]")

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 10:
                continue

            season = parts[0]
            team_label = parts[2]
            player_section = " ".join(parts[4:])

            players = pattern.findall(player_section)

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


def parse_all_rookie_file(file_path):
    from collections import defaultdict
    import re

    rookie_per_season = defaultdict(lambda: {
        "first-all-rookie": [],
        "secound-all-rookie": []
    })

    name_pattern = re.compile(r"\b[A-Z][a-zA-Z.'\-]+\s[A-Z][a-zA-Z.'\-]+\b")

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 8:
                continue

            season = parts[0]
            team_label = parts[2]
            player_section = " ".join(parts[4:])

            players = name_pattern.findall(player_section)

            if team_label == "1st":
                key = "first-all-rookie"
            elif team_label == "2nd":
                key = "secound-all-rookie"
            else:
                continue

            rookie_per_season[season][key] = players

    return rookie_per_season




def merge_and_save(all_nba, all_rookie):
    all_seasons = set(all_nba.keys()).union(all_rookie.keys())

    for season in all_seasons:
        folder = os.path.join("Seasons", season)
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, "season_data.json")

        data = {
            "season": season,
            "all-nba": all_nba.get(season, {
                "first-all-nba": [],
                "secound-all-nba": [],
                "third-all-nba": []
            }),
            "all-rookie": all_rookie.get(season, {
                "first-all-rookie": [],
                "secound-all-rookie": []
            })
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved: {path}")

if __name__ == "__main__":
    nba_file = "All-Time.txt"
    rookie_file = "All-Rookie.txt"

    all_nba_data = parse_all_nba_file(nba_file)
    all_rookie_data = parse_all_rookie_file(rookie_file)
    merge_and_save(all_nba_data, all_rookie_data)
