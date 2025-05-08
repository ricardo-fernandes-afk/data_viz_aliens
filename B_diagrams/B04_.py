import pandas as pd
import matplotlib.pyplot as plt

# CSV-Datei laden
path = r"C:\Users\FLJ\OneDrive - Hochschule Luzern\Share_JRS\04_Frühlingssemster25\07_DataVis\04_JayRiciTill\data_viz_aliens\C_API\ufo_cleaned.csv"
df = pd.read_csv(path)

# Spalten bereinigen
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['shape'] = df['shape'].str.lower().str.strip()
df = df[df['year'].between(1940, 2024)]

# Top 4 Shapes definieren
top_shapes = df['shape'].value_counts().nlargest(4).index.tolist()

# Andere als "other" zusammenfassen
df['shape_grouped'] = df['shape'].apply(lambda x: x if x in top_shapes else 'other')

# Gruppieren: Jahr × Shape
shape_counts = df.groupby(['year', 'shape_grouped']).size().unstack(fill_value=0)

# Rolling Average anwenden (5 Jahre)
shape_counts_smooth = shape_counts.rolling(window=5, center=True).mean()

# Farben definieren
colors = {
    'light': '#FFE600',
    'circle': '#00D1FF',
    'triangle': '#FF5733',
    'fireball': '#C70039',
    'other': '#999999'
}

# Plot erstellen
plt.style.use('default')
fig, ax = plt.subplots(figsize=(14, 7))

for shape in top_shapes + ['other']:
    ax.plot(shape_counts_smooth.index,
            shape_counts_smooth[shape],
            label=shape.capitalize(),
            color=colors.get(shape, '#cccccc'),
            linewidth=2)

# Titel & Achsen
ax.set_title("How UFO Shapes Changed Over Time", fontsize=16, fontweight='bold')
ax.set_xlabel("Year")
ax.set_ylabel("Number of Sightings (5-year avg.)")
ax.legend(title="Shape", loc='upper left')
ax.grid(True, linestyle='--', alpha=0.4)

plt.tight_layout()
plt.show()
