#Where the UFOs Land: Hotspots in the U.S.
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# CSV laden
path = 'C_API/ufo_cleaned.csv'
df = pd.read_csv(path)

# Nur USA-Daten verwenden
df_usa = df[df['country'] == 'us']

# Sightings pro Bundesstaat zählen
sightings_per_state = df_usa['state'].value_counts().reset_index()
sightings_per_state.columns = ['state_code', 'sightings']

# Weltweite Sichtungen pro Land
sightings_world = df['country'].value_counts().reset_index()
sightings_world.columns = ['country_code', 'sightings']

# Bundesstaaten in Großbuchstaben (Plotly braucht sie so)
sightings_per_state['state_code'] = sightings_per_state['state_code'].str.upper()

# USA-Karte erzeugen
usa_map = px.choropleth(
    sightings_per_state,
    locations='state_code',
    locationmode='USA-states',
    color='sightings',
    color_continuous_scale='Viridis',
    scope='usa',
    labels={'sightings': 'Sightings'},
    title='UFO Sightings by US State'
)

# Weltkarte (kleines Inset)
world_map = go.Choropleth(
    locations=sightings_world['country_code'],
    z=sightings_world['sightings'],
    locationmode='country names',
    colorscale='Greys',
    showscale=False,
    geo='geo2'
)

# Subplots mit zwei Geografien (USA und Weltkarte)
fig = make_subplots(specs=[[{"type": "choropleth"}]])

fig.add_trace(usa_map)
fig.add_trace(world_map)

# Layout mit zwei Karten
fig.update_layout(
    title_text='UFO Sightings in the US with Global Context',
    geo1=dict(
        scope='usa',
        domain=dict(x=[0, 1], y=[0, 1]),
        bgcolor='rgba(0,0,0,0)'
    ),
    geo2=dict(
        scope='world',
        domain=dict(x=[0.7, 1], y=[0, 0.3]),  # Position und Größe der Inset-Weltkarte
        bgcolor='rgba(0,0,0,0)'
    ),
    paper_bgcolor='black',
    font_color='white',
)

fig.show()
