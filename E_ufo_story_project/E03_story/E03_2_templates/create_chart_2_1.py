import pandas as pd
import plotly.graph_objects as go
import os
import plotly.express as px
from matplotlib.colors import to_rgb, to_hex
import numpy as np

# Pfade
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
data_path = os.path.join(base_dir, "E01_data", "ufo_cleaned.csv")
output_path = os.path.join(base_dir, "E03_story", "E03_1_charts", "slide2_months.html")

# Daten einlesen
df = pd.read_csv(data_path, low_memory=False)
df['Occurred'] = pd.to_datetime(df['Occurred'], errors='coerce')
df['month'] = df['Occurred'].dt.month

# Monatszählung
month_counts = df['month'].value_counts().sort_index()
month_names = ['January ', 'February ', 'March ', 'April ', 'May ', 'June ',
               'July ', 'August ', 'September ', 'October ', 'November ', 'December ']
values = [month_counts.get(i, 0) for i in range(1, 13)]
total = sum(values)
percentages = [(v / total) * 100 for v in values]

# Reihenfolge umkehren (Januar oben)
month_names = month_names[::-1]
values = values[::-1]
percentages = percentages[::-1]

# Farben interpolieren
start_color = np.array(to_rgb("#4A62D0"))  # dunkelblau
end_color   = np.array(to_rgb("#90FCC3"))  # mint
min_val, max_val = min(values), max(values)
norm_values = [(v - min_val) / (max_val - min_val) for v in values]
colors = [to_hex((1 - nv) * start_color + nv * end_color) for nv in norm_values]

# Diagramm
fig = go.Figure()

fig.add_trace(go.Bar(
    y=month_names,
    x=percentages,
    orientation='h',
    marker=dict(
        color=colors,
        line=dict(width=0)
    ),
    name="",
    hovertemplate='%{customdata} sightings',
    customdata=values,
    opacity=0.95
))

# Layout
fig.update_layout(
    template="plotly_dark",
    title=None,
    xaxis=dict(
        title="Percentage of Sightings",
        ticksuffix="%",
        showgrid=True,
        gridcolor="rgba(255,255,255,0.05)",
        automargin=True
    ),
    yaxis=dict(
        title=None,
        automargin=True,
        ticklabelposition="outside",
        tickfont=dict(size=13),
    ),
    margin=dict(l=40, r=40, t=20, b=40),
    bargap=0.6
)

# Speichern
os.makedirs(os.path.dirname(output_path), exist_ok=True)
fig.write_html(output_path)
print(f"✅ Perfektes Monatsdiagramm gespeichert: {output_path}")
