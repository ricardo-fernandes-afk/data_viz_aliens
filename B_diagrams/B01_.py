import pandas as pd
import matplotlib.pyplot as plt

# KORREKTER DATEIPFAD – bitte sicherstellen, dass Datei vorhanden ist
path = r"C:\Users\FLJ\OneDrive - Hochschule Luzern\Share_JRS\04_Frühlingssemster25\07_DataVis\04_JayRiciTill\data_viz_aliens\C_API\ufo_cleaned.csv"
df = pd.read_csv(path)

# Sichtungen pro Jahr berechnen
sightings_per_year = df['year'].value_counts().sort_index()

# Rolling Average berechnen
rolling_avg = sightings_per_year.rolling(window=5, center=True).mean()

# Wichtige Ereignisse hervorheben
highlight_years = {
    1997: "Phoenix Lights",
    2001: "Post-9/11 spike",
    2004: "USS Nimitz",
    2020: "Pentagon video"
}

# Plot im Sci-Fi-Stil
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(14, 7))

# Linien zeichnen
ax.plot(sightings_per_year.index, sightings_per_year.values, color='#39FF14', alpha=0.4, label='Sightings (raw)')
ax.plot(rolling_avg.index, rolling_avg.values, color='white', linewidth=2.5, label='5-Year Rolling Avg')

# Titel und Achsen
ax.set_title("When the Sky Went Crazy", fontsize=18, fontweight='bold', color='white', pad=20)
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Number of Sightings", fontsize=12)
ax.grid(True, linestyle='--', alpha=0.3)
ax.legend()

# Annotationen einfügen
for year, label in highlight_years.items():
    if year in sightings_per_year.index:
        y_val = sightings_per_year[year]
        ax.annotate(f"{label}",
                    xy=(year, y_val),
                    xytext=(year, y_val + 500),
                    arrowprops=dict(facecolor='white', arrowstyle='->'),
                    fontsize=10,
                    color='white',
                    ha='center')

plt.tight_layout()
plt.show()
