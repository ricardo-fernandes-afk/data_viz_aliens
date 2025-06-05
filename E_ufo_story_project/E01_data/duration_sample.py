import pandas as pd
import os

# Basisordner korrekt ermitteln
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Absoluter Pfad zur Input-Datei und zur Output-Datei
data_path = os.path.join(base_dir, "E_ufo_story_project", "E01_data", "ufo_cleaned_new.csv")
output_path = os.path.join(base_dir, "E_ufo_story_project", "E01_data", "duration_sample.csv")

# Einlesen & Schreiben
df = pd.read_csv(data_path, low_memory=False)
df[['Duration']].head(1000).to_csv(output_path, index=False)
