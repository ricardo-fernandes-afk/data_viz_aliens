import pandas as pd
import numpy as np
import plotly.graph_objects as go
from matplotlib.colors import to_rgb, to_hex
import re
import os

# === Pfade definieren ===
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
data_path = os.path.join(base_dir, "E01_data", "ufo_cleaned_new.csv")
output_path = os.path.join(base_dir, "F_final_project", "html_to_run", "slide3_2_diagram.html")

# === Daten einlesen ===
df = pd.read_csv(data_path, low_memory=False)
df.columns = df.columns.str.strip().str.lower()

# === Länderkennung extrahieren ===
def extract_country(location):
    if pd.isna(location):
        return None
    match = re.search(r'\(([^)]+)\)', location)
    if match:
        return match.group(1).split('/')[0].strip().lower()
    return location.split(',')[-1].strip().lower()

df['country_guess'] = df['location'].apply(extract_country)

country_map = {
    'us': 'United States', 'usa': 'United States', 'u.s.': 'United States',
    'uk': 'United Kingdom', 'england': 'United Kingdom', 'scotland': 'United Kingdom',
    'canada': 'Canada', 'australia': 'Australia', 'germany': 'Germany',
    'mexico': 'Mexico', 'france': 'France', 'brazil': 'Brazil',
    'italy': 'Italy', 'china': 'China', 'japan': 'Japan',
    'russia': 'Russian Federation', 'south korea': 'South Korea', 'korea': 'South Korea'
}

df['country_clean'] = df['country_guess'].replace(country_map)
df = df[df['country_clean'].notna() & (df['country_clean'] != '')]

# === Sichtungen zählen ===
country_counts = df['country_clean'].value_counts()
country_counts = country_counts[country_counts > 2].reset_index()
country_counts.columns = ['country', 'sightings']

usa_val = country_counts.loc[country_counts['country'] == 'United States', 'sightings'].values[0]
total_val = country_counts['sightings'].sum()
usa_pct = usa_val / total_val * 100

usa_label = f"{usa_pct:.1f}%<br>of all sightings"

# === Farbverlauf definieren ===
start_color = np.array(to_rgb("#4A62D0"))
end_color = np.array(to_rgb("#90FCC3"))

min_c, max_c = country_counts['sightings'].min(), country_counts['sightings'].max()
norm_vals = ((country_counts['sightings'] - min_c) / (max_c - min_c)) ** 0.6

country_counts = country_counts[~norm_vals.isna()].reset_index(drop=True)
norm_vals = np.log10(country_counts['sightings'])  # absolute log-Skala
norm_vals = (norm_vals - norm_vals.min()) / (norm_vals.max() - norm_vals.min())
colors = [to_hex(nv * start_color + (1 - nv) * end_color) for nv in norm_vals]
colorscale = [[i / (len(colors) - 1), c] for i, c in enumerate(colors)]

# === Karte erstellen ===
choropleth = go.Choropleth(
    locations=country_counts['country'],
    z=country_counts['sightings'],
    locationmode="country names",
    zmin=min_c,
    zmax=max_c,
    colorscale=colorscale,
    marker_line_color='white',
    marker_line_width=0.4,
    showscale=False,
    hovertemplate='<b>%{location}</b><br><b>Sightings:</b> %{z:,}<extra></extra>'
)

# === Layout ===
fig = go.Figure(data=[choropleth])
fig.update_layout(
    geo=dict(
        scope='world',
        showland=True,
        landcolor='black',
        bgcolor='rgba(0,0,0,0)',
        showcountries=True,
        showcoastlines=False,
        showframe=False,
        countrycolor='white',
        projection=dict(type='natural earth'),
        lataxis=dict(range=[-60, 85]),
    ),
    paper_bgcolor='black',
    font_color='white',
    margin=dict(l=10, r=10, t=40, b=40),
    dragmode=False
)

fig.add_trace(go.Scattergeo(
    lon=[-100],
    lat=[40],
    mode="text",
    text=[usa_label],
    textfont=dict(size=12, color="black"),
    showlegend=False,
    hoverinfo='skip'
))


# === Exportieren ===
os.makedirs(os.path.dirname(output_path), exist_ok=True)
fig.write_html(output_path)
print(f"✅ Weltkarte gespeichert: {output_path}")
