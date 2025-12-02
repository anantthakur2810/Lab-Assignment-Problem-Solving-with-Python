import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv(r"C:\Users\Anant\Desktop\Python\Assignment_4\weather.csv")
print("Shape:", df.shape)
print(df.head())
print(df.describe())

df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")

df = df[["date", "meantemp", "humidity", "wind_speed", "meanpressure"]]

df["meantemp"] = df["meantemp"].fillna(df["meantemp"].mean())
df["humidity"] = df["humidity"].fillna(df["humidity"].mean())
df["wind_speed"] = df["wind_speed"].fillna(df["wind_speed"].mean())
df["meanpressure"] = df["meanpressure"].fillna(df["meanpressure"].mean())

df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month

temp = df["meantemp"].values
rain = np.zeros(len(df))
hum = df["humidity"].values

print("\nOverall stats:")
print("Temp  mean:", np.mean(temp), " min:", np.min(temp), " max:", np.max(temp), " std:", np.std(temp))
print("Hum   mean:", np.mean(hum), " min:", np.min(hum), " max:", np.max(hum), " std:", np.std(hum))

print("\nMonthly stats (temp, humidity, pressure):")
monthly_stats = df.groupby(["year", "month"])[["meantemp", "humidity", "meanpressure"]].agg(["mean", "min", "max", "std"])
print(monthly_stats)

print("\nYearly stats:")
yearly_stats = df.groupby("year")[["meantemp", "humidity", "meanpressure"]].agg(["mean", "min", "max", "std"])
print(yearly_stats)

plt.style.use("seaborn-v0_8")

plt.figure(figsize=(10, 4))
plt.plot(df["date"], df["meantemp"], color="red")
plt.title("Daily Mean Temperature")
plt.xlabel("Date")
plt.ylabel("Mean Temperature")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("daily_temperature.png")
plt.close()

monthly_pressure = df.groupby(["year", "month"])["meanpressure"].sum().reset_index()
monthly_pressure["year_month"] = monthly_pressure["year"].astype(str) + "-" + monthly_pressure["month"].astype(str)

plt.figure(figsize=(10, 4))
plt.bar(monthly_pressure["year_month"], monthly_pressure["meanpressure"], color="blue")
plt.title("Monthly Pressure (used as rainfall-style bar)")
plt.xlabel("Year-Month")
plt.ylabel("Total Pressure")
plt.xticks(rotation=90, fontsize=8)
plt.tight_layout()
plt.savefig("monthly_pressure_bar.png")
plt.close()

plt.figure(figsize=(6, 4))
plt.scatter(df["meantemp"], df["humidity"], alpha=0.5, c="green")
plt.title("Humidity vs Temperature")
plt.xlabel("Mean Temperature")
plt.ylabel("Humidity")
plt.tight_layout()
plt.savefig("humidity_vs_temp.png")
plt.close()

fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

axes[0].plot(df["date"], df["meantemp"], color="red")
axes[0].set_title("Daily Mean Temperature")
axes[0].set_ylabel("Temp")

axes[1].plot(df["date"], df["humidity"], color="blue")
axes[1].set_title("Daily Humidity")
axes[1].set_xlabel("Date")
axes[1].set_ylabel("Humidity")

for ax in axes:
    ax.tick_params(axis="x", rotation=45)

plt.tight_layout()
plt.savefig("temp_humidity_combined.png")
plt.close()

def season_from_month(m):
    if m in [12, 1, 2]:
        return "Winter"
    elif m in [3, 4, 5]:
        return "Spring"
    elif m in [6, 7, 8]:
        return "Summer"
    else:
        return "Autumn"

df["season"] = df["month"].apply(season_from_month)

print("\nMonthly aggregation:")
print(df.groupby(["year", "month"])[["meantemp", "humidity", "meanpressure"]].agg(["mean", "min", "max"]))

print("\nSeasonal aggregation:")
print(df.groupby("season")[["meantemp", "humidity", "meanpressure"]].agg(["mean", "min", "max", "std"]))

df.to_csv("cleaned_weather.csv", index=False)
print("\nSaved cleaned_weather.csv and all plots.")
