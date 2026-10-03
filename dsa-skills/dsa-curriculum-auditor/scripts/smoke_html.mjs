// Headless interaction test for a built chapter file. Usage: node smoke_html.mjs CHAPTER.html
// Needs jsdom: npm install jsdom (set NODE_PATH to its node_modules if it is not local).
import { createRequire } from 'node:module';
import fs from 'node:fs';
const require = createRequire(import.meta.url);
let JSDOM, VirtualConsole;
try { ({ JSDOM, VirtualConsole } = require('jsdom')); } catch (e) { console.log('SKIPPED: jsdom is not installed (npm install jsdom)'); process.exit(2); }
const file = process.argv[2];
const htmlText = fs.readFileSync(file, 'utf8');
let failed = 0;
const ok = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); if (!c) failed++; };
const wait = ms => new Promise(r => setTimeout(r, ms));

function open(seed) {
  const errors = [], vc = new VirtualConsole();
  vc.on('jsdomError', e => errors.push(String(e.message || e)));
  vc.on('error', e => errors.push(String(e)));
  const dom = new JSDOM(htmlText, {
    runScripts: 'dangerously', url: 'https://textbook.test/chapter.html', virtualConsole: vc, pretendToBeVisual: true,
    beforeParse(w) { w.confirm = () => true; w.alert = () => {}; if (seed) for (const [k, v] of Object.entries(seed)) w.localStorage.setItem(k, v); }
  });
  return { dom, w: dom.window, d: dom.window.document, errors };
}
const { w, d, errors } = open();
const key = d.body.getAttribute('data-chapter-key');
const q = s => d.querySelector(s), qa = s => [...d.querySelectorAll(s)];
const fire = (el, t) => el.dispatchEvent(new w.Event(t, { bubbles: true }));

ok(errors.length === 0, 'page scripts ran without errors' + (errors.length ? ': ' + errors[0] : ''));
const ex = qa('.exercise');
ok(ex.length > 0, `found ${ex.length} exercise cards`);
ok(qa('textarea.note').length === ex.length, 'every exercise has a notes box');
ok(qa('select.status-sel').length === ex.length, 'every exercise has a status selector');
ok(qa('details.solution').length === ex.length, 'every exercise has a solution section');
ok(/0\/\d+ solved/.test(q('#progress-text').textContent), 'progress starts at zero: ' + q('#progress-text').textContent);

// notes + status persist
const ta = q('textarea.note'); ta.value = 'my invariant: window valid after repair'; fire(ta, 'input');
const sel = q('select.status-sel'); sel.value = 'solved'; fire(sel, 'change');
ok(/^1\/\d+ solved/.test(q('#progress-text').textContent), 'status change updates progress: ' + q('#progress-text').textContent);
const lessonBox = q('.lesson-done input'); if (lessonBox) { lessonBox.checked = true; fire(lessonBox, 'change'); }
const cn = q('#chapter-notes'); cn.value = 'revisit negative-number sums'; fire(cn, 'input');
await wait(450);
const saved = w.localStorage.getItem(key);
ok(!!saved && saved.includes('my invariant') && saved.includes('revisit negative'), 'notes saved to localStorage');

// reload with the saved state in a fresh page
const again = open({ [key]: saved });
ok(again.d.querySelector('textarea.note').value.startsWith('my invariant'), 'notes restored after reload');
ok(again.d.querySelector('select.status-sel').value === 'solved', 'status restored after reload');
ok(again.d.querySelector('#chapter-notes').value.includes('negative'), 'chapter notes restored after reload');

// export markdown (capture the Blob)
let captured = '';
w.Blob = function (parts) { captured = parts.join(''); };
w.URL.createObjectURL = () => 'blob:x'; w.URL.revokeObjectURL = () => {};
q('#export-md').click();
ok(captured.includes('# My notes') && captured.includes('my invariant') && captured.includes('Solved'), 'export produces Markdown with notes and status');
captured = ''; q('#export-json').click();
ok(captured.includes('"notes"'), 'backup JSON export works');

// trace player
const tr = q('.trace');
if (tr) {
  const data = JSON.parse(tr.getAttribute('data-trace'));
  const next = tr.querySelector('[data-a=next]'), ct = tr.querySelector('.ct');
  ok(ct.textContent.startsWith('Step 1 /'), 'trace player starts at step 1');
  next.click(); next.click();
  ok(ct.textContent.startsWith('Step 3 /'), 'Next advances the trace');
  tr.querySelector('[data-a=prev]').click();
  ok(ct.textContent.startsWith('Step 2 /'), 'Back rewinds the trace');
  if (!data.type) {
    for (let i = 0; i < data.steps.length; i++) next.click();
    ok(ct.textContent.startsWith('Step ' + data.steps.length), 'trace stops at the last step');
    if (data.pointers.includes('left') && data.pointers.includes('right')) ok(tr.querySelectorAll('.tp-cell.in').length >= 1, 'window cells are highlighted');
    else ok([...tr.querySelectorAll('.tp-ptr')].some(e => e.textContent.trim()), 'pointer labels are shown on cells');
  }
  tr.querySelector('[data-a=reset]').click();
  ok(ct.textContent.startsWith('Step 1 /'), 'Reset returns to step 1');
}
// schedule player + quiz, when present
const sch = qa('.trace').find(t => JSON.parse(t.getAttribute('data-trace')).type === 'schedule');
if (sch) {
  const rows = sch.querySelectorAll('tbody tr');
  ok(rows[rows.length - 1].classList.contains('ph'), 'schedule hides future steps');
  const rv = sch.querySelector('[data-a=reveal]');
  if (rv) { const box = sch.querySelector('.reveal-box'); ok(box.hidden, 'outcome hidden until revealed'); rv.click(); ok(!box.hidden, 'Reveal outcome shows the answer'); }
}
const quiz = q('.quiz');
if (quiz) {
  const opts = quiz.querySelectorAll('.opt'); opts[0].click();
  ok(quiz.querySelector('.why') && !quiz.querySelector('.why').hidden, 'quiz shows an explanation after answering');
  ok(quiz.querySelectorAll('.opt.right').length === 1, 'quiz marks exactly one correct option');
}
// search
const s = q('#search'); s.value = 'invariant'; fire(s, 'input');
ok(qa('#search-results a').length >= 1, 'search finds matches for "invariant"');
ok(!!q('#search-index') && !qa('[data-search]').length, 'search reads the build-time index, not the live page text');
// backup export carries chapter key and schema; import validates them
captured = ''; q('#export-json').click();
const backup = JSON.parse(captured);
ok(backup.schema === 2 && backup.chapterKey === key && backup.data && backup.data.notes, 'backup JSON records schema version and chapter key');
async function tryImport(obj, { confirmAnswer = true, seed } = {}) {
  const page = open(seed); const alerts = [];
  page.w.alert = m => alerts.push(m); page.w.confirm = () => confirmAnswer;
  const input = page.d.querySelector('#import-json');
  const file = new page.w.File([JSON.stringify(obj)], 'b.json', { type: 'application/json' });
  Object.defineProperty(input, 'files', { value: [file], configurable: true });
  input.dispatchEvent(new page.w.Event('change', { bubbles: true }));
  await wait(150);
  return { alerts, ta: page.d.querySelector('textarea.note').value, w: page.w };
}
let r = await tryImport(backup);
ok(r.alerts.some(a => /imported/i.test(a)) && r.ta.startsWith('my invariant'), 'import of a matching backup restores notes');
r = await tryImport({ ...backup, chapterKey: 'dsa:chapter-99', chapterTitle: 'Chapter 99: Other' });
ok(r.alerts.some(a => /different chapter/i.test(a)) && r.ta === '', 'import of another chapter is refused and changes nothing');
r = await tryImport({ ...backup, schema: 9 });
ok(r.alerts.some(a => /unsupported/i.test(a)) && r.ta === '', 'import of an unsupported-format backup is refused');
r = await tryImport(backup.data);
ok(r.alerts.some(a => /not a notes backup/i.test(a)) && r.ta === '', 'bare data without schema/chapter envelope is refused (strict policy)');
r = await tryImport({ ...backup, schema: undefined });
ok(r.alerts.some(a => /not a notes backup/i.test(a)) && r.ta === '', 'backup with missing schema is refused');
r = await tryImport(backup, { confirmAnswer: false, seed: { [key]: JSON.stringify({ v: 2, notes: { [ex[0].getAttribute('data-id')]: { text: 'existing', ts: 1 } }, status: {}, lessons: {}, quiz: {}, chapter: { text: '', ts: 0 } }) } });
ok(r.ta === 'existing', 'replacing existing notes can be declined and changes nothing');
r = await tryImport({ hello: 'world' });
ok(r.alerts.some(a => /not a notes backup/i.test(a)), 'unrelated JSON is rejected');
ok(!!again.d.querySelector('#import-json'), 'import control exists');
// reset
q('#reset-all').click(); await wait(10);
ok(q('textarea.note').value === '', 'reset clears notes');
console.log(failed ? `\n${failed} check(s) failed` : '\nall checks passed');
process.exit(failed ? 1 : 0);
