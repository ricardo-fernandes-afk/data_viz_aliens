import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os
from matplotlib.colors import to_rgb, to_hex

# Projektpfade
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
data_path = os.path.join(base_dir, "E01_data", "ufo_cleaned_new.csv")
output_path = os.path.join(base_dir, "F_final_project", "html_to_run", "slide3_1_diagram.html")

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
            text='Number<br>of Sightings',
            side='right',
            font=dict(color='white', size=12)
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
    lon=[-110, -95, -82],
    lat=[38, 38, 38],
    mode='text',
    text=[
        f"<b>West</b><br>{region_pct.get('West', '0%')}",
        f"<b>Middle</b><br>{region_pct.get('Middle', '0%')}",
        f"<b>East</b><br>{region_pct.get('East', '0%')}"
    ],
    textfont=dict(size=16, color="black"),
    showlegend=False,
    hoverinfo='skip'
)

# Layout aktualisieren
fig = go.Figure(data=[choropleth, split_lines, region_text])
fig.update_layout(
    geo=dict(
        scope='usa',
        showland=True,
        landcolor='black',
        bgcolor='rgba(0,0,0,0)',
        lakecolor='black',
        center=dict(lat=38, lon=-95),
        projection=dict(type='albers usa'),
        showcountries=False,
        showframe=False,
        showcoastlines=False
    ),
    paper_bgcolor='black',
    font_color='white',
    margin=dict(l=10, r=10, t=40, b=40),
    dragmode=False
)

# HTML speichern
os.makedirs(os.path.dirname(output_path), exist_ok=True)
fig.write_html(output_path)
print(f"✅ USA-Heatmap gespeichert: {output_path}")
