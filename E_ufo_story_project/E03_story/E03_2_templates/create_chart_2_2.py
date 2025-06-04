import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os
from matplotlib.colors import to_rgb, to_hex

# Pfade
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
data_path = os.path.join(base_dir, "E01_data", "ufo_cleaned_new.csv")
output_path = os.path.join(base_dir, "E03_story", "E03_1_charts", "slide2_2_hours.html")

# Daten einlesen
df = pd.read_csv(data_path, low_memory=False)
df['Occurred'] = pd.to_datetime(df['Occurred'], errors='coerce')
df['hour'] = df['Occurred'].dt.hour

# Gruppierung in 3h-Segmente
bins = [(0, 3), (3, 6), (6, 9), (9, 12), (12, 15), (15, 18), (18, 21), (21, 24)]
labels = ["0–3", "3–6", "6–9", "9–12", "12–15", "15–18", "18–21", "21–24"]
group_counts = [df[df['hour'].between(start, end - 1, inclusive="both")].shape[0] for start, end in bins]
total = sum(group_counts)
values = [(v / total) * 100 for v in group_counts]

# Farbverlauf
start_color = np.array(to_rgb("#4A62D0"))
end_color = np.array(to_rgb("#90FCC3"))
min_val, max_val = min(values), max(values)
colors = [to_hex((1 - (v - min_val)/(max_val - min_val)) * start_color + ((v - min_val)/(max_val - min_val)) * end_color) for v in values]

# Winkelpositionen
angles = np.linspace(0, 360, len(labels), endpoint=False)

# Interaktive Texte für Hover
hover_texts = [
    f"{count:,} sightings<br>{percent:.1f}%" 
    for count, percent in zip(group_counts, values)
]

# Plot
fig = go.Figure()

fig.add_trace(go.Barpolar(
    r=values,
    theta=angles,
    width=[360/len(labels)] * len(labels),
    marker_color=colors,
    marker_line_color="white",
    marker_line_width=0.5,
    opacity=0.95,
    hovertext=hover_texts,
    hoverinfo="text"
))

fig.update_layout(
    template="plotly_dark",
    showlegend=False,
    polar=dict(
        radialaxis=dict(visible=False),
        angularaxis=dict(
            tickmode='array',
            tickvals=angles,
            ticktext=labels,
            direction="clockwise",
            rotation=90,
            tickfont=dict(size=13, color="white"),
            showline=False,
            ticks=''
        )
    ),
    margin=dict(l=40, r=40, t=40, b=40)
)

# Speichern als HTML – Interaktiv!
os.makedirs(os.path.dirname(output_path), exist_ok=True)
fig.write_html(output_path)
print(f"✅ Interaktive HTML gespeichert: {output_path}")
