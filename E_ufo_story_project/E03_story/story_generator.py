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
        "chart": "E03_1_charts/slide2_months.html",
        "chart2": "E03_1_charts/slide2_2_hours.html"
    },
    {
    "title": "Hotspots on Earth",
    "text": "The majority of sightings come from the US. But not all states are equal: California, Florida and Texas lead the list.",
    "chart": "E03_1_charts/slide3_hotspots.html",
    "chart2": "E03_1_charts/slide3_world.html"
    },
    {
    "title": "Triangles, Fireballs and Lights",
    "text": "In the 60s, classic discs dominated. Today, it's fireballs, lights and triangles. Are aliens upgrading their vehicles—or are we just describing what we expect to see?",
    "chart": "E03_1_charts/slide4_shapes.html"
    },
    {
    "title": "Blink and They're Gone?",
    "text": "Most sightings are short—many last less than 5 minutes. But some UFO types linger longer than others.",
    "chart": "E03_1_charts/slide5_1_donut_duration.html",
    "chart2": "E03_1_charts/slide5_2_heatmap_shape_duration.html"
    },
    {
    "title": "Aliens and Holidays",
    "text": "Sightings peak on Halloween, New Year’s and the Fourth of July. Maybe aliens love fireworks—or they just like to party.",
    "chart": "E03_1_charts/slide6_wordcloud_cleaned.png"
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
