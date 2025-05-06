import kagglehub
import pandas as pd
import numpy as np
import os

# Step 1: Datensatz laden über API
path = kagglehub.dataset_download("NUFORC/ufo-sightings")
print("Dataset saved at:", path)

# Step 2: Lade CSV-Datei
csv_path = os.path.join(path, "ufo_sightings.csv")
df = pd.read_csv(csv_path)

# Step 3: Wichtige Spalten bereinigen
df = df[['datetime', 'city', 'state', 'country', 'shape', 'duration_seconds', 'comments', 'date_posted', 'latitude', 'longitude']]

# Step 4: Zeitangaben verarbeiten
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
df['year'] = df['datetime'].dt.year
df['month'] = df['datetime'].dt.month
df['hour'] = df['datetime'].dt.hour

# Step 5: Dauer als log-transformierte Spalte
df['duration_seconds'] = pd.to_numeric(df['duration_seconds'], errors='coerce')
df['log_duration'] = np.log1p(df['duration_seconds'])

# Step 6: UFO-Form vereinheitlichen (Top 10 + "other")
top_shapes = df['shape'].value_counts().nlargest(10).index
df['shape_simplified'] = df['shape'].where(df['shape'].isin(top_shapes), other='other')

# Step 7: Entferne NaNs in wichtigen Feldern
df = df.dropna(subset=['datetime', 'shape_simplified', 'duration_seconds'])

# Optional: Nur gültige Koordinaten für Maps
df_geo = df.dropna(subset=['latitude', 'longitude'])

# Step 8: Überblick
print("Daten fertig vorbereitet – Anzahl Zeilen:", len(df))
print("Zeitraum:", df['year'].min(), "bis", df['year'].max())
print("Beispielhafte Formen:", df['shape_simplified'].unique())

# Optional: Abspeichern als Clean-Version
df.to_csv("ufo_cleaned.csv", index=False)
