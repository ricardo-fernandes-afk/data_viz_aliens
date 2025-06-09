import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os
from matplotlib.colors import to_rgb, to_hex

# Projektpfade
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
data_path = os.path.join("E_ufo_story_project", "E01_data", "ufo_cleaned_new.csv")
output_path = os.path.join("F_final_project", "html_to_run", "slide3_1_diagram.html")

# Daten einlesen
df = pd.read_csv(data_path, low_memory=False)
df.columns = df.columns.str.strip().str.lower()

# State-Kürzel extrahieren (robust)
df['state'] = df['location'].str.extract(r',\s*([A-Z]{2})\s*(?:,|\s)?\s*USA', expand=False)

# Nur gültige US-States
valid_states = [
    'AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA',
    'KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ',
    'NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT',
    'VA','WA','WV','WI','WY','DC'
]
df = df[df['state'].isin(valid_states)]

# Sichtungen pro Bundesstaat (linear)
state_counts = df['state'].value_counts().reset_index()
state_counts.columns = ['state', 'sightings']

# Farbverlauf definieren
start_color = np.array(to_rgb("#4A62D0"))
end_color = np.array(to_rgb("#90FCC3"))
min_val, max_val = state_counts['sightings'].min(), state_counts['sightings'].max()
norm_vals = ((state_counts['sightings'] - min_val) / (max_val - min_val)) ** 0.6
colors = [to_hex(nv * start_color + (1 - nv) * end_color) for nv in norm_vals]
state_counts['color'] = colors

# Regionenzuordnung
west = ['WA', 'OR', 'CA', 'NV', 'AZ', 'UT', 'ID', 'MT', 'WY', 'CO', 'NM', 'AK', 'HI']
east = ['ME', 'NH', 'VT', 'MA', 'RI', 'CT', 'NY', 'NJ', 'PA', 'DE', 'MD', 'VA', 'NC', 'SC', 'GA', 'FL', 'WV']
# Middle = Rest
state_counts['region'] = state_counts['state'].apply(
    lambda x: 'West' if x in west else ('East' if x in east else 'Middle')
)

# Prozentuale Verteilung
region_totals = state_counts.groupby('region')['sightings'].sum()
total = region_totals.sum()
region_pct = (region_totals / total * 100).round(1).astype(str) + '%'

# Choropleth-Karte
choropleth = go.Choropleth(
    locations=state_counts['state'],
    z=state_counts['sightings'],
    locationmode="USA-states",
    colorscale=[[i / (len(colors) - 1), c] for i, c in enumerate(colors)],
    marker_line_color='white',
    marker_line_width=0.5,
    showscale=True,
    colorbar=dict(
        title=dict(
            text='Number of Sightings',
            side='right',
            font=dict(color='white', size=8)
        ),
        tickfont=dict(color='white', size=10),
        len=0.9,             # fast gesamte Höhe
        thickness=10,
        x=0.05,              # ganz links
        y=0.5,               # mittig vertikal
        yanchor='middle',    # von der Mitte aus ausrichten
        bgcolor='rgba(0,0,0,0)'
    ),
    hovertemplate='<b>%{location}</b><br><b>Sightings:</b> %{z:,}<extra></extra>'
)

# Trennlinien grob über -100° und -85° Länge
split_lines = go.Scattergeo(
    lon=[-103, -103, None, -88, -88],
    lat=[24, 50, None, 24, 50],
    mode='lines',
    line=dict(color='white', width=1, dash='dot'),
    showlegend=False,
    hoverinfo='skip'
)


# Text Overlays mit Region & Prozent
region_text = go.Scattergeo(
    lon=[-110, -95, -80],
    lat=[51, 51, 47],
    mode='text',
    text=[
        f"<b></b><br>{region_pct.get('West', '0%')}",
        f"<b></b><br>{region_pct.get('Middle', '0%')}",
        f"<b></b><br>{region_pct.get('East', '0%')}"
    ],
    textfont=dict(size=10, color="white"),
    showlegend=False,
    hoverinfo='skip'
)

# Layout aktualisieren
fig = go.Figure(data=[choropleth, split_lines, region_text])

# Bundesstaaten-Beschriftung – Koordinaten-Mitte
state_coords = {
    'AL': (-86.8, 32.8), 'AK': (-152.4, 61.4), 'AZ': (-111.5, 34.0), 'AR': (-92.4, 34.8),
    'CA': (-119.4, 36.8), 'CO': (-105.5, 39.1), 'CT': (-72.7, 41.6), 'DE': (-75.5, 38.6),
    'FL': (-81.5, 27.8), 'GA': (-83.6, 32.6), 'HI': (-155.5, 20.5), 'ID': (-114.2, 44.1),
    'IL': (-89.2, 40.0), 'IN': (-86.1, 40.2), 'IA': (-93.2, 42.0), 'KS': (-98.0, 38.5),
    'KY': (-84.8, 37.5), 'LA': (-91.9, 30.9), 'ME': (-69.4, 45.2), 'MD': (-76.6, 39.0),
    'MA': (-71.8, 42.3), 'MI': (-85.6, 44.2), 'MN': (-94.6, 46.5), 'MS': (-89.7, 32.7),
    'MO': (-92.6, 38.3), 'MT': (-110.4, 46.9), 'NE': (-99.9, 41.5), 'NV': (-116.9, 38.8),
    'NH': (-71.6, 43.2), 'NJ': (-74.4, 40.2), 'NM': (-106.1, 34.5), 'NY': (-75.5, 42.9),
    'NC': (-79.0, 35.5), 'ND': (-100.0, 47.5), 'OH': (-82.9, 40.4), 'OK': (-97.5, 35.5),
    'OR': (-120.5, 44.1), 'PA': (-77.2, 41.2), 'RI': (-71.4, 41.6), 'SC': (-81.2, 33.8),
    'SD': (-99.9, 44.4), 'TN': (-86.4, 35.7), 'TX': (-99.9, 31.0), 'UT': (-111.6, 39.3),
    'VT': (-72.7, 44.0), 'VA': (-78.7, 37.4), 'WA': (-120.7, 47.5), 'WV': (-80.5, 38.6),
    'WI': (-89.5, 44.5), 'WY': (-107.5, 43.0), 'DC': (-77.0, 38.9)
}

# Staaten, die nicht beschriftet werden sollen (zu klein/zu eng)
exclude = {'DC', 'RI', 'CT', 'DE', 'NJ', 'MD', 'MA', 'VT', 'NH'}

# Nur die übrigen Staaten
visible_states = [s for s in state_counts['state'] if s in state_coords and s not in exclude]

fig.add_trace(go.Scattergeo(
    lon=[state_coords[s][0] for s in visible_states],
    lat=[state_coords[s][1] for s in visible_states],
    text=visible_states,
    mode="text",
    textfont=dict(size=8, color="black"),
    showlegend=False,
    hoverinfo='skip',
    geo='geo'
))

fig.update_layout(
    geo=dict(
        scope='usa',
        showland=True,
        landcolor='black',
        bgcolor='rgba(0,0,0,0)',
        lakecolor='black',
        center=dict(lat=38, lon=-100),
        projection=dict(type='albers usa'),
        showcountries=False,
        showframe=False,
        showcoastlines=False,
    ),
    template="plotly_dark",
    font_color='white',
    margin=dict(l=10, r=10, t=40, b=10),
    dragmode=False,
)

# HTML speichern
os.makedirs(os.path.dirname(output_path), exist_ok=True)
fig.write_html(output_path)
print(f"✅ USA-Heatmap gespeichert: {output_path}")
