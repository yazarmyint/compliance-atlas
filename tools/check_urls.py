"""Standing QA for the atlas's cited URLs: resolution and redirect drift.

Run:  python tools/check_urls.py [--json report.json] [--only learn.microsoft.com]

Reads every URL in compliance-atlas.json (row sources, framework official_source /
document_url / template source, and the product naming_source / URL registries as they
appear in the built file) and reports, per URL:

  OK           200, and the final URL matches the cited one
  REDIRECT     200, but the final URL differs by more than locale insertion
  WAF          403/406 from a host known to block automated clients (documented, not a defect)
  BROKEN       any other status, or a transport error

Two things this exists to catch that a plain 200-check does not:

1. Redirect drift. Microsoft retires redirects eventually, and a redirect often means the
   cited page was consolidated into another article, which degrades the citation even while
   it still resolves. Locale insertion (/en-us/) is normalised away because it is noise.

2. False failures from rate limiting. learn.microsoft.com returns 429 under parallel load;
   a naive 12-way sweep produced 40 spurious failures, all of which returned 200 on serial
   retry. Requests to throttled hosts are therefore serialised with a delay, and any 429 is
   retried with backoff rather than reported.

Exit code is 0 when nothing is BROKEN and nothing is an unexplained REDIRECT.
"""
import argparse, json, os, re, sys, time, urllib.error, urllib.request
from urllib.parse import urlsplit, urlunsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS = os.path.join(ROOT, "compliance-atlas.json")

# Hosts that rate-limit automated clients. Requests to these are serialised.
THROTTLED_HOSTS = {"learn.microsoft.com", "docs.microsoft.com", "azure.microsoft.com", "www.microsoft.com"}
THROTTLE_SECONDS = 1.1
MAX_RETRIES = 4

# Hosts whose WAF blocks scripted clients outright. Both remain human-reachable, and every
# row citing them also carries a machine-resolving alternate (AUDIT-FINDINGS SS7.2).
WAF_HOSTS = {"dodcio.defense.gov", "www.hhs.gov"}

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
LOCALE = re.compile(r"^/[a-z]{2}-[a-z]{2}(?=/)")


def canonical(url):
    """Strip the locale segment and a trailing slash so /en-us/ insertion is not drift."""
    p = urlsplit(url)
    path = LOCALE.sub("", p.path) or "/"
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    return urlunsplit((p.scheme, p.netloc.lower(), path, p.query, ""))


def collect(atlas):
    """Every cited URL in the built atlas, mapped to the places that cite it."""
    seen = {}

    def add(url, where):
        if isinstance(url, str) and url.startswith("http"):
            seen.setdefault(url, set()).add(where)

    for r in atlas.get("rows", []):
        for s in r.get("sources", []):
            add(s, r["id"])
    for fid, fw in (atlas.get("frameworks") or {}).items():
        add(fw.get("official_source"), f"framework:{fid}")
        add(fw.get("document_url"), f"framework:{fid}")
        tmpl = fw.get("compliance_manager_template") or {}
        add(tmpl.get("source"), f"framework:{fid}")
    for pid, prod in (atlas.get("products") or {}).items():
        add(prod.get("naming_source"), f"product:{pid}")
        add(prod.get("url"), f"product:{pid}")
    for name, sol in (atlas.get("solutions") or {}).items():
        add(sol.get("url"), f"solution:{name}")
    # The project's own off-site links — repository, issue tracker, changelog — which the about page
    # and footer render as real links. They rot exactly like citations do, so they belong in this sweep.
    for key, url in (atlas.get("meta", {}).get("project") or {}).items():
        add(url, f"project:{key}")
    return seen


def fetch(url):
    """Return (status, final_url, note). Retries 429 with backoff."""
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })
    for attempt in range(MAX_RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                return resp.status, resp.geturl(), ""
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < MAX_RETRIES - 1:
                time.sleep(2 ** attempt * 2)
                continue
            return e.code, e.geturl() if hasattr(e, "geturl") else url, e.reason or ""
        except Exception as e:  # transport, DNS, TLS, timeout
            if attempt < MAX_RETRIES - 1:
                time.sleep(1.5)
                continue
            return None, url, f"{type(e).__name__}: {e}"
    return None, url, "retries exhausted"


def classify(url, status, final):
    host = urlsplit(url).netloc.lower()
    if status in (403, 406) and host in WAF_HOSTS:
        return "WAF"
    # Any 2xx is a successful fetch. This was `status != 200`, which reported EUR-Lex as BROKEN:
    # eur-lex.europa.eu answers scripted clients with 202 Accepted (its bot-mitigation path) while
    # serving the correct document at the cited URL. Treating 200 as the only success was the defect,
    # not the citation. Found 2026-07-20.
    if not (status and 200 <= status < 300):
        return "BROKEN"
    return "OK" if canonical(url) == canonical(final) else "REDIRECT"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="write the full report here")
    ap.add_argument("--only", help="check only URLs on this host")
    args = ap.parse_args()

    with open(ATLAS, encoding="utf-8") as fh:
        atlas = json.load(fh)
    cited = collect(atlas)
    urls = sorted(cited)
    if args.only:
        urls = [u for u in urls if urlsplit(u).netloc.lower() == args.only.lower()]

    print(f"Checking {len(urls)} cited URLs "
          f"({sum(1 for u in urls if urlsplit(u).netloc.lower() in THROTTLED_HOSTS)} on throttled hosts)\n")

    results, last_throttled = [], 0.0
    for i, url in enumerate(urls, 1):
        host = urlsplit(url).netloc.lower()
        if host in THROTTLED_HOSTS:
            wait = THROTTLE_SECONDS - (time.monotonic() - last_throttled)
            if wait > 0:
                time.sleep(wait)
            last_throttled = time.monotonic()
        status, final, note = fetch(url)
        verdict = classify(url, status, final)
        results.append({"url": url, "status": status, "final_url": final,
                        "verdict": verdict, "note": note,
                        "cited_by": sorted(cited[url])})
        if verdict != "OK":
            print(f"[{verdict:8}] {url}")
            if verdict == "REDIRECT":
                print(f"{'':11}-> {final}")
            elif note:
                print(f"{'':11}   {status} {note}")
        if i % 25 == 0:
            print(f"  ...{i}/{len(urls)}")

    counts = {}
    for r in results:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    print("\n" + "-" * 60)
    for v in ("OK", "REDIRECT", "WAF", "BROKEN"):
        if counts.get(v):
            print(f"{v:10} {counts[v]}")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(results, fh, indent=1)
        print(f"\nreport -> {args.json}")

    return 1 if counts.get("BROKEN") or counts.get("REDIRECT") else 0


if __name__ == "__main__":
    sys.exit(main())
