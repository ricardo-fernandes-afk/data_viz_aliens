import pandas as pd
import plotly.graph_objects as go
import os

# Pfade
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
data_path = os.path.join(base_dir, "E01_data", "ufo_cleaned.csv")
output_path = os.path.join(base_dir, "E03_story", "E03_1_charts", "slide4_shapes.html")

# Daten laden & vorbereiten
df = pd.read_csv(data_path, low_memory=False)
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
df['year'] = df['datetime'].dt.year
df['shape'] = df['shape'].str.lower().str.strip()
df = df[df['year'].between(1940, 2024)]

# Top 4 Shapes
top_shapes = df['shape'].value_counts().nlargest(4).index.tolist()
df = df[df['shape'].isin(top_shapes)]

# Gruppieren
shape_years = df.groupby(['year', 'shape']).size().unstack(fill_value=0)
shape_smooth = shape_years.rolling(window=5, center=True).mean()

# Farben
colors = {
    'light': '#4A62D0',
    'triangle': '#90FCC3',
    'fireball': '#71AFB3',
    'circle': '#FFFFFF'
}

# Plot
fig = go.Figure()
for shape in top_shapes:
    fig.add_trace(go.Scatter(
        x=shape_smooth.index,
        y=shape_smooth[shape],
        mode='lines',
        name=shape.capitalize(),
        line=dict(width=3, color=colors.get(shape, 'gray'))
    ))

fig.update_layout(
    template="plotly_dark",
    title="Triangles, Fireballs and Lights: UFO Shapes Over Time",
    xaxis_title="Year",
    yaxis_title="Sightings (5-year avg.)",
    legend=dict(font=dict(color='white')),
    margin=dict(l=40, r=40, t=80, b=40)
)

# Speichern
os.makedirs(os.path.dirname(output_path), exist_ok=True)
fig.write_html(output_path)
print(f"✅ Slide 4 gespeichert: {output_path}")
