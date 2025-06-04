import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import os

# Pfade
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
data_path = os.path.join(base_dir, "E01_data", "ufo_cleaned_new.csv")
output_path = os.path.join(base_dir, "F_final_project", "html_to_run", "slide1_diagram.html")

# Daten laden
df = pd.read_csv(data_path, low_memory=False)
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df = df[df['Year'].between(1990, 2024)]

# Sichtungen pro Jahr
sightings = df['Year'].value_counts().sort_index()
rolling_avg = sightings.rolling(window=5, center=True).mean()

# Farben
color_main = "#4A62D0"
color_avg = "#90FCC3"
color_anno = "#71AFB3"
color_warning = "#FFAA33"

# Plot initialisieren
fig = go.Figure()

# Hauptlinie (Sightings)
fig.add_trace(go.Scatter(
    x=sightings.index, y=sightings.values,
    mode="lines", name="Sightings (raw)",
    line=dict(color=color_main, width=3),
    opacity=1.0,
    hovertemplate="Year: %{x}<br>Sightings: %{y}<extra></extra>"
))

# Sekundärlinie (Rolling Average)
fig.add_trace(go.Scatter(
    x=rolling_avg.index, y=rolling_avg.values,
    mode="lines", name="5-Year Rolling Avg",
    line=dict(color=color_avg, width=2, dash='dash'),
    opacity=0.6,
    hoverinfo='skip'
))

# Ereignis-Annotations
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
            arrowhead=2,
            ax=-60, ay=-30,  # Pfeil kommt von unten rechts
            arrowcolor=color_anno,
            font=dict(color=color_anno, size=12),
            bgcolor="rgba(0,0,0,0.5)",
            borderpad=4
        )

# Layout
fig.update_layout(
    template="plotly_dark",
    xaxis=dict(
        title="Year",
        tickmode="linear",
        dtick=2,
        showgrid=True,
        gridcolor="rgba(255,255,255,0.05)"
    ),
    yaxis=dict(
        title="Number of Sightings",
        showgrid=True,
        gridcolor="rgba(255,255,255,0.05)"
    ),
    margin=dict(l=40, r=40, t=40, b=40),
    legend=dict(
        font=dict(color='white'),
        x=0.98, y=0.98,
        xanchor="right", yanchor="bottom",
        bgcolor="rgba(0,0,0,0)"
    )
)

# Speichern
os.makedirs(os.path.dirname(output_path), exist_ok=True)
fig.write_html(output_path)
print(f"✅ Perfektes Monatsdiagramm gespeichert: {output_path}")
