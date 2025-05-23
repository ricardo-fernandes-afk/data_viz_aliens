import pandas as pd
import plotly.express as px
import os

# Projektpfade
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
data_path = os.path.join(base_dir, "E01_data", "ufo_cleaned.csv")
output_path = os.path.join(base_dir, "E03_story", "E03_1_charts", "slide3_hotspots.html")

# Daten laden
df = pd.read_csv(data_path, low_memory=False)

# Nur USA-Daten
df = df[df['country'] == 'us']
df['state'] = df['state'].str.upper()

# Gruppieren
state_counts = df['state'].value_counts().reset_index()
state_counts.columns = ['state_code', 'sightings']

# Plotly Choropleth Map
fig = px.choropleth(
    state_counts,
    locations='state_code',
    locationmode="USA-states",
    color='sightings',
    color_continuous_scale='Viridis',
    scope="usa",
    title="UFO Sightings by US State"
)

# Layout
fig.update_layout(
    template="plotly_dark",
    margin=dict(l=40, r=40, t=80, b=40)
)

# Speichern
os.makedirs(os.path.dirname(output_path), exist_ok=True)
fig.write_html(output_path)
print(f"✅ Slide 3 gespeichert: {output_path}")
