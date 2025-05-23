import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os

# Pfade setzen
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
data_path = os.path.join(base_dir, "E01_data", "ufo_cleaned.csv")
output_path = os.path.join(base_dir, "E03_story", "E03_1_charts", "slide2_2_polar_hours.html")

# Daten einlesen
df = pd.read_csv(data_path, low_memory=False)
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
df['hour'] = df['datetime'].dt.hour

# Stunden zählen (0–23)
hour_counts = df['hour'].value_counts().sort_index()
hours = list(range(24))
values = [hour_counts.get(h, 0) for h in hours]

# Winkel berechnen (Stunde → Grad)
angles = np.linspace(0, 360, 24, endpoint=False)
labels = [f"{h}:00" for h in hours]

# Farbverlauf (nachts = mint, tags = blau)
colors = ['#4A62D0'] * 24
for i in list(range(20, 24)) + list(range(0, 3)):
    colors[i] = '#90FCC3'  # Mintgrün für Nacht

# Plotly Polar Chart
fig = go.Figure()

fig.add_trace(go.Barpolar(
    r=values,
    theta=angles,
    width=[15]*24,
    marker_color=colors,
    marker_line_color="white",
    marker_line_width=1,
    opacity=0.95
))

fig.update_layout(
    template="plotly_dark",
    title="Aliens Love the Night",
    polar=dict(
        radialaxis=dict(visible=True, tickfont=dict(color="white")),
        angularaxis=dict(
            tickmode='array',
            tickvals=angles,
            ticktext=labels,
            direction="clockwise",
            rotation=90,
            tickfont=dict(color='white')
        )
    ),
    margin=dict(l=40, r=40, t=80, b=40)
)

# Speichern
os.makedirs(os.path.dirname(output_path), exist_ok=True)
fig.write_html(output_path)
print(f"✅ Slide 2.2 (Polar Uhrzeit) gespeichert: {output_path}")
