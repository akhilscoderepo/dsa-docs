// Real-browser check of a built chapter: layout at desktop and phone widths, console errors, persistence, screenshots.
// Usage: node render_check.mjs CHAPTER.html [OUTDIR]     Needs: npm ci (playwright-core) and a Chromium binary.
// Browser lookup: $CHROMIUM_PATH, Playwright Chromium (Linux/macOS/Windows cache dirs), then Chrome and Edge in their usual install paths.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright-core')); } catch { console.log('SKIPPED: playwright-core is not installed (npm ci)'); process.exit(2); }

function findBrowser() {
  if (process.env.CHROMIUM_PATH && fs.existsSync(process.env.CHROMIUM_PATH)) return process.env.CHROMIUM_PATH;
  const env = process.env;
  const roots = [env.PLAYWRIGHT_BROWSERS_PATH, '/opt/pw-browsers', path.join(env.HOME || env.USERPROFILE || '', '.cache/ms-playwright'),
    path.join(env.LOCALAPPDATA || '', 'ms-playwright'), path.join(env.HOME || '', 'Library/Caches/ms-playwright')].filter(Boolean);
  for (const r of roots) {
    if (!fs.existsSync(r)) continue;
    for (const d of fs.readdirSync(r).filter(n => /^chromium(-\d+)?$/.test(n)).sort().reverse()) {
      for (const sub of ['chrome-linux/chrome', 'chrome-linux64/chrome', 'chrome-mac/Chromium.app/Contents/MacOS/Chromium', 'chrome-win/chrome.exe', 'chrome-win64/chrome.exe']) {
        const p = path.join(r, d, sub); if (fs.existsSync(p)) return p;
      }
    }
  }
  const win = [env.PROGRAMFILES, env['PROGRAMFILES(X86)'], env.LOCALAPPDATA].filter(Boolean).flatMap(b => [
    path.join(b, 'Google/Chrome/Application/chrome.exe'), path.join(b, 'Microsoft/Edge/Application/msedge.exe'), path.join(b, 'Chromium/Application/chrome.exe')]);
  for (const p of [...win, '/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/google-chrome', '/usr/bin/microsoft-edge',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge']) if (fs.existsSync(p)) return p;
  return null;
}
const exe = findBrowser();
if (!exe) { console.log('SKIPPED: no Chromium binary found (set CHROMIUM_PATH)'); process.exit(2); }

const file = path.resolve(process.argv[2]);
const outDir = path.resolve(process.argv[3] || 'render-out');
fs.mkdirSync(outDir, { recursive: true });
const url = pathToFileURL(file).href;
let failed = 0;
const ok = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); if (!c) failed++; };

const browser = await chromium.launch({ executablePath: exe, args: ['--no-sandbox'] });
async function session(name, viewport, extra = {}) {
  const ctx = await browser.newContext({ viewport, ...extra });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  page.on('requestfailed', r => errors.push('request failed: ' + r.url().slice(0, 80)));
  await page.goto(url);
  await page.waitForLoadState('load');
  return { ctx, page, errors, name };
}
const layout = page => page.evaluate(() => {
  const de = document.documentElement, vw = de.clientWidth, over = [];
  for (const el of document.querySelectorAll('main *')) {
    const r = el.getBoundingClientRect();
    if (r.width > 0 && r.right > vw + 1 && !el.closest('pre') && !el.closest('.tablewrap') && !el.closest('nav') && !getComputedStyle(el).position.match(/fixed|sticky/)) over.push(el.tagName + '.' + el.className);
  }
  const small = [...document.querySelectorAll('button, select, input[type=checkbox], summary')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && (r.height < 28 || r.width < 28); }).length;
  const fs = parseFloat(getComputedStyle(document.body).fontSize);
  const codeFs = Math.min(...[...document.querySelectorAll('pre.code')].map(p => parseFloat(getComputedStyle(p).fontSize)));
  return { scrollW: de.scrollWidth, vw, overflowing: over.slice(0, 5), small, fs, codeFs, h: de.scrollHeight };
});

for (const [name, vp, extra] of [['desktop', { width: 1280, height: 900 }, {}], ['phone', { width: 390, height: 844 }, { isMobile: true, hasTouch: true, deviceScaleFactor: 2 }]]) {
  const s = await session(name, vp, extra), page = s.page;
  ok(s.errors.length === 0, `${name}: no console or network errors` + (s.errors.length ? ' - ' + s.errors[0] : ''));
  const L = await layout(page);
  ok(L.scrollW <= L.vw + 1, `${name}: no horizontal page scroll (scrollWidth ${L.scrollW} vs ${L.vw})`);
  ok(L.overflowing.length === 0, `${name}: no content overflows the viewport` + (L.overflowing.length ? ': ' + L.overflowing.join(', ') : ''));
  ok(L.fs >= 16, `${name}: body text is ${L.fs}px (>= 16)`);
  ok(L.codeFs >= 12.5, `${name}: code text is ${L.codeFs}px (>= 12.5)`);
  if (name === 'phone') ok(L.small === 0, `phone: ${L.small} tap targets smaller than 28px`);
  await page.screenshot({ path: path.join(outDir, `${name}-top.png`) });
  const menu = await page.locator('#menu-btn').isVisible();
  ok(name === 'phone' ? menu : !menu, `${name}: menu button ${name === 'phone' ? 'visible' : 'hidden'}`);
  if (name === 'phone') {
    await page.click('#menu-btn');
    ok(await page.locator('nav.side').isVisible(), 'phone: contents drawer opens');
    await page.screenshot({ path: path.join(outDir, 'phone-menu.png') });
    await page.click('#menu-btn');
  }
  // interactions in the real browser
  const trace = page.locator('.trace').first();
  await trace.scrollIntoViewIfNeeded();
  await trace.locator('[data-a=next]').click(); await trace.locator('[data-a=next]').click();
  ok((await trace.locator('.ct').textContent()).startsWith('Step 3'), `${name}: trace Next works in a real browser`);
  await page.screenshot({ path: path.join(outDir, `${name}-trace.png`) });
  const ex = page.locator('.exercise').first();
  await ex.scrollIntoViewIfNeeded();
  const note = ex.locator('textarea.note');
  await note.fill('browser note ' + name);
  await ex.locator('select.status-sel').selectOption('solved');
  await ex.locator('details.hint > summary').click();
  ok(await ex.locator('details.hint').evaluate(d => d.open), `${name}: hint expands`);
  await page.screenshot({ path: path.join(outDir, `${name}-exercise.png`) });
  await page.waitForTimeout(400);
  await page.reload(); await page.waitForLoadState('load');
  ok((await page.locator('textarea.note').first().inputValue()) === 'browser note ' + name, `${name}: notes survive a real reload (file:// localStorage)`);
  ok((await page.locator('select.status-sel').first().inputValue()) === 'solved', `${name}: status survives a real reload`);
  ok(/1\/\d+ solved/.test(await page.locator('#progress-text').textContent()), `${name}: progress restored after reload`);
  await page.locator('#my-notes').scrollIntoViewIfNeeded();
  await page.screenshot({ path: path.join(outDir, `${name}-notes.png`) });
  // theme: dark must keep text readable (contrast of body vs background)
  await page.emulateMedia({ colorScheme: 'dark' });
  const c = await page.evaluate(() => { const cs = getComputedStyle(document.body); return [cs.color, cs.backgroundColor]; });
  const lum = s => { const m = s.match(/\d+/g).map(Number).slice(0, 3).map(v => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }); return 0.2126 * m[0] + 0.7152 * m[1] + 0.0722 * m[2]; };
  const ratio = (Math.max(lum(c[0]), lum(c[1])) + 0.05) / (Math.min(lum(c[0]), lum(c[1])) + 0.05);
  ok(ratio >= 7, `${name}: dark mode body contrast ${ratio.toFixed(1)}:1`);
  await page.screenshot({ path: path.join(outDir, `${name}-dark.png`) });
  await s.ctx.close();
}
await browser.close();
console.log(failed ? `\n${failed} check(s) failed. Screenshots are in ${outDir}` : `\nall checks passed. Screenshots are in ${outDir}`);
process.exit(failed ? 1 : 0);
