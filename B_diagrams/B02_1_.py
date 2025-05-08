import pandas as pd
import matplotlib.pyplot as plt

# CSV-Datei laden
path = r"C:\Users\FLJ\OneDrive - Hochschule Luzern\Share_JRS\04_Frühlingssemster25\07_DataVis\04_JayRiciTill\data_viz_aliens\C_API\ufo_cleaned.csv"
df = pd.read_csv(path)

# Sichtungen pro Monat berechnen
sightings_per_month = df['month'].value_counts().sort_index()

# Monatsnamen
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Farben – Sommermonate hervorheben (Jun, Jul, Aug)
colors = ['#888888'] * 12
for i in [5, 6, 7]:  # Juni, Juli, August (Index 5, 6, 7)
    colors[i] = '#FF5733'  # Orange-Rot

# Plot – Darkmode
plt.style.use('dark_background')
plt.figure(figsize=(10, 5))
plt.bar(months, sightings_per_month.values, color=colors)

plt.title("Aliens Love Summer Nights", fontsize=16, fontweight='bold', color='white', pad=20)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Total UFO Sightings", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.4)

# Zusatztext unterhalb
plt.figtext(0.5, -0.05,
            "Most sightings happen in summer – apparently, aliens also enjoy BBQ season.",
            wrap=True, horizontalalignment='center', fontsize=10, style='italic', color='white')

plt.tight_layout()
plt.show()
