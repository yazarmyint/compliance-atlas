"""Generate compliance-atlas.html from the canonical JSON + template.
Run:  python build/build_html.py
Never hand-edit the output file — edit template.html or the row modules, then rebuild.

Renamed 2026-07-17 (platform generalization): reads compliance-atlas.json (was
purview-compliance-map.json) and writes compliance-atlas.html (was purview-compliance-map.html)."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, "compliance-atlas.json")
TEMPLATE = os.path.join(ROOT, "build", "template.html")
OUT = os.path.join(ROOT, "compliance-atlas.html")

def main():
    data = json.load(open(JSON_PATH, encoding="utf-8"))
    payload = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    payload = payload.replace("</", "<\\/")  # keep </script> sequences inert inside the data block
    tpl = open(TEMPLATE, encoding="utf-8").read()
    marker = "/*__DATA__*/"
    assert marker in tpl, "template is missing the data marker"
    html = tpl.replace(marker, payload)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {OUT}")
    print(f"  rows embedded: {len(data['rows'])} | frameworks: {len(data['frameworks'])} | products: {len(data.get('products',{}))} | size: {len(html)/1024:.0f} KB")

if __name__ == "__main__":
    main()
