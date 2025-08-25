import pandas as pd
import glob

# 读取所有 CSV 文件
all_files = glob.glob("temperatures/*.csv")
dfs = []

for file in all_files:
    # 默认逗号分隔
    df = pd.read_csv(file)
    # 清理列名：去掉空格，统一小写
    df.columns = df.columns.str.strip().str.lower()
    # 重命名列，使程序通用
    df = df.rename(columns={
        "station_id": "station",
        "temperature_c": "temperature"
    })
    dfs.append(df)

# 合并所有文件
data = pd.concat(dfs, ignore_index=True)

# 检查列名
print("列名：", data.columns.tolist())

# 转换日期
data["date"] = pd.to_datetime(data["date"], errors="coerce")

# 忽略缺失温度
data = data.dropna(subset=["temperature"])

# -------------------------------
# 功能 1：计算四季平均温度
# -------------------------------
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

# -------------------------------
# 功能 2：温差最大的站点
# -------------------------------
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

# -------------------------------
# 功能 3：温度稳定性分析
# -------------------------------
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

print("✅ 分析完成，结果已保存到 txt 文件。")
