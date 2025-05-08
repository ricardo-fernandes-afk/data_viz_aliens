import pandas as pd
import matplotlib.pyplot as plt

# CSV laden
path = r"C:\Users\FLJ\OneDrive - Hochschule Luzern\Share_JRS\04_Frühlingssemster25\07_DataVis\04_JayRiciTill\data_viz_aliens\C_API\ufo_cleaned.csv"
df = pd.read_csv(path)

# Bereinigen
df['duration_seconds'] = pd.to_numeric(df['duration_seconds'], errors='coerce')
df['shape'] = df['shape'].str.lower().str.strip()
df = df[(df['duration_seconds'] > 0) & (df['duration_seconds'] < 100000)]

# Top 5 echte Shapes (ohne "other")
top_shapes = df['shape'].value_counts().drop('other', errors='ignore').nlargest(5).index.tolist()
df_top = df[df['shape'].isin(top_shapes)]

# Median pro Shape berechnen & sortieren
median_duration = df_top.groupby('shape')['duration_seconds'].median().sort_values()

# Farben manuell zuweisen
colors = {
    'triangle': '#FF5733',
    'circle': '#00D1FF',
    'light': '#FFE600',
    'fireball': '#C70039',
    'sphere': '#9D00FF'
}
color_list = [colors.get(shape, '#888888') for shape in median_duration.index]

# Plot
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(median_duration.index, median_duration.values, color=color_list, edgecolor='white')

# Y-Achse log
ax.set_yscale('log')
ax.set_title("Which UFO Shapes Stay the Longest (Median)", fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel("UFO Shape")
ax.set_ylabel("Median Duration (seconds, log scale)")
ax.grid(True, which='both', linestyle='--', alpha=0.3)

# Werte auf die Balken schreiben
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height * 1.1,
            f"{int(height):,}s", ha='center', va='bottom', fontsize=10, color='white')

# Kommentar unten
plt.figtext(0.5, -0.05,
            "Triangles and spheres tend to stay the longest – lights are blink-and-gone.",
            wrap=True, horizontalalignment='center', fontsize=10, style='italic', color='white')

plt.tight_layout()
plt.show()
