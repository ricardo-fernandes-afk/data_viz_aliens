import pandas as pd

# Pfad zur Datei – ggf. anpassen
csv_path = "E_ufo_story_project/E01_data/ufo_cleaned_new.csv"

# Laden & vorbereiten
df = pd.read_csv(csv_path, low_memory=False)
df.columns = df.columns.str.strip().str.lower()
df['occurred'] = pd.to_datetime(df['occurred'], errors='coerce')
df = df.dropna(subset=['occurred'])

# Gruppieren nach Kalendertag (ohne Jahr)
df['month_day'] = df['occurred'].dt.strftime('%m-%d')
top_days = df.groupby('month_day').size().sort_values(ascending=False)

# Top 20 anzeigen
top_n = 20
print(f"\nTop {top_n} Kalendertage mit den meisten UFO-Sichtungen (über alle Jahre):")
print(top_days.head(top_n).to_frame("sightings"))