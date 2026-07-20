/* Generate og-image.png — the 1200x630 social card previewed when the atlas URL is shared.
 *
 * Run:  node tools/make_og_image.mjs
 * Setup (once):  cd tools && npm install   (same puppeteer-core as the axe harness)
 *
 * The card carries the atlas NAME and SUBTITLE only, deliberately NO counts. A social card lives on
 * the hosted URL where the name and og:description already do the persuading, and a count baked into
 * a PNG is the one artifact type every gate in this project is blind to — no JSON diff, no
 * check_urls.py, no axe run will ever catch "378" going stale inside an image. Leaving counts out
 * kills that staleness class at birth, which is why there is no maintenance trigger for this file.
 * The live counts stay in og:description (text, built from the dataset, cannot drift). See
 * AUDIT-FINDINGS 29.3.
 *
 * Because it carries no volatile data, this card only needs regenerating if the brand name or tagline
 * changes — both of which are read here from compliance-atlas.json, so a rebuild-then-rerun keeps it
 * in sync. It is a committed asset, not a build step: build_html.py does not run it.
 *
 * Visual language matches the site's folio styling (paper ground, accent ink, serif display, the
 * paragraph-mark brand glyph), so the preview reads as the same publication as the page it opens.
 */
import puppeteer from "puppeteer-core";
import { existsSync, readFileSync } from "fs";
import { dirname, resolve } from "path";
import { fileURLToPath } from "url";

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
const OUT = resolve(ROOT, "og-image.png");
const WIDTH = 1200, HEIGHT = 630;

const CHROME_CANDIDATES = [
  process.env.CHROME_PATH,
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/usr/bin/google-chrome",
  "/usr/bin/chromium",
].filter(Boolean);
const chrome = CHROME_CANDIDATES.find(existsSync);
if (!chrome) { console.error("No Chrome found. Set CHROME_PATH."); process.exit(2); }

// Name and subtitle come from the built dataset so the card cannot drift from the brand. Nothing
// numeric is read — the card is countless by design.
const meta = JSON.parse(readFileSync(resolve(ROOT, "compliance-atlas.json"), "utf8")).meta;
const title = meta.brand.title;
const subtitle = meta.brand.tagline;
const host = "yazarmyint.github.io/compliance-atlas";

const esc = s => s.replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

const HTML = `<!doctype html><html><head><meta charset="utf-8"><style>
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:${WIDTH}px;height:${HEIGHT}px}
  body{
    background:
      radial-gradient(120% 140% at 100% 0%, #fffdf8 0%, #faf7f0 46%, #f2ede1 100%);
    color:#20242c;
    font-family:"Segoe UI Variable Text","Segoe UI",-apple-system,"Helvetica Neue",sans-serif;
    position:relative; overflow:hidden;
  }
  /* Thin accent frame, inset — the same border-and-paper feel as the atlas cards. */
  .frame{position:absolute; inset:26px; border:1.5px solid #c5bda9; border-radius:20px}
  /* Oversized brand glyph as a quiet watermark, bleeding off the right edge. */
  .mark{position:absolute; right:-46px; top:-96px; font-family:Cambria,"Palatino Linotype",Georgia,serif;
    font-weight:600; font-size:640px; line-height:1; color:#7c2d12; opacity:.06}
  /* Content is centred in the region ABOVE the host strip (top:0 to 118px-from-bottom) so the
     wrapped subtitle can never collide with the host line pinned at the bottom. */
  .stack{position:absolute; left:96px; top:0; bottom:118px; display:flex; flex-direction:column;
    justify-content:center; max-width:770px}
  .overline{font-size:22px; letter-spacing:.26em; text-transform:uppercase; color:#7c2d12; font-weight:700}
  .overline .glyph{font-family:Cambria,Georgia,serif}
  h1{font-family:Cambria,"Palatino Linotype",Georgia,"Times New Roman",serif; font-weight:600;
    font-size:108px; line-height:1.03; letter-spacing:-.01em; color:#20242c; margin:22px 0 0}
  .rule{width:132px; height:6px; background:#7c2d12; border-radius:3px; margin:32px 0 30px}
  .sub{font-size:42px; line-height:1.26; color:#565b66; font-weight:400; max-width:720px}
  .host{position:absolute; left:96px; bottom:60px; font-family:"Cascadia Code",Consolas,monospace;
    font-size:22px; color:#656870; letter-spacing:.01em}
</style></head><body>
  <div class="mark">&para;</div>
  <div class="frame"></div>
  <div class="stack">
    <div class="overline"><span class="glyph">&para;</span>&nbsp;&nbsp;Compliance reference</div>
    <h1>${esc(title)}</h1>
    <div class="rule"></div>
    <div class="sub">${esc(subtitle)}</div>
  </div>
  <div class="host">${esc(host)}</div>
</body></html>`;

const browser = await puppeteer.launch({ executablePath: chrome, headless: "new" });
const page = await browser.newPage();
await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 1 });
await page.setContent(HTML, { waitUntil: "load" });
await new Promise(r => setTimeout(r, 200));            // let the web-safe fonts settle
await page.screenshot({ path: OUT, clip: { x: 0, y: 0, width: WIDTH, height: HEIGHT } });
await browser.close();
console.log(`Wrote ${OUT} (${WIDTH}x${HEIGHT}, countless card: "${title}" / "${subtitle}")`);
