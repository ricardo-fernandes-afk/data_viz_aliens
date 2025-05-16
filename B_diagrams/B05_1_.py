import pandas as pd
import matplotlib.pyplot as plt

# Datei laden
path = 'C_API/ufo_cleaned.csv'
df = pd.read_csv(path)

# Dauer in Sekunden bereinigen
df['duration_seconds'] = pd.to_numeric(df['duration_seconds'], errors='coerce')
df = df[(df['duration_seconds'] > 0) & (df['duration_seconds'] < 100000)]

# Dauerklassen definieren
bins = [0, 10, 60, 300, 1800, 3600, 100000]
labels = ['<10s', '10–60s', '1–5min', '5–30min', '30–60min', '>1h']
df['duration_class'] = pd.cut(df['duration_seconds'], bins=bins, labels=labels)

# Gruppieren
duration_counts = df['duration_class'].value_counts().sort_index()

# Farben (Darkmode Style)
colors = ['#39FF14', '#00D1FF', '#FFC300', '#FF5733', '#C70039', '#900C3F']

# Plot
plt.style.use('dark_background')
plt.figure(figsize=(10, 6))
plt.bar(duration_counts.index, duration_counts.values, color=colors, edgecolor='white')

plt.title("How Long Do UFO Sightings Last? (Grouped)", fontsize=16, fontweight='bold', pad=20)
plt.xlabel("Duration Group")
plt.ylabel("Number of Sightings")
plt.grid(axis='y', linestyle='--', alpha=0.4)

# Zusatztext
plt.figtext(0.5, -0.05,
            "Over half of all sightings last under 5 minutes – most are short, intense flashes of mystery.",
            wrap=True, horizontalalignment='center', fontsize=10, style='italic', color='white')

plt.tight_layout()
plt.show()
