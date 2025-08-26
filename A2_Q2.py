# Group: DAN/EXT 28
# Members: Hendrick Dang – S395598, Mehraab Ferdouse – S393148,
#          Fateen Rahman – S387983, Kevin Zhu – S387035

import os
import pandas as pd
import math

# Read all CSV files in the temperatures folder into one DataFrame
def read_all_csv(folder):
    dfs = []
    for f in os.listdir(folder):
        if f.endswith(".csv"):
            path = os.path.join(folder, f)
            df = pd.read_csv(path)
            dfs.append(df)
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame()

# Calculate seasonal averages across all stations and years
def seasonal_avg(df):
    # NaN ignored by mean() automatically
    summer = df[['January','February','December']].mean().mean()
    autumn = df[['March','April','May']].mean().mean()
    winter = df[['June','July','August']].mean().mean()
    spring = df[['September','October','November']].mean().mean()
    return {'Summer':summer,'Autumn':autumn,'Winter':winter,'Spring':spring}

# Get all temps per station as a dict {station: [temps...]}
def temps_by_station(df):
    result = {}
    months = ['January','February','March','April','May','June','July',
              'August','September','October','November','December']
    for _, row in df.iterrows():
        st = row['STATION_NAME']
        vals = [v for v in row[months].tolist() if not (pd.isna(v))]
        if st not in result:
            result[st] = []
        result[st].extend(vals)
    return result

# Find station(s) with largest temperature range
def largest_range(st_dict):
    max_range = -math.inf
    info = {}
    for st, vals in st_dict.items():
        if not vals: 
            continue
        r = max(vals) - min(vals)
        if r > max_range:
            max_range = r
            info = {st:(r,max(vals),min(vals))}
        elif abs(r - max_range) < 1e-9:
            info[st] = (r,max(vals),min(vals))
    return info

# Find most stable and most variable station(s) by std dev
def stability(st_dict):
    stds = {}
    for st, vals in st_dict.items():
        if len(vals) >= 2:
            stds[st] = pd.Series(vals).std()
    if not stds:
        return [], []
    min_sd = min(stds.values())
    max_sd = max(stds.values())
    most_stable = [st for st,sd in stds.items() if abs(sd-min_sd)<1e-9]
    most_var = [st for st,sd in stds.items() if abs(sd-max_sd)<1e-9]
    return [(st,min_sd) for st in most_stable], [(st,max_sd) for st in most_var]

def main():
    folder = "temperatures"  # same folder as script
    df = read_all_csv(folder)
    if df.empty:
        print("No data found.")
        return

    # 1) Seasonal averages
    avgs = seasonal_avg(df)
    with open("average_temp.txt","w") as f:
        for s,v in avgs.items():
            f.write(f"{s}: {v:.1f}°C\n")

    # 2) Temps per station
    st_dict = temps_by_station(df)
    high_ranges = largest_range(st_dict)
    with open("largest_temp_range_station.txt","w") as f:
        for st,(r,mx,mn) in high_ranges.items():
            f.write(f"{st}: Range {r:.1f}°C (Max: {mx:.1f}°C, Min: {mn:.1f}°C)\n")

    # 3) Stability
    stable, variable = stability(st_dict)
    with open("temperature_stability_stations.txt","w") as f:
        for st,sd in stable:
            f.write(f"Most Stable: Station {st}: StdDev {sd:.2f}°C\n")
        for st,sd in variable:
            f.write(f"Most Variable: Station {st}: StdDev {sd:.2f}°C\n")

    print("Done writing results.")

if __name__ == "__main__":
    main()
