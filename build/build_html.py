"""Generate compliance-atlas.html from the canonical JSON + template.
Run:  python build/build_html.py
Never hand-edit the output file — edit template.html or the row modules, then rebuild.

Renamed 2026-07-17 (platform generalization): reads compliance-atlas.json (was
purview-compliance-map.json) and writes compliance-atlas.html (was purview-compliance-map.html)."""
import datetime, html, json, os, re, shutil, sys

# ---- stale-bytecode guard (PR-058). MUST stay above any future sibling import. ----
# This entry point imports no build/ module today -- it reads the JSON and the template as files --
# so the guard is preventive here, not load-bearing. It is present because the constraint the
# project wants is "no build entry point can execute against stale cached bytecode", and that has
# to hold for the entry point someone later adds a `from common import ...` to. See the full
# explanation in assemble.py and AUDIT-FINDINGS §26.8.
sys.dont_write_bytecode = True
shutil.rmtree(os.path.join(os.path.dirname(os.path.abspath(__file__)), "__pycache__"),
              ignore_errors=True)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, "compliance-atlas.json")
TEMPLATE = os.path.join(ROOT, "build", "template.html")
OUT = os.path.join(ROOT, "compliance-atlas.html")
INDEX_OUT = os.path.join(ROOT, "index.html")

# Where the atlas is hosted. This is a build/hosting fact, not dataset content, so it lives here
# rather than in compliance-atlas.json. It feeds rel="canonical" and og:url in the atlas, and the
# redirect stub below. Change it here if the site ever moves.
SITE_URL = "https://yazarmyint.github.io/compliance-atlas/"
ATLAS_FILENAME = "compliance-atlas.html"
CANONICAL_URL = SITE_URL + ATLAS_FILENAME

# GitHub Pages serves index.html at the directory root, but the deliverable is named
# compliance-atlas.html and that name is load-bearing: it is what file:// readers download, what
# the release asset is called, and what existing references point at. Rather than rename the output
# or ship a duplicate copy of a ~1 MB file under two names, the root is a redirect stub. It carries
# its own Open Graph tags because link-preview crawlers do not follow meta refresh — without them a
# shared root URL would preview as a blank page.
INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta http-equiv="refresh" content="0; url={filename}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
{favicon}
<style>
html{{color-scheme:light dark}}
body{{margin:0;min-height:100vh;display:grid;place-items:center;
  background:#faf7f0;color:#20242c;
  font:16px/1.6 "Segoe UI Variable Text","Segoe UI",-apple-system,"Helvetica Neue",sans-serif}}
main{{padding:2rem;text-align:center}}
h1{{font-family:Cambria,"Palatino Linotype",Georgia,serif;font-weight:600;margin:0 0 .5rem}}
a{{color:#1e5fae}}
@media (prefers-color-scheme:dark){{
  body{{background:#181b22;color:#e6e2d8}} a{{color:#5b96d6}}
}}
</style>
<script>
/* Runs before the meta refresh fires, and unlike the refresh it carries the hash across, so a
   deep link shared against the site root (e.g. .../#/about) lands on the right view. replace()
   keeps the stub out of the back-button history. The meta refresh above is the no-JS fallback. */
location.replace({filename_js} + location.hash);
</script>
</head>
<body>
<main>
<h1>{title}</h1>
<p>Redirecting to <a href="{filename}">{filename}</a>&hellip;</p>
</main>
</body>
</html>
"""

def main():
    data = json.load(open(JSON_PATH, encoding="utf-8"))
    payload = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    payload = payload.replace("</", "<\\/")  # keep </script> sequences inert inside the data block
    tpl = open(TEMPLATE, encoding="utf-8").read()
    marker = "/*__DATA__*/"
    assert marker in tpl, "template is missing the data marker"
    # Head metadata (title, description, Open Graph) is substituted rather than read from the data
    # island at runtime, so crawlers that do not execute the script still see it. Substituted before
    # the payload goes in, so dataset content can never be mistaken for a marker.
    meta = data["meta"]
    # The footer's build timestamp is produced here, not read from the dataset (PR-057). It used to
    # arrive as meta.generated, which made compliance-atlas.json move on every rebuild and cost the
    # project a strict empty-diff drift check. Same format as before — isoformat to the second — so
    # the rendered footer line is unchanged. Consequence, and it is intended: compliance-atlas.html
    # still carries a moving timestamp and diffs on every rebuild. The drift check is defined on the
    # JSON, not the HTML.
    built_at = datetime.datetime.now().isoformat(timespec="seconds")
    # Substituted into a JS string literal in template.html, so the format is asserted rather than
    # escaped: an ISO timestamp cannot carry a quote or a backslash out of the assertion.
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", built_at), built_at
    for token, value in (("__BRAND_TITLE__", meta["brand"]["title"]),
                         ("__META_DESCRIPTION__", meta["description_meta"]),
                         ("__CANONICAL_URL__", CANONICAL_URL)):
        assert token in tpl, f"template is missing the {token} marker"
        tpl = tpl.replace(token, html.escape(value, quote=True))
    # Substituted unescaped: this one lands inside a script, where HTML entities would render
    # literally rather than decode.
    assert "__BUILT_AT__" in tpl, "template is missing the __BUILT_AT__ marker"
    tpl = tpl.replace("__BUILT_AT__", built_at)
    doc = tpl.replace(marker, payload)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"Wrote {OUT}")
    print(f"  rows embedded: {len(data['rows'])} | frameworks: {len(data['frameworks'])} | products: {len(data.get('products',{}))} | size: {len(doc)/1024:.0f} KB")
    print(f"  built at: {built_at} (stamped into the HTML; the JSON carries no timestamp)")
    write_index(meta)

def write_index(meta):
    """Emit the root redirect stub. Generated, not hand-written, so its title, description and
    favicon cannot drift from the atlas they point at."""
    favicon = re.search(r'^<link rel="icon".*$', open(TEMPLATE, encoding="utf-8").read(), re.M)
    assert favicon, "template is missing the favicon link the stub reuses"
    doc = INDEX_TEMPLATE.format(
        title=html.escape(meta["brand"]["title"], quote=True),
        description=html.escape(meta["description_meta"], quote=True),
        canonical=html.escape(CANONICAL_URL, quote=True),
        filename=ATLAS_FILENAME,
        filename_js=json.dumps(ATLAS_FILENAME),
        favicon=favicon.group(0),
    )
    with open(INDEX_OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"Wrote {INDEX_OUT}")
    print(f"  redirects to: {CANONICAL_URL}")

if __name__ == "__main__":
    main()
