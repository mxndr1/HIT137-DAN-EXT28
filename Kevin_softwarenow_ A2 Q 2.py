import pandas as pd
import glob

all_files = glob.glob("temperatures/*.csv")
dfs = []

for file in all_files:

    df = pd.read_csv(file)

    df.columns = df.columns.str.strip().str.lower()
    df = df.rename(columns={
        "station_id": "station",
        "temperature_c": "temperature"
    })
    dfs.append(df)

data = pd.concat(dfs, ignore_index=True)

print("Following name：", data.columns.tolist())

data["date"] = pd.to_datetime(data["date"], errors="coerce")

data = data.dropna(subset=["temperature"])

def get_season(month):
    if month in [12, 1, 2]:
        return "Summer"
    elif month in [3, 4, 5]:
        return "Autumn"
    elif month in [6, 7, 8]:
        return "Winter"
    else:
        return "Spring"

data["season"] = data["date"].dt.month.apply(get_season)

season_avg = data.groupby("season")["temperature"].mean()

with open("average_temp.txt", "w", encoding="utf-8") as f:
    for season, avg in season_avg.items():
        f.write(f"{season}: {avg:.1f}°C\n")

station_stats = data.groupby("station")["temperature"].agg(["max", "min"])
station_stats["range"] = station_stats["max"] - station_stats["min"]

max_range = station_stats["range"].max()
largest_range_stations = station_stats[station_stats["range"] == max_range]

with open("largest_temp_range_station.txt", "w", encoding="utf-8") as f:
    for station, row in largest_range_stations.iterrows():
        f.write(
            f"{station}: Range {row['range']:.1f}°C "
            f"(Max: {row['max']:.1f}°C, Min: {row['min']:.1f}°C)\n"
        )

stddev = data.groupby("station")["temperature"].std()

min_std = stddev.min()
max_std = stddev.max()

most_stable = stddev[stddev == min_std]
most_variable = stddev[stddev == max_std]

with open("temperature_stability_stations.txt", "w", encoding="utf-8") as f:
    for station, val in most_stable.items():
        f.write(f"Most Stable: {station}: StdDev {val:.1f}°C\n")
    for station, val in most_variable.items():
        f.write(f"Most Variable: {station}: StdDev {val:.1f}°C\n")

print("Successful!")
