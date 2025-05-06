# Definierte Farbpalette für verschiedene Zwecke
def get_defined_color_palette():
    color_palette = {
        "background_light": "#f5f5f5",  # Helles Grau für Hintergründe
        "background_dark": "#2c2c2c",   # Dunkles Grau für Hintergründe
        "text_light": "#ffffff",        # Weiß für helle Texte
        "text_dark": "#000000",         # Schwarz für dunkle Texte
        "primary": "#1f77b4",           # Blau für primäre Elemente
        "secondary": "#ff7f0e",         # Orange für sekundäre Elemente
        "accent": "#2ca02c",            # Grün für Akzente
        "error": "#d62728",             # Rot für Fehler
        "warning": "#ffcc00",           # Gelb für Warnungen
        "info": "#17becf",              # Türkis für Informationen
        "success": "#98df8a",           # Hellgrün für Erfolg
        # Zusätzliche Farben für Diagramme
        "chart_color_1": "#F25260",
        "chart_color_2": "#04BFBF",
        "chart_color_3": "#F2D022",
        "chart_color_4": "#F27127",
        "chart_color_5": "#bcbd22",
        "chart_color_6": "#17becf",
    }
    return color_palette

# Beispiel: Farbpalette abrufen
color_palette = get_defined_color_palette()

# Farben ausgeben
for name, color in color_palette.items():
    print(f"{name}: {color}")