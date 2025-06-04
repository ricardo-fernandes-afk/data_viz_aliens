import os
from jinja2 import Environment, FileSystemLoader

# Bestimme das Verzeichnis, in dem das Skript liegt
template_dir = os.path.dirname(__file__)
env = Environment(loader=FileSystemLoader(template_dir))

# Lade das Haupt-Template (enthält {% include ... %})
template = env.get_template('template.html')

# Rendere das Template (fügt chapter1.html, chapter2.html usw. zusammen)
output = template.render()

# Erstelle den Output-Ordner (dist), falls nicht vorhanden
output_path = os.path.join(template_dir, 'html_to_run')
os.makedirs(output_path, exist_ok=True)

# Schreibe das gerenderte HTML in dist/index.html (UTF-8 wegen Emojis)
with open(os.path.join(output_path, 'ufos_in_the_sky.html'), 'w', encoding='utf-8') as f:
    f.write(output)

