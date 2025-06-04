import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# 0) Pfade definieren
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
data_path = os.path.join(base_dir, "E01_data", "ufo_cleaned_new.csv")
output_path = os.path.join("F_final_project", "html_to_run", "slide4_diagram.html")

# 1) Daten einlesen und Jahr extrahieren
df = pd.read_csv(data_path, low_memory=False)
df["datetime"] = pd.to_datetime(df["Occurred"], errors="coerce")
df["year"] = df["datetime"].dt.year
df = df[df["year"].notna()].astype({"year": int})
df["shape"] = df["Shape"].str.lower().str.strip()

# 2) Häufigkeit pro Jahr × Shape berechnen
counts = df.groupby(["year", "shape"]).size().unstack(fill_value=0)

# 3) Top 20 Shapes auswählen, Rest zu "others" bündeln
totals = counts.sum(axis=0).sort_values(ascending=False)
top19 = totals.head(19).index.tolist()
others = [s for s in totals.index if s not in top19]
counts["others"] = counts[others].sum(axis=1)
counts = counts[top19 + ["others"]]

# 4) Index auf alle Jahre erweitern und reset_index
all_years = range(1950, 2024)  # von 1925 bis 2025
counts = counts.reindex(all_years, fill_value=0).reset_index().rename(columns={"index": "year"})

# 5) Konstanten für Achsen-Range ermitteln
year_min = 1950
year_max = 2023
shapes = [col for col in counts.columns if col != "year"]
y_max = counts[shapes].values.max()

# 6) Small Multiples (3 Reihen × 7 Spalten = 21 Plots)
fig = make_subplots(
    rows=5, cols=4,
    subplot_titles=[s.title() for s in shapes],
    shared_xaxes=True,      # X-Achse gleich
    shared_yaxes=True,      # Y-Achse gleich für alle Subplots
    horizontal_spacing=0.1,
    vertical_spacing=0.1,
)

for i, shape in enumerate(shapes):
    row = (i // 4) + 1
    col = (i % 4) + 1

    # Linie für dieses Shape
    fig.add_trace(
        go.Scatter(
            x=counts["year"],
            y=counts[shape],
            mode="lines",
            line_color="#90FCC3",  # Mint-Grün
            hovertemplate="<b>" + shape.title() + "</b><br>Year: %{x}<br>Count: %{y}<extra></extra>"
        ),
        row=row, col=col
    )

    # X-Achse (1925, 1975, 2025) und Grid
    fig.update_xaxes(
        row=row, col=col,
        tickmode="array",
        tickvals=[1950, 1975, 2000, 2023],
        showgrid=True,
        gridcolor="rgba(255,255,255,0.05)",
        range=[year_min, year_max]  # alle Subplots haben dieselbe X-Range
    )

    # Y-Achse (0 bis y_max)
    fig.update_yaxes(
        row=row, col=col,
        range=[0, y_max],
        showgrid=False,
    )

# 7) Gesamt-Layout
fig.update_layout(
    template="plotly_dark",
    showlegend=False,
    height=900,
    width=1200,
    margin=dict(l=40, r=40, t=40, b=40),
)

# 8) HTML-Datei speichern
os.makedirs(os.path.dirname(output_path), exist_ok=True)
fig.write_html(output_path)

print(f"✅ Small multiples erfolgreich gespeichert unter: {output_path}")
