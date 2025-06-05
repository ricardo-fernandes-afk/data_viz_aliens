import pandas as pd
import plotly.express as px
import os

# Pfade festlegen
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
data_path = os.path.join(base_dir, "E01_data", "ufo_cleaned.csv")
output_path = os.path.join("F_final_project", "html_to_run", "slide5_2_diagram.html")

# Daten einlesen
df = pd.read_csv(data_path, low_memory=False)
df['duration_seconds'] = pd.to_numeric(df['duration_seconds'], errors='coerce')
df['shape'] = df['shape'].str.lower().str.strip()
df = df[(df['duration_seconds'] > 0) & (df['duration_seconds'] < 30000)]

# Dauerklassen definieren
bins = [0, 10, 60, 300, 1800, 3600, 30000]
labels = ['<10s', '10–60s', '1–5min', '5–30min', '30–60min', '>1h']
df['duration_class'] = pd.cut(df['duration_seconds'], bins=bins, labels=labels)

# Top 6 Shapes wählen
top_shapes = df['shape'].value_counts().nlargest(6).index.tolist()
df = df[df['shape'].isin(top_shapes)]

# Gruppieren: Shape × Dauerklasse
heatmap_data = df.groupby(['shape', 'duration_class']).size().reset_index(name='count')

# Heatmap plotten
fig = px.density_heatmap(
    heatmap_data,
    x="duration_class",
    y="shape",
    z="count",
    color_continuous_scale="Viridis",
    title="Which Shapes Last How Long?",
    labels={"duration_class": "Duration", "shape": "UFO Shape", "count": "Sightings"}
)

fig.update_layout(
    template="plotly_dark",
    margin=dict(l=40, r=40, t=80, b=40)
)

# Speichern
os.makedirs(os.path.dirname(output_path), exist_ok=True)
fig.write_html(output_path)
print(f"✅ Slide 5.2 gespeichert: {output_path}")
