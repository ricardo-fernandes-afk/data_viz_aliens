#UFOs Love Holidays?
import pandas as pd
import matplotlib.pyplot as plt

# Datei laden
path = r"C:\Users\FLJ\OneDrive - Hochschule Luzern\Share_JRS\04_Frühlingssemster25\07_DataVis\04_JayRiciTill\data_viz_aliens\C_API\ufo_cleaned.csv"
df = pd.read_csv(path)

# Datum bereinigen
df['date'] = pd.to_datetime(df['datetime'], errors='coerce')
df = df.dropna(subset=['date'])

# Liste relevanter Feiertage (monat/tag)
key_dates = {
    '01-01': "New Year's Day",
    '04-01': "April Fools",
    '07-04': "Independence Day",
    '10-31': "Halloween",
    '12-25': "Christmas",
    '12-31': "New Year's Eve"
}

# Spalte für MM-TT extrahieren
df['month_day'] = df['date'].dt.strftime('%m-%d')

# Zählen, wie oft Sichtungen an den Feiertagen waren
counts = df['month_day'].value_counts()
holiday_counts = {key_dates[k]: counts.get(k, 0) for k in key_dates}

# Plot
plt.style.use('dark_background')
plt.figure(figsize=(10, 6))
labels = list(holiday_counts.keys())
values = list(holiday_counts.values())
colors = ['#FFE600', '#00D1FF', '#FF5733', '#C70039', '#9D00FF', '#00FF7F']

plt.bar(labels, values, color=colors, edgecolor='white')

plt.title("Do UFO Sightings Spike on Holidays?", fontsize=16, fontweight='bold', pad=20)
plt.ylabel("Number of Sightings")
plt.grid(axis='y', linestyle='--', alpha=0.4)

plt.figtext(0.5, -0.05,
            "Spikes on Halloween & July 4th suggest fireworks might fool the skywatchers.",
            wrap=True, horizontalalignment='center', fontsize=10, style='italic', color='white')

plt.tight_layout()
plt.show()
