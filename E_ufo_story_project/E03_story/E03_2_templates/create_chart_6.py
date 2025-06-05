import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import os

# Pfade festlegen
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
data_path = os.path.join(base_dir, "E01_data", "ufo_cleaned.csv")
img_output = os.path.join("F_final_project", "html_to_run", "slide6_diagram.png")

# Daten laden
df = pd.read_csv(data_path, low_memory=False)
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
df = df.dropna(subset=['datetime'])

# Feiertage definieren
holidays = ["01-01", "04-01", "07-04", "10-31", "12-25", "12-31"]
df['month_day'] = df['datetime'].dt.strftime('%m-%d')

# Nur Kommentare von Feiertagen
comments = df[df['month_day'].isin(holidays)]['comments'].dropna().astype(str)
text = " ".join(comments).lower()

# Stoppwörter + eigene Ausschlüsse
stopwords = set(STOPWORDS)
stopwords.update(["just", "like", "could", "would", "also", "one", "two", "three", "four", "ufo", "object", "objects", "something", "thing", "things", "still"])

# Wordcloud erstellen
wc = WordCloud(
    background_color="black",
    width=1600,
    height=800,
    max_words=80,
    stopwords=stopwords,
    colormap="winter",
    contour_color="#4A62D0",
    contour_width=0.4
).generate(text)

# Speichern
os.makedirs(os.path.dirname(img_output), exist_ok=True)
wc.to_file(img_output)
print(f"✅ Slide 6 Wordcloud gespeichert: {img_output}")

