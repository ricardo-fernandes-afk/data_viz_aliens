import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
from matplotlib.colors import to_rgb, to_hex

# Pfade festlegen
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
data_path = os.path.join(base_dir, "E01_data", "ufo_cleaned_new.csv")
html_output = os.path.join("F_final_project", "html_to_run", "slide6_diagram.html")

# Daten laden
df = pd.read_csv(data_path, low_memory=False)
df.columns = df.columns.str.strip().str.lower()
df['occurred'] = pd.to_datetime(df['occurred'], errors='coerce')
df = df.dropna(subset=['occurred'])

# Gruppieren nach Kalendertag
df['month'] = df['occurred'].dt.month
df['day'] = df['occurred'].dt.day
grouped = df.groupby(['month', 'day']).size().reset_index(name='sightings')

# Vollständige Tagesstruktur
all_days = pd.MultiIndex.from_product(
    [range(1, 13), range(1, 32)],
    names=['month', 'day']
)
calendar_df = grouped.set_index(['month', 'day']).reindex(all_days).reset_index()
calendar_df['sightings'] = calendar_df['sightings'].fillna(0)

# Ungültige Tage entfernen
calendar_df = calendar_df[
    ~((calendar_df['month'] == 2) & (calendar_df['day'] > 29)) &
    ~((calendar_df['month'].isin([4, 6, 9, 11])) & (calendar_df['day'] > 30))
]

# Farbverlauf und Punktgröße
norm = (calendar_df['sightings'] - calendar_df['sightings'].min()) / (calendar_df['sightings'].max() - calendar_df['sightings'].min())
start_color = np.array(to_rgb("#4A62D0"))
end_color = np.array(to_rgb("#90FCC3"))
calendar_df['color'] = [to_hex(start_color * (1 - n) + end_color * n) for n in norm]
calendar_df['size'] = 1 + norm * 30  # Punktgröße: 4–20 px

# Feiertagsbeschriftungen
annotations = {
    (1, 1): "New Year",
    (7, 4): "Independence Day",
    (6, 1): "Start of Summer",
    (6, 15): "Father's Day",
    (7, 15): "Mid-Summer Peak",
    (6, 30): "Meteor Watch Day",
    (8, 15): "Assumption Day",
    (10, 31): "Halloween",
    (11, 11): "Veterans Day",
    (12, 25): "Christmas",
    (12, 31): "New Year's Eve"
}

# Punktplot statt Rechtecke
scatter = go.Scatter(
    x=calendar_df['day'] - 0.5,
    y=calendar_df['month'] - 0.5,
    mode='markers',
    marker=dict(
        color=calendar_df['color'],
        size=calendar_df['size'],
        line=dict(width=0)
    ),
    hovertext=[f"{int(row['day'])}.{int(row['month'])}: {int(row['sightings'])} sightings" for _, row in calendar_df.iterrows()],
    hoverinfo='text'
)

fig = go.Figure(data=[scatter])

# Annotationen einfügen
for (month, day), label in annotations.items():
    fig.add_annotation(
        x=day - 0.5,
        y=month - 0.5,
        text=label,
        showarrow=False,
        font=dict(size=8, color="white"),
        xanchor='center',
        yshift=15, 
        yanchor='bottom'
    )

# Achsenlayout mit verschobenen Ticks
fig.update_layout(
    template="plotly_dark",
    width=1000,
    height=600,
    margin=dict(t=20, b=20, l=20, r=20),
    xaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        tickmode='array',
        tickvals=[d + 0.5 for d in range(31)],
        ticktext=[str(d + 1) for d in range(31)],
        title='Day',
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        tickmode='array',
        tickvals=[m + 0.5 for m in range(12)],
        ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        title='Month',
    )
)

fig.update_xaxes(range=[0, 31])
fig.update_yaxes(range=[0, 12])

# Speichern
os.makedirs(os.path.dirname(html_output), exist_ok=True)
fig.write_html(html_output)
