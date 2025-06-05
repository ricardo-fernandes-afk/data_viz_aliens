import pandas as pd
import numpy as np
import re

# Sample laden
df = pd.read_csv("E_ufo_story_project/E01_data/duration_sample.csv")
df["Duration"] = df["Duration"].astype(str).str.strip().str.lower()

# Funktion einfügen (aus vorherigem Schritt)
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
        num = re.match(r'^\d+\.?\d*$', duration_str)
        if num:
            return float(num.group(0))
    return seconds if seconds > 0 else np.nan

# Anwenden
df["duration_seconds"] = df["Duration"].apply(duration_to_seconds)

# Ergebnis speichern
df.to_csv("E_ufo_story_project/E01_data/duration_sample_converted.csv", index=False)
