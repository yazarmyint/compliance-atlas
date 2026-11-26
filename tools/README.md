# tools/

Standing QA for the atlas. Neither tool is part of the published artifact — nothing in here ships
to a reader, and `compliance-atlas.html` has no dependency on either. Both are checks you run
against the built output, and both exit non-zero on failure so they can gate a release.

| Tool | Checks | Needs |
|---|---|---|
| `check_urls.py` | Every URL cited anywhere in the dataset still resolves, and has not silently redirected somewhere else | Python 3, no packages |
| `axe_check.mjs` | WCAG 2.1 A/AA, every view type × both themes | Node 18+, `npm install`, installed Chrome |

## check_urls.py — citation resolution

```powershell
python tools/check_urls.py                          # full sweep
python tools/check_urls.py --json report.json       # machine-readable output
python tools/check_urls.py --only learn.microsoft.com
```

Verdicts are `OK`, `REDIRECT` (resolves, but the cited page moved — the citation has degraded and
should be repointed), `WAF` (a host that refuses scripted clients but serves the page to a browser),
and `BROKEN`. Requests to rate-limiting hosts are serialised, so a full run takes several minutes;
that is deliberate, because a parallel sweep produces spurious failures.

`WAF` is not a pass. Each such host is listed in `WAF_HOSTS` with the status it returns to the script,
the date a person last opened the cited page in a browser, and what they saw. Every run prints those
pages under **CHECK BY HAND**. The script does not try to get past a refusal (no user-agent rotation);
a person with a browser is the check. The status is matched per host, so a 404 counts as a refusal for
`www.ftc.gov` only.

Exit code is 0 only when nothing is `BROKEN`, nothing is `REDIRECT`, and no hand check is older than
90 days. Offline unit tests of the verdict logic are in `tests/test_check_urls.py`.

## axe_check.mjs — accessibility

Install once:

```powershell
cd tools
npm install
```

Then, from the repository root:

```powershell
node tools/axe_check.mjs                            # the built file, from file://
node tools/axe_check.mjs --url https://yazarmyint.github.io/compliance-atlas/compliance-atlas.html
node tools/axe_check.mjs --routes "#/,#/about" --themes dark --json a11y.json
```

It drives the Chrome already installed on the machine through `puppeteer-core` rather than
downloading its own; set `CHROME_PATH` if yours is not in a standard location. Exit code is 0 only
when every route/theme combination reports zero violation nodes, and a theme that fails to apply
counts as a failure rather than a pass, since contrast results against the wrong palette are
meaningless.

`tools/node_modules/` is gitignored. Keep the route list in `ALL_ROUTES` in step with the router in
`build/template.html`: a route missing there is a route that never gets audited.

**What a clean run does and does not mean.** axe automates roughly a third of WCAG success
criteria. Zero violations is a floor, not a certification, and it is not a substitute for a pass
with a real screen reader (NVDA or JAWS) — which remains unperformed. See `AUDIT-FINDINGS.md` §21.
