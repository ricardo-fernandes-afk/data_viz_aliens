import pandas as pd
import plotly.graph_objects as go
import os
import numpy as np

# Pfade
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
data_path = os.path.join(base_dir, "E01_data", "ufo_cleaned.csv")
output_path = os.path.join(base_dir, "E03_story", "E03_1_charts", "slide2_polar_months.html")

# Daten einlesen
df = pd.read_csv(data_path, low_memory=False)
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
df['month'] = df['datetime'].dt.month

# Sichtungen pro Monat berechnen
month_counts = df['month'].value_counts().sort_index()
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
values = [month_counts.get(i, 0) for i in range(1, 13)]

# Polar-Achsenwinkel definieren
angles = np.linspace(0, 360, 12, endpoint=False)

# Plotly Polar Bar Chart
fig = go.Figure()

fig.add_trace(go.Barpolar(
    r=values,
    theta=angles,
    width=[30]*12,
    marker_color=['#4A62D0' if i not in [5, 6, 7] else '#90FCC3' for i in range(12)],
    marker_line_color="white",
    marker_line_width=1,
    opacity=0.9
))

# Layout
fig.update_layout(
    template="plotly_dark",
    title="Aliens Love Summer Nights",
    polar=dict(
        radialaxis=dict(visible=True, tickfont=dict(color="white")),
        angularaxis=dict(
            tickmode='array',
            tickvals=angles,
            ticktext=month_names,
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
print(f"✅ Slide 2 (Polar) gespeichert: {output_path}")
