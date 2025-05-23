from jinja2 import Environment, FileSystemLoader
import os

# Templatepfad absolut zum Skriptverzeichnis
base_dir = os.path.dirname(__file__)
template_dir = os.path.join(base_dir, "E03_2_templates")
output_path = os.path.join(base_dir, "ufo_story.html")

# Abschnittsdaten
sections = [
    {
        "title": "When the Sky Went Crazy",
        "text": "Sightings surged in waves—perhaps reflecting cultural moments, not cosmic arrivals.",
        "chart": "E03_1_charts/slide1_timeline.html"
    },
    {
        "title": "Aliens Love Summer Nights",
        "text": "Most sightings occur in summer and after dark—coincidence?",
        "chart": "E03_1_charts/slide2_months.html"
    }
]


# Template laden
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template("story_templates.html")

# HTML erzeugen
output = template.render(sections=sections)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(output)

print("✅ ufo_story.html created.")
import webbrowser
webbrowser.open("ufo_story.html")

