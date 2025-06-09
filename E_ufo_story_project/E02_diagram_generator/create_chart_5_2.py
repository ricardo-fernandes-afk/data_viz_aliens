import pandas as pd
import plotly.graph_objects as go
import os
import re
import numpy as np

# Funktion zur Konvertierung von Dauer zu Sekunden
def duration_to_seconds(duration_str):
    if not isinstance(duration_str, str) or duration_str.strip() == "" or "unknown" in duration_str:
        return np.nan
    duration_str = duration_str.lower().strip()
    replacements = {
        "one": "1",
        "few seconds": "5 sec",
        "several hours": "10800 sec",
        ">1 minute": "90 sec"
    }
    for k, v in replacements.items():
        duration_str = duration_str.replace(k, v)
    range_match = re.match(r'(\d+\.?\d*)\s*-\s*(\d+\.?\d*)', duration_str)
    if range_match:
        avg = (float(range_match.group(1)) + float(range_match.group(2))) / 2
        duration_str = str(avg)
    seconds = 0
    hr_match = re.search(r'(\d+\.?\d*)\s*(h|hr|hour)', duration_str)
    min_match = re.search(r'(\d+\.?\d*)\s*(m|min|minute)', duration_str)
    sec_match = re.search(r'(\d+\.?\d*)\s*(s|sec|second)', duration_str)
    if hr_match: seconds += float(hr_match.group(1)) * 3600
    if min_match: seconds += float(min_match.group(1)) * 60
    if sec_match: seconds += float(sec_match.group(1))
    if seconds == 0:
        number = re.match(r'^\d+\.?\d*$', duration_str)
        if number:
            return float(number.group(0))
    return seconds if seconds > 0 else np.nan

# Pfade
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
data_path = os.path.join(base_dir, "E01_data", "ufo_cleaned_new.csv")
output_path = os.path.join("F_final_project", "html_to_run", "slide5_2_diagram.html")

# Daten laden und vorbereiten
df = pd.read_csv(data_path, low_memory=False)
df.columns = df.columns.str.strip()
df["Shape"] = df["Shape"].astype(str).str.lower().str.strip()
df["Duration_cleaned"] = df["Duration"].astype(str).str.strip().str.lower()
df["duration_seconds"] = df["Duration_cleaned"].apply(duration_to_seconds)
df = df[(df["duration_seconds"] > 0) & (df["duration_seconds"] < 100000)]

# Dauerklassen definieren
bins = [0, 10, 60, 300, 1800, 3600, 100000]
labels = ['<10s', '10–60s', '1–5min', '5–30min', '30–60min', '>1h']
colors = ['#4A62D0', '#71AFB3', '#90FCC3', '#FFE600', '#FF5733', '#C70039']
df["duration_class"] = pd.cut(df["duration_seconds"], bins=bins, labels=labels)

# Top 19 Shapes
shape_counts = df["Shape"].value_counts()
# Alle "other" und "others" vereinheitlichen
df["Shape"] = df["Shape"].replace({"others": "other"})

# Neue Top 20 nach Bereinigung
shape_counts = df["Shape"].value_counts()
top_shapes = shape_counts.head(20).index.tolist()
df["Shape_grouped"] = df["Shape"].apply(lambda x: x if x in top_shapes else "other")

# Prozentuale Verteilung pro Shape
pivot = pd.crosstab(df["Shape_grouped"], df["duration_class"])
pivot = pivot.div(pivot.sum(axis=1), axis=0).fillna(0)
pivot = pivot.sort_index(ascending=False)

# Prozentwerte für Labels
percent_labels = pivot.applymap(lambda v: f"{v:.0%}" if v > 0.01 else "")

# Balkendiagramm erzeugen
fig = go.Figure()
for i, duration in enumerate(labels):
    fig.add_trace(go.Bar(
        y=pivot.index,
        x=pivot[duration],
        name=duration,
        orientation='h',
        marker=dict(color=colors[i]),
        hoverinfo="skip",
        text=percent_labels[duration],
        textposition='inside',
        textfont=dict(size=12, color="black", family="Arial", weight="bold"),
        insidetextanchor='middle',
    ))

fig.update_layout(
    barmode='stack',
    template='plotly_dark',
    height=900,
    width=1000,
    margin=dict(l=10, r=10, t=40, b=40),
    showlegend=True,
    bargap=0.5,
    xaxis=dict(
        tickvals=[0.0, 1.0],
        ticktext=["0%", "100%"],
        showgrid=False,
        title=None
    ),
    yaxis=dict(
        title=None,
        tickfont=dict(size=12, color="white"),
        showgrid=False,
        automargin=True,
    )
)

# Speichern
os.makedirs(os.path.dirname(output_path), exist_ok=True)
fig.write_html(output_path)
print(f"✅ Slide 5.2 gespeichert: {output_path}")
