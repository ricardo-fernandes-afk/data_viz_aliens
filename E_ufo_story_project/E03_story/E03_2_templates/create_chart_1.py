import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import os

# Projektstruktur
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
data_path = os.path.join(base_dir, "E01_data", "ufo_cleaned.csv")
output_path = os.path.join(base_dir, "E03_story", "E03_1_charts", "slide1_timeline.html")

# Daten laden
df = pd.read_csv(data_path, low_memory=False)
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
df['year'] = df['datetime'].dt.year
df = df[df['year'].between(1940, 2024)]

# Sichtungen pro Jahr
sightings = df['year'].value_counts().sort_index()
rolling_avg = sightings.rolling(window=5, center=True).mean()

# Farben definieren
color_main = "#4A62D0"     # Primär (Blau)
color_avg = "#90FCC3"      # Rolling Avg (Mintgrün)
color_anno = "#71AFB3"     # Annotation (Türkis)

# Plot
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=sightings.index, y=sightings.values,
    mode="lines", name="Sightings (raw)",
    line=dict(color=color_main, width=2), opacity=0.5
))

fig.add_trace(go.Scatter(
    x=rolling_avg.index, y=rolling_avg.values,
    mode="lines", name="5-Year Rolling Avg",
    line=dict(color=color_avg, width=3)
))

# Annotations
highlights = {
    1997: "Phoenix Lights",
    2001: "Post-9/11 spike",
    2004: "USS Nimitz",
    2020: "Pentagon video"
}

for year, label in highlights.items():
    if year in sightings.index:
        fig.add_annotation(
            x=year,
            y=sightings[year],
            text=label,
            showarrow=True,
            arrowhead=1,
            arrowcolor=color_anno,
            font=dict(color=color_anno),
            bgcolor="rgba(0,0,0,0.6)"
        )

# Layout
fig.update_layout(
    template="plotly_dark",
    title="When the Sky Went Crazy",
    xaxis_title="Year",
    yaxis_title="Number of Sightings",
    margin=dict(l=40, r=40, t=80, b=40),
    legend=dict(font=dict(color='white'))
)

# Speichern
os.makedirs(os.path.dirname(output_path), exist_ok=True)
pio.write_html(fig, file=output_path, auto_open=False)

print(f"✅ Slide 1 gespeichert mit Freaking Aliens Farben: {output_path}")
