import os
import pandas as pd

SEASONS = {
    "December": "Summer", "January": "Summer", "February": "Summer",
    "March": "Autumn", "April": "Autumn", "May": "Autumn",
    "June": "Winter", "July": "Winter", "August": "Winter",
    "September": "Spring", "October": "Spring", "November": "Spring",
}
SEASON_ORDER = ["Summer", "Autumn", "Winter", "Spring"]
MONTH_COLS = ["January","February","March","April","May","June",
              "July","August","September","October","November","December"]

def load_all(folder="temperatures"):
    base_dir = os.path.dirname(__file__)
    folder_abs = os.path.abspath(os.path.join(base_dir, folder))

    # list all top-level .csv files
    files = [
        os.path.join(folder_abs, f)
        for f in os.listdir(folder_abs)
        if f.lower().endswith(".csv") and os.path.isfile(os.path.join(folder_abs, f))
    ]
    if not files:
        raise FileNotFoundError(f"No CSVs in {folder_abs}")

    dfs = []
    for path in files:
        try:
            df = pd.read_csv(path)
        except Exception:
            continue

        if "STATION_NAME" not in df.columns:
            continue
        if not all(m in df.columns for m in MONTH_COLS):
            continue

        tidy = df.melt(
            id_vars=["STATION_NAME"],
            value_vars=MONTH_COLS,
            var_name="month",
            value_name="temperature",
        ).dropna(subset=["temperature"])

        tidy["season"] = tidy["month"].map(SEASONS)
        dfs.append(tidy)

    if not dfs:
        raise ValueError("No usable files (need STATION_NAME and all 12 month columns).")
    return pd.concat(dfs, ignore_index=True)

def write_seasonal_average(data, out_path="average_temp.txt"):
    s = data.groupby("season")["temperature"].mean()
    lines = [f"{season}: {s[season]:.1f}°C" for season in SEASON_ORDER if season in s.index]
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def write_largest_range(data, out_path="largest_temp_range_station.txt"):
    agg = data.groupby("STATION_NAME")["temperature"].agg(["min", "max"])
    agg["range"] = agg["max"] - agg["min"]
    max_range = agg["range"].max()
    winners = agg[agg["range"] == max_range].sort_index()

    lines = [
        f"{st}: Range {row['range']:.1f}°C (Max: {row['max']:.1f}°C, Min: {row['min']:.1f}°C)"
        for st, row in winners.iterrows()
    ]
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def write_stability(data, out_path="temperature_stability_stations.txt"):
    std = data.groupby("STATION_NAME")["temperature"].std(ddof=1).dropna()
    min_std, max_std = std.min(), std.max()
    most_stable = std[std == min_std].sort_index()
    most_variable = std[std == max_std].sort_index()

    lines = [f"Most Stable: {st}: StdDev {min_std:.1f}°C" for st in most_stable.index]
    lines += [f"Most Variable: {st}: StdDev {max_std:.1f}°C" for st in most_variable.index]
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def main():
    data = load_all("temperatures")
    write_seasonal_average(data, "average_temp.txt")
    write_largest_range(data, "largest_temp_range_station.txt")
    write_stability(data, "temperature_stability_stations.txt")

if __name__ == "__main__":
    main()