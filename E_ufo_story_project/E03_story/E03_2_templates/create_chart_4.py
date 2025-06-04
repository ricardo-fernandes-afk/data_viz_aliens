import pandas as pd
import plotly.graph_objects as go
import os

# Pfade
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
data_path = os.path.join(base_dir, "E01_data", "ufo_cleaned_new.csv")
output_path = os.path.join(base_dir, "E04_final_project", "slide4_diagram.html")

# Daten laden & vorbereiten
df = pd.read_csv(data_path, low_memory=False)
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
df['year'] = df['datetime'].dt.year
df['shape'] = df['shape'].str.lower().str.strip()
df = df[df['year'].between(1940, 2024)]

# Gruppieren: Sightings pro Jahr und Shape
shape_years = df.groupby(['year', 'shape']).size().unstack(fill_value=0)

# Glätten
shape_smooth = shape_years.rolling(window=5, center=True).mean().dropna()

# Shapes sortieren nach Gesamtsumme
total_counts = shape_smooth.sum().sort_values(ascending=False)
sorted_shapes = total_counts.index.tolist()

# Farbenverlauf definieren: von #90FCC3 (hell) zu #4A62D0 (dunkel)
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt

cmap = LinearSegmentedColormap.from_list("custom_gradient", ["#90FCC3", "#4A62D0"])
color_range = [cmap(i / (len(sorted_shapes) - 1)) for i in range(len(sorted_shapes))]
color_hex = [f'rgb({int(r*255)}, {int(g*255)}, {int(b*255)})' for r, g, b, _ in color_range]

# Plot: Streamgraph-Stil mit stackgroup
fig = go.Figure()
for i, shape in enumerate(sorted_shapes):
    fig.add_trace(go.Scatter(
        x=shape_smooth.index,
        y=shape_smooth[shape],
        mode='lines',
        name=shape.capitalize(),
        line=dict(width=0.5, color=color_hex[i]),
        stackgroup='one',  # Streamgraph-Effekt
        hoverinfo='x+y+name'
    ))

# Layout
fig.update_layout(
    template="plotly_dark",
    title="The Changing Face of UFOs",
    xaxis=dict(title="Year"),
    yaxis=dict(title="", showgrid=False),  # Y-Achse leer, aber nicht entfernt
    legend=dict(font=dict(color='white')),
    margin=dict(l=40, r=40, t=80, b=40),
    showlegend=True
)

# Speichern
os.makedirs(os.path.dirname(output_path), exist_ok=True)
fig.write_html(output_path)
print(f"✅ Slide 4 gespeichert: {output_path}")