import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import gaussian_kde
import numpy as np
import os

# Projektpfade
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
data_path = os.path.join(base_dir, "E01_data", "ufo_cleaned.csv")
output_path = os.path.join(base_dir, "E03_story", "E03_1_charts", "slide3_hotspots.html")

# Daten laden
df = pd.read_csv(data_path, low_memory=False)

# Nur USA-Daten mit Koordinaten
df_us = df[(df['country'] == 'us') & df['latitude'].notna() & df['longitude'].notna()].copy()
df_us['latitude'] = pd.to_numeric(df_us['latitude'], errors='coerce')
df_us['longitude'] = pd.to_numeric(df_us['longitude'], errors='coerce')

# Sampling zur Performance-Optimierung
df_sample = df_us.sample(n=20000, random_state=42).dropna(subset=['latitude', 'longitude'])
lat = df_sample['latitude'].values
lon = df_sample['longitude'].values

# 2D-Kernel Density Estimate berechnen
xy = np.vstack([lon, lat])
kde = gaussian_kde(xy)
densities = kde(xy)
norm_dens = (densities - densities.min()) / (densities.max() - densities.min())

# "Spooky"-Farbschema
colorscale = [
    [0.0, '#0d0221'],   # fast schwarz
    [0.1, '#22007c'],   # tief violett
    [0.4, '#38d430'],   # neongrün
    [1.0, '#ffcc00']    # gel
]

# Weltweite Sichtungen pro Land
sightings_world = df['country'].value_counts().reset_index()
sightings_world.columns = ['country_code', 'sightings']
sightings_world['log_sightings'] = np.log1p(sightings_world['sightings'])  # log(1+x)

# ScatterMap mit Dichte-Farbwerten
scatter_map = go.Scattergeo(
    lon=lon,
    lat=lat,
    mode='markers',
    marker=dict(
        size=3,
        color=norm_dens,
        colorscale=colorscale,
        opacity=0.6
    ),
    geo='geo1',
    showlegend=False
)

# Weltkarte (kleines Inset)
world_map = go.Choropleth(
    locations=sightings_world['country_code'],
    z=sightings_world['log_sightings'],
    locationmode='country names',
    colorscale=colorscale,
    zmin=0,
    zmax=sightings_world['log_sightings'].max(),
    showscale=False,
    marker_line_color='white',
    marker_line_width=0.4,
    geo='geo2'
)

# Zwei Karten (USA + Weltkontext)
fig = make_subplots(specs=[[{"type": "choropleth"}]])
fig.add_trace(scatter_map)
fig.add_trace(world_map)

fig.update_layout(
    title_text='UFO Sightings Clusters in the US with Global Context',
    geo1=dict(
        scope='usa',
        domain=dict(x=[0, 1], y=[0, 1]),
        showland=True,
        landcolor='rgb(10,10,10)',
        bgcolor='rgba(0,0,0,0)',
        projection_type='albers usa'
    ),
    geo2=dict(
        scope='world',
        domain=dict(x=[0.7, 1], y=[0, 0.3]),
        showland=True,
        landcolor='black',
        showcoastlines=False,
        showframe=False,
        showcountries=True,
        countrycolor='white',
        bgcolor='rgba(0,0,0,0)'
    ),
    paper_bgcolor='black',
    font_color='white',
)

# HTML speichern
os.makedirs(os.path.dirname(output_path), exist_ok=True)
fig.write_html(output_path)
print(f"✅ Slide 3 gespeichert: {output_path}")
