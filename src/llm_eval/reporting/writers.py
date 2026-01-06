import json
from jinja2 import Template

def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def write_markdown(path, stats):
    tpl = Template("""
# LLM Evaluation Report

{% for _, row in stats.iterrows() %}
### {{ row["model"] }} — {{ row["metric"] }}
- Mean: {{ "%.3f"|format(row["mean"]) }}
- Median: {{ "%.3f"|format(row["median"]) }}
- Std: {{ "%.3f"|format(row["std"]) }}
- Min: {{ "%.3f"|format(row["min"]) }}
- Max: {{ "%.3f"|format(row["max"]) }}

{% endfor %}
""")
    with open(path, "w") as f:
        f.write(tpl.render(stats=stats))
