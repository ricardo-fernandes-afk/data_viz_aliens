#Where the UFOs Land: Hotspots in the U.S.
import pandas as pd
import plotly.express as px

# CSV laden
path = 'C_API/ufo_cleaned.csv'
df = pd.read_csv(path)

# Nur USA-Daten verwenden
df_usa = df[df['country'] == 'us']

# Sightings pro Bundesstaat zählen
sightings_per_state = df_usa['state'].value_counts().reset_index()
sightings_per_state.columns = ['state_code', 'sightings']

# Bundesstaaten in Großbuchstaben (Plotly braucht sie so)
sightings_per_state['state_code'] = sightings_per_state['state_code'].str.upper()

# Choropleth-Karte erzeugen
fig = px.choropleth(
    sightings_per_state,
    locations='state_code',
    locationmode='USA-states',
    color='sightings',
    color_continuous_scale='Viridis',
    scope='usa',
    labels={'sightings': 'Sightings'},
    title='UFO Sightings by US State'
)

fig.update_layout(
    title_font=dict(size=20),
    geo=dict(bgcolor='rgba(0,0,0,0)'),
    paper_bgcolor='black',
    font_color='white'
)

fig.show()
