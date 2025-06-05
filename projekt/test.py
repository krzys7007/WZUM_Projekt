import os
import json
import time
from nba_api.stats.endpoints import leaguedashplayerstats
from nba_api.stats.library.parameters import SeasonType

def get_season_string(start_year):
    """Returns NBA season string like '2000-01'"""
    return f"{start_year}-{str(start_year + 1)[-2:]}"

def save_player_stats(season: str, df):
    folder = f"Seasons/{season}/PlayerStats"
    os.makedirs(folder, exist_ok=True)
    for _, row in df.iterrows():
        player_name = row['PLAYER_NAME'].replace(" ", "_").replace(".", "")
        path = os.path.join(folder, f"{player_name}.json")
        with open(path, 'w') as f:
            json.dump(row.to_dict(), f, indent=2)

def fetch_and_save_season_stats(season: str):
    print(f"Fetching stats for {season}...")
    try:
        stats = leaguedashplayerstats.LeagueDashPlayerStats(
            season=season,
            season_type_all_star=SeasonType.regular
        )
        df = stats.get_data_frames()[0]
        save_player_stats(season, df)
        print(f"Saved {len(df)} player files for {season}")
    except Exception as e:
        print(f"Failed to fetch stats for {season}: {e}")

def main(start_year=2000, end_year=2025):
    for year in range(start_year, end_year):
        season = get_season_string(year)
        fetch_and_save_season_stats(season)
        time.sleep(1)  # Respectful delay to avoid rate limits

if __name__ == "__main__":
    main()
