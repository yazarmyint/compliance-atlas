/* Standing QA for accessibility: axe-core WCAG 2.1 A/AA over every route, in both themes.
 *
 * Run:  node tools/axe_check.mjs [--url <target>] [--routes a,b,c] [--themes light,dark] [--json out.json]
 *
 * With no --url it audits the built file from file://, which is the offline artifact readers
 * actually download. Pass --url to audit the hosted copy instead:
 *
 *   node tools/axe_check.mjs
 *   node tools/axe_check.mjs --url https://yazarmyint.github.io/compliance-atlas/compliance-atlas.html
 *
 * Setup (once):  cd tools && npm install
 *
 * This harness was rebuilt from scratch twice (AUDIT-FINDINGS 21.1, 22) before being committed
 * here. It drives the Chrome already installed on the machine via puppeteer-core rather than
 * downloading a browser, so `npm install` stays small; set CHROME_PATH if yours is somewhere
 * unusual. Exit code is 0 only when every route/theme combination reports zero violation nodes.
 *
 * Automated checks cover roughly a third of WCAG success criteria. A clean run here is a floor,
 * not a certification, and does not substitute for a pass with a real screen reader.
 */
import puppeteer from "puppeteer-core";
import { existsSync, readFileSync, writeFileSync } from "fs";
import { createRequire } from "module";
import { dirname, resolve } from "path";
import { fileURLToPath, pathToFileURL } from "url";

const require = createRequire(import.meta.url);
const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
const axeSource = readFileSync(require.resolve("axe-core/axe.min.js"), "utf8");

// One route per view type the router in build/template.html can render, plus the two newest
// industry lenses. Note there is no #/industries route: the industries index is the landing page.
// The row-listing views (#/framework/..., #/product/.../solution/..., #/cell/..., #/search/...)
// are where nearly all violation nodes have historically lived, because that is where the row
// disclosures and the coverage chips are, so each is represented. iso-27001-2022 is the largest
// framework at 57 rows, which makes it the heaviest single page in the atlas.
const ALL_ROUTES = [
  "#/",                                              // landing + industries index
  "#/about",
  "#/frameworks",
  "#/framework/iso-27001-2022",                      // framework rows (largest, 57)
  "#/products",
  "#/product/purview",
  "#/product/purview/solution/Data%20Loss%20Prevention",
  "#/matrix",
  "#/matrix/purview",
  "#/cell/purview/iso-27001-2022/Data%20Loss%20Prevention",
  "#/search/retention",
  "#/industry/legal",
  "#/industry/insurance",
  "#/row/iso-a-5-10",                                 // PR-004 row deep link, valid id (single-row view)
  "#/row/no-such-row",                               // PR-004 row deep link, invalid id (not-found state)
];

const WCAG_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"];

const CHROME_CANDIDATES = [
  process.env.CHROME_PATH,
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/usr/bin/google-chrome",
  "/usr/bin/chromium",
].filter(Boolean);

function arg(name, fallback) {
  const i = process.argv.indexOf(`--${name}`);
  return i !== -1 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}

const chrome = CHROME_CANDIDATES.find(existsSync);
if (!chrome) {
  console.error(`No Chrome found. Tried:\n  ${CHROME_CANDIDATES.join("\n  ")}\nSet CHROME_PATH.`);
  process.exit(2);
}

const target = arg("url") || pathToFileURL(resolve(ROOT, "compliance-atlas.html")).href;
const routes = arg("routes", ALL_ROUTES.join(",")).split(",");
const themes = arg("themes", "light,dark").split(",");
const jsonOut = arg("json");

console.log(`target: ${target}`);
console.log(`chrome: ${chrome}`);
console.log(`${routes.length} routes x ${themes.length} themes = ${routes.length * themes.length} combinations\n`);

const browser = await puppeteer.launch({
  executablePath: chrome,
  headless: "new",
  args: ["--allow-file-access-from-files"],
});

const report = [];
let total = 0;

for (const theme of themes) {
  for (const route of routes) {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 900 });
    // The theme goes in the query string and the route in the hash, then the hash is set again
    // after load: a hash present in the initial URL does not always fire the router's
    // hashchange, and setting it explicitly makes the navigation deterministic.
    await page.goto(`${target}?theme=${theme}${route}`, { waitUntil: "load", timeout: 60000 });
    await page.evaluate(r => { location.hash = r; }, route);
    await new Promise(r => setTimeout(r, 350));

    const gotTheme = await page.evaluate(() => document.documentElement.dataset.theme);
    const h1 = await page.evaluate(() => document.querySelector("#app h1")?.textContent?.trim() || "(none)");

    await page.evaluate(axeSource);
    const res = await page.evaluate(async tags =>
      await axe.run(document, { runOnly: { type: "tag", values: tags } }), WCAG_TAGS);

    const nodes = res.violations.reduce((n, v) => n + v.nodes.length, 0);
    total += nodes;
    report.push({ theme, route, appliedTheme: gotTheme, h1, nodes,
      violations: res.violations.map(v => ({ id: v.id, impact: v.impact, help: v.help, nodes: v.nodes.length })) });

    console.log(`${nodes ? "FAIL" : "ok  "} ${theme.padEnd(5)} ${route.padEnd(22)} theme=${gotTheme} h1="${h1.slice(0, 42)}" violations=${nodes}`);
    for (const v of res.violations) {
      console.log(`      [${v.impact}] ${v.id}: ${v.help} (${v.nodes.length})`);
      for (const n of v.nodes.slice(0, 3)) console.log(`         ${n.html.slice(0, 150)}`);
    }
    // A theme that did not apply means the audit ran against the wrong palette, so the
    // contrast results are meaningless rather than passing. Treat it as a failure.
    if (gotTheme !== theme) {
      console.log(`      ATTENTION: requested theme ${theme} but document reports ${gotTheme}`);
      total += 1;
    }
    await page.close();
  }
}

await browser.close();
if (jsonOut) {
  writeFileSync(jsonOut, JSON.stringify({ target, generated: new Date().toISOString(), total, report }, null, 2));
  console.log(`\nWrote ${jsonOut}`);
}
console.log(`\nTOTAL VIOLATION NODES: ${total}`);
process.exit(total ? 1 : 0);
