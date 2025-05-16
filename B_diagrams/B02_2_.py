import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# CSV-Datei laden
path = 'C_API/ufo_cleaned.csv'
df = pd.read_csv(path)

# Sichtungen pro Stunde zählen
sightings_per_hour = df['hour'].value_counts().sort_index()
hours = np.arange(24)
values = sightings_per_hour.reindex(hours, fill_value=0).values

# Winkel berechnen
angles = np.deg2rad(np.linspace(0, 360, 24, endpoint=False))

# Farben je nach Häufigkeit (normalisiert)
norm_values = (values - values.min()) / (values.max() - values.min())
colors = plt.cm.plasma(norm_values)  # Farbverlauf: Plasma

# Plot im Darkmode
plt.style.use('dark_background')
fig = plt.figure(figsize=(8, 8))
ax = plt.subplot(111, polar=True)
bars = ax.bar(angles, values, width=2*np.pi/24, bottom=0, color=colors, edgecolor='white')

# Kreisachse & Richtung
ax.set_theta_zero_location('N')  # Mitternacht oben
ax.set_theta_direction(-1)       # Uhrzeiger

# Achsenbeschriftung (Stunden)
ax.set_xticks(angles)
ax.set_xticklabels(hours, color='white', fontsize=10)

# Titel und Storytext
ax.set_title("Aliens Love the Night", fontsize=16, fontweight='bold', color='white', pad=20)
plt.figtext(0.5, 0.05,
            "Most sightings occur between 8pm and 2am – the alien rush hour?",
            wrap=True, horizontalalignment='center', fontsize=10, style='italic', color='white')

plt.tight_layout()
plt.show()
