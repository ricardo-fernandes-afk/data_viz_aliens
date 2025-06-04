import pandas as pd
import csv

# JSON-Datei laden
df = pd.read_json("E_ufo_story_project/E01_data/nuforc.json")

# Zeitspalte bereinigen
df['Occurred'] = df['Occurred'].str.replace(" Local", "", regex=False)
df['Occurred'] = pd.to_datetime(df['Occurred'], errors='coerce')
df['Year'] = df['Occurred'].dt.year

# Optional: nur relevante Spalten behalten
columns_to_keep = ['Sighting', 'Occurred', 'Location', 'Shape', 'Duration', 'Reported', 'Summary', 'Text', 'Year']
df = df[columns_to_keep]

# Zeilenumbrüche in Texten durch Leerzeichen ersetzen
df.replace({r'[\r\n]+': ' '}, regex=True, inplace=True)

# Export als lesbare CSV mit sauberen Feldern
df.to_csv(
    "E_ufo_story_project/E01_data/ufo_cleaned.csv",
    index=False,
    quoting=csv.QUOTE_ALL,           # Alle Felder in Anführungszeichen
    lineterminator="\n",            # Normale Zeilenumbrüche
    encoding="utf-8"
)

print("✅ Lesbare CSV-Datei erfolgreich erstellt: E01_data/ufo_cleaned_readable.csv")
