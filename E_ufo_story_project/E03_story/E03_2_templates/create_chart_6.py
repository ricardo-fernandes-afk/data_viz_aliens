# create_chart_6.py
import pandas as pd
import plotly.graph_objects as go
import os
from datetime import datetime

# Basisverzeichnis
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
data_path = os.path.join(base_dir, "E01_data", "ufo_cleaned.csv")
output_path = os.path.join(base_dir, "E03_story", "E03_1_charts", "slide6_diagramm.html")

# Daten laden und vorbereiten
df = pd.read_csv(data_path, low_memory=False)
df['date'] = pd.to_datetime(df['datetime'], errors='coerce')
df = df.dropna(subset=['date'])
df['day_of_year'] = df['date'].dt.dayofyear

# Sichtungen nach Kalendertag aggregieren
sightings_by_day = df['day_of_year'].value_counts().sort_index()

# Feiertage (als day-of-year)
feiertage = {
    "New Year's Day":  datetime(2023, 1, 1).timetuple().tm_yday,
    "April Fools":     datetime(2023, 4, 1).timetuple().tm_yday,
    "Independence Day": datetime(2023, 7, 4).timetuple().tm_yday,
    "Halloween":       datetime(2023, 10, 31).timetuple().tm_yday,
    "Christmas":       datetime(2023, 12, 25).timetuple().tm_yday,
    "New Year's Eve":  datetime(2023, 12, 31).timetuple().tm_yday,
}

# Linie zeichnen
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=sightings_by_day.index,
    y=sightings_by_day.values,
    mode='lines',
    name='Sightings per Day',
    line=dict(color='#71AFB3', width=2)
))

# Feiertage markieren
for name, day in feiertage.items():
    if day in sightings_by_day.index:
        fig.add_trace(go.Scatter(
            x=[day],
            y=[sightings_by_day[day]],
            mode='markers+text',
            name=name,
            text=[name],
            textposition="top center",
            marker=dict(size=10, color='#FFE600', symbol='star')
        ))

# Layout
fig.update_layout(
    template="plotly_dark",
    title="Do UFO Sightings Spike on Holidays?",
    xaxis_title="Day of Year",
    yaxis_title="Number of Sightings",
    font_color="#CCFFE3",
    plot_bgcolor="#0D0D0D",
    paper_bgcolor="#0D0D0D",
    margin=dict(t=80, b=50, l=50, r=50)
)

# Ordner anlegen und speichern
os.makedirs(os.path.dirname(output_path), exist_ok=True)
fig.write_html(output_path, include_plotlyjs='cdn')

print(f"✅ Feiertags-Liniendiagramm gespeichert unter: {output_path}")
