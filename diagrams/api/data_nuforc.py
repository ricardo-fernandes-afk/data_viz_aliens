import pandas as pd
import numpy as np
import os

# Lokaler Pfad zur CSV-Datei (du hast sie im Ordner diagrams/api gespeichert)
csv_path = os.path.join("diagrams", "api", "complete.csv")

# CSV einlesen
df = pd.read_csv(csv_path, on_bad_lines='skip', low_memory=False)

# Überblick über die Spalten
print("Spalten:", df.columns.tolist())

# Relevante Spalten auswählen (angepasst an dein File!)
df = df[['datetime', 'city', 'state', 'country', 'shape', 'duration_minutes', 'comments', 'latitude', 'longitude']]

# Zeitstempel parsen
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
df = df.dropna(subset=['datetime'])  # nur gültige Zeitstempel behalten
df['year'] = df['datetime'].dt.year
df['month'] = df['datetime'].dt.month
df['hour'] = df['datetime'].dt.hour

# Dauer in Sekunden umrechnen und log-transformieren
df['duration_minutes'] = pd.to_numeric(df['duration_minutes'], errors='coerce')
df['duration_seconds'] = df['duration_minutes'] * 60
df['log_duration'] = np.log1p(df['duration_seconds'])

# Shape vereinfachen (Top 10 behalten)
top_shapes = df['shape'].value_counts().nlargest(10).index
df['shape_simplified'] = df['shape'].where(df['shape'].isin(top_shapes), other='other')

# NaNs in Schlüsselfeldern entfernen
df = df.dropna(subset=['shape_simplified', 'duration_seconds'])

# Geo-Daten vorbereiten für Maps
df_geo = df.dropna(subset=['latitude', 'longitude'])

# Überblick
print("Anzahl Datensätze nach Bereinigung:", len(df))
print("Jahre:", df['year'].min(), "-", df['year'].max())
print("Formen:", df['shape_simplified'].unique())

# Optional: lokal speichern für andere Diagramme
df.to_csv("ufo_cleaned.csv", index=False)
