import pandas as pd
import plotly.graph_objects as go
import os

# Pfade festlegen
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
data_path = os.path.join(base_dir, "E01_data", "ufo_cleaned.csv")
output_path = os.path.join(base_dir, "E03_story", "E03_1_charts", "slide5_1_donut_duration.html")

# Daten laden
df = pd.read_csv(data_path, low_memory=False)
df['duration_seconds'] = pd.to_numeric(df['duration_seconds'], errors='coerce')
df = df[(df['duration_seconds'] > 0) & (df['duration_seconds'] < 100000)]

# Dauer in Gruppen einteilen
bins = [0, 10, 60, 300, 1800, 3600, 100000]
labels = ['<10s', '10–60s', '1–5min', '5–30min', '30–60min', '>1h']
df['duration_class'] = pd.cut(df['duration_seconds'], bins=bins, labels=labels)
counts = df['duration_class'].value_counts().sort_index()

# Donut-Diagramm erzeugen
fig = go.Figure(data=[go.Pie(
    labels=counts.index,
    values=counts.values,
    hole=0.5,
    marker_colors=['#4A62D0', '#71AFB3', '#90FCC3', '#FFE600', '#FF5733', '#C70039']
)])

fig.update_layout(
    title_text="How Long Do UFO Sightings Last?",
    template="plotly_dark",
    margin=dict(l=40, r=40, t=80, b=40)
)

# Speichern
os.makedirs(os.path.dirname(output_path), exist_ok=True)
fig.write_html(output_path)
print(f"✅ Slide 5.1 gespeichert: {output_path}")
