(function () {
  'use strict';
  var KEY = document.body.getAttribute('data-chapter-key') || 'dsa-chapter';
  var TITLE = document.body.getAttribute('data-chapter-title') || document.title;
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function rich(s) { return esc(s).replace(/`([^`]+)`/g, '<code>$1</code>'); }

  /* ---------- storage ---------- */
  var storageOK = true, state = null;
  try { var t = KEY + ':probe'; localStorage.setItem(t, '1'); localStorage.removeItem(t); } catch (e) { storageOK = false; }
  var SCHEMA = 2;
  function blank() { return { v: SCHEMA, notes: {}, status: {}, lessons: {}, quiz: {}, chapter: { text: '', ts: 0 } }; }
  function normalize(s) {
    var b = blank(); s = s && typeof s === 'object' ? s : {};
    ['notes', 'status', 'lessons', 'quiz'].forEach(function (k) { b[k] = s[k] && typeof s[k] === 'object' ? s[k] : {}; });
    b.chapter = s.chapter && typeof s.chapter === 'object' ? { text: String(s.chapter.text || ''), ts: s.chapter.ts || 0 } : { text: '', ts: 0 };
    return b;
  }
  try { state = normalize(JSON.parse(localStorage.getItem(KEY) || 'null')); } catch (e) { state = blank(); }
  var timer = null;
  function save() {
    clearTimeout(timer);
    timer = setTimeout(function () {
      try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { storageOK = false; banner(); }
    }, 250);
  }
  function banner() {
    if ($('.banner')) return;
    var b = document.createElement('div'); b.className = 'banner';
    b.textContent = 'This browser is blocking local storage, so notes will not survive a reload. Use "Export notes" or "Copy notes" before you close the page.';
    var m = $('main'); m.insertBefore(b, m.firstChild);
  }
  if (!storageOK) banner();

  /* ---------- theme ---------- */
  var root = document.documentElement;
  try { var th = localStorage.getItem('dsa:theme'); if (th) root.setAttribute('data-theme', th); } catch (e) {}
  var themeBtn = $('#theme-toggle');
  if (themeBtn) themeBtn.addEventListener('click', function () {
    var cur = root.getAttribute('data-theme'), next = cur === 'dark' ? 'light' : cur === 'light' ? '' : 'dark';
    if (next) root.setAttribute('data-theme', next); else root.removeAttribute('data-theme');
    try { localStorage.setItem('dsa:theme', next); } catch (e) {}
  });

  /* ---------- notes, status, progress ---------- */
  function stamp(el, ts) { if (el) el.textContent = ts ? 'saved ' + new Date(ts).toLocaleString() : ''; }
  function progress() {
    var ex = $$('.exercise'), solved = ex.filter(function (e) { return state.status[e.getAttribute('data-id')] === 'solved'; }).length;
    var ls = $$('.lesson-done input'), done = ls.filter(function (i) { return state.lessons[i.getAttribute('data-id')]; }).length;
    var total = ex.length + ls.length, got = solved + done;
    var bar = $('#progress-bar'), txt = $('#progress-text');
    if (bar) bar.style.width = (total ? Math.round(100 * got / total) : 0) + '%';
    if (txt) txt.textContent = solved + '/' + ex.length + ' solved \u00b7 ' + done + '/' + ls.length + ' lessons';
    $$('nav.side a[data-lesson]').forEach(function (a) { a.classList.toggle('done', !!state.lessons[a.getAttribute('data-lesson')]); });
  }
  function applyState() {
    $$('textarea.note').forEach(function (ta) {
      var id = ta.getAttribute('data-id'), n = state.notes[id];
      ta.value = n ? n.text : '';
      stamp(ta.parentNode.querySelector('.saved'), n && n.text ? n.ts : 0);
    });
    $$('select.status-sel').forEach(function (s) {
      var v = state.status[s.getAttribute('data-id')] || 'new'; s.value = v; s.setAttribute('data-v', v);
    });
    $$('.lesson-done input').forEach(function (i) { i.checked = !!state.lessons[i.getAttribute('data-id')]; });
    var cn = $('#chapter-notes'); if (cn) { cn.value = state.chapter.text || ''; stamp($('#chapter-saved'), state.chapter.text ? state.chapter.ts : 0); }
    $$('.quiz').forEach(function (q) { if (q._restore) q._restore(); });
    progress();
  }
  document.addEventListener('input', function (e) {
    var t = e.target;
    if (t.matches && t.matches('textarea.note')) {
      var id = t.getAttribute('data-id'), ts = Date.now();
      if (t.value) state.notes[id] = { text: t.value, ts: ts }; else delete state.notes[id];
      stamp(t.parentNode.querySelector('.saved'), t.value ? ts : 0); save();
    } else if (t.id === 'chapter-notes') {
      state.chapter = { text: t.value, ts: Date.now() }; stamp($('#chapter-saved'), t.value ? state.chapter.ts : 0); save();
    }
  });
  document.addEventListener('change', function (e) {
    var t = e.target;
    if (t.matches && t.matches('select.status-sel')) {
      var v = t.value; t.setAttribute('data-v', v);
      if (v === 'new') delete state.status[t.getAttribute('data-id')]; else state.status[t.getAttribute('data-id')] = v;
      save(); progress();
    } else if (t.matches && t.matches('.lesson-done input')) {
      if (t.checked) state.lessons[t.getAttribute('data-id')] = true; else delete state.lessons[t.getAttribute('data-id')];
      save(); progress();
    }
  });
  document.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('button.clear-note') : null;
    if (!b) return;
    var ta = $('textarea.note[data-id="' + b.getAttribute('data-id') + '"]');
    if (ta && ta.value && !confirm('Clear the notes for this exercise?')) return;
    if (ta) { ta.value = ''; ta.dispatchEvent(new Event('input', { bubbles: true })); }
  });

  /* ---------- code copy ---------- */
  function copyText(text, done) {
    function fallback() {
      var ta = document.createElement('textarea'); ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); } catch (e) {} ta.remove(); done();
    }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, fallback); else fallback();
  }
  $$('pre.code').forEach(function (pre) {
    var b = document.createElement('button'); b.type = 'button'; b.className = 'copy'; b.textContent = 'Copy';
    b.addEventListener('click', function () { copyText($('code', pre).textContent, function () { b.textContent = 'Copied'; setTimeout(function () { b.textContent = 'Copy'; }, 1200); }); });
    pre.appendChild(b);
  });

  /* ---------- trace players ---------- */
  function controller(el, n, draw) {
    var i = 0, playing = null, ct = $('.ct', el);
    function show() { draw(i); if (ct) ct.textContent = 'Step ' + (i + 1) + ' / ' + n; }
    function go(k) { i = Math.max(0, Math.min(n - 1, k)); show(); }
    function stop() { if (playing) { clearInterval(playing); playing = null; var p = $('[data-a=play]', el); if (p) p.textContent = 'Play'; } }
    el.setAttribute('tabindex', '0');
    el.addEventListener('click', function (e) {
      var a = e.target.getAttribute && e.target.getAttribute('data-a'); if (!a) return;
      if (a === 'next') { stop(); go(i + 1); } else if (a === 'prev') { stop(); go(i - 1); } else if (a === 'reset') { stop(); go(0); }
      else if (a === 'play') {
        if (playing) { stop(); return; }
        if (i >= n - 1) go(0);
        e.target.textContent = 'Pause';
        playing = setInterval(function () { if (i >= n - 1) stop(); else go(i + 1); }, 900);
      }
    });
    el.addEventListener('keydown', function (e) {
      if (e.target !== el) return;
      if (e.key === 'ArrowRight') { e.preventDefault(); stop(); go(i + 1); } else if (e.key === 'ArrowLeft') { e.preventDefault(); stop(); go(i - 1); }
    });
    show();
    return { go: go };
  }
  var CTL = '<div class="tp-ctl"><button type="button" data-a="reset">Reset</button><button type="button" data-a="prev">Back</button><button type="button" class="primary" data-a="next">Next</button><button type="button" data-a="play">Play</button><span class="ct"></span></div>';
  function mountArray(el, d) {
    el.innerHTML = '<div class="tp-label">Step through the trace (arrow keys work too)</div><div class="tp-cells"></div><div class="tp-vars"></div><div class="tp-note" aria-live="polite"></div>' + CTL;
    var box = $('.tp-cells', el);
    d.cells.forEach(function (v, k) {
      var c = document.createElement('div'); c.className = 'tp-cell';
      c.innerHTML = '<span class="tp-idx">' + k + '</span><span class="tp-val"></span><span class="tp-ptr"></span>';
      $('.tp-val', c).textContent = v; box.appendChild(c);
    });
    controller(el, d.steps.length, function (i) {
      var s = d.steps[i], at = s.at || {};
      $$('.tp-cell', el).forEach(function (c, k) {
        c.classList.toggle('in', 'left' in at && 'right' in at && at.left <= k && k <= at.right);
        $('.tp-ptr', c).textContent = Object.keys(at).filter(function (n) { return at[n] === k; }).join(' ');
      });
      var vars = $('.tp-vars', el); vars.innerHTML = '';
      Object.keys(s.vars || {}).forEach(function (k) { var c = document.createElement('span'); c.className = 'chip'; c.textContent = k + ' = ' + s.vars[k]; vars.appendChild(c); });
      $('.tp-note', el).textContent = s.note || '';
    });
  }
  function mountSchedule(el, d) {
    var head = '<tr>' + d.lanes.map(function (l) { return '<th>' + esc(l) + '</th>'; }).join('') + '<th>' + esc(d.sharedLabel || 'Shared value') + '</th></tr>';
    var rows = d.steps.map(function (s) {
      return '<tr>' + d.lanes.map(function (_, li) { return '<td>' + (s.lane === li ? '<code>' + esc(s.text) + '</code>' : '') + '</td>'; }).join('') + '<td>' + (s.shared === undefined ? '' : '<code>' + esc(s.shared) + '</code>') + '</td></tr>';
    }).join('');
    el.innerHTML = '<div class="tp-label">Replay the schedule one operation at a time</div>' +
      (d.question ? '<p class="q"><strong>Predict first:</strong> ' + rich(d.question) + '</p>' : '') +
      '<div class="tablewrap"><table class="sched"><thead>' + head + '</thead><tbody>' + rows + '</tbody></table></div><div class="tp-note" aria-live="polite"></div>' + CTL +
      (d.answer ? '<div class="row"><button type="button" data-a="reveal">Reveal outcome</button></div><div class="reveal-box" hidden>' + rich(d.answer) + '</div>' : '');
    var trs = $$('tbody tr', el);
    controller(el, d.steps.length, function (i) {
      trs.forEach(function (tr, k) { tr.classList.toggle('ph', k > i); tr.classList.toggle('cur', k === i); });
      $('.tp-note', el).textContent = d.steps[i].note || '';
    });
    var rv = $('[data-a=reveal]', el);
    if (rv) rv.addEventListener('click', function () { $('.reveal-box', el).hidden = false; });
  }
  $$('.trace').forEach(function (el) {
    try { var d = JSON.parse(el.getAttribute('data-trace')); if (d.type === 'schedule') mountSchedule(el, d); else mountArray(el, d); }
    catch (err) { el.textContent = 'This trace could not be displayed.'; }
  });

  /* ---------- quizzes ---------- */
  $$('.quiz').forEach(function (el) {
    var qs; try { qs = JSON.parse(el.getAttribute('data-quiz')); } catch (e) { el.textContent = 'This quiz could not be displayed.'; return; }
    if (!Array.isArray(qs)) qs = [qs];
    var base = el.getAttribute('data-qid'), restorers = [];
    qs.forEach(function (q, qi) {
      var id = q.id ? 'qz.' + q.id : base + '.' + qi, box = document.createElement('div');
      box.innerHTML = '<p class="q">' + rich(q.q) + '</p><div class="opts"></div><div class="why" hidden></div>';
      var opts = $('.opts', box), why = $('.why', box), btns = [];
      q.options.forEach(function (o, oi) {
        var b = document.createElement('button'); b.type = 'button'; b.className = 'opt'; b.innerHTML = rich(o);
        b.addEventListener('click', function () { choose(oi, false); }); opts.appendChild(b); btns.push(b);
      });
      function choose(oi, restoring) {
        btns.forEach(function (b, k) { b.classList.toggle('right', k === q.answer); b.classList.toggle('wrong', k === oi && oi !== q.answer); });
        why.hidden = false; why.innerHTML = (oi === q.answer ? '<strong>Correct.</strong> ' : '<strong>Not quite.</strong> ') + rich(q.explain || '');
        if (!restoring) { state.quiz[id] = oi; save(); }
      }
      restorers.push(function () {
        btns.forEach(function (b) { b.classList.remove('right', 'wrong'); }); why.hidden = true;
        if (state.quiz[id] !== undefined) choose(state.quiz[id], true);
      });
      el.appendChild(box);
    });
    el._restore = function () { restorers.forEach(function (r) { r(); }); };
  });

  /* ---------- search ---------- */
  var inp = $('#search'), out = $('#search-results');
  if (inp && out) {
    var docs = [];
    try { docs = JSON.parse(($('#search-index') || { textContent: '[]' }).textContent); } catch (e) { docs = []; }
    inp.addEventListener('input', function () {
      var q = inp.value.trim().toLowerCase(); out.innerHTML = ''; if (q.length < 2) return;
      var n = 0;
      docs.forEach(function (d) {
        var p = d.text.toLowerCase().indexOf(q); if (p < 0 || n >= 12) return; n++;
        var a = document.createElement('a'); a.href = '#' + d.id;
        var b = document.createElement('b'); b.textContent = d.title; a.appendChild(b);
        var s = Math.max(0, p - 45), e = Math.min(d.text.length, p + q.length + 70), sp = document.createElement('span');
        sp.appendChild(document.createTextNode((s ? '\u2026' : '') + d.text.slice(s, p)));
        var m = document.createElement('mark'); m.textContent = d.text.slice(p, p + q.length); sp.appendChild(m);
        sp.appendChild(document.createTextNode(d.text.slice(p + q.length, e) + (e < d.text.length ? '\u2026' : '')));
        a.appendChild(sp); a.addEventListener('click', function () { document.body.classList.remove('nav-open'); }); out.appendChild(a);
      });
      if (!n) out.textContent = 'No matches.';
    });
  }

  /* ---------- export / import / reset ---------- */
  var STAT = { solved: 'Solved', attempted: 'Attempted', revisit: 'Needs review', new: 'Not started' };
  function notesMarkdown() {
    var L = ['# My notes: ' + TITLE, '', 'Exported ' + new Date().toLocaleString(), ''];
    $$('section.lesson').forEach(function (sec) {
      var items = [];
      $$('.exercise', sec).forEach(function (ex) {
        var id = ex.getAttribute('data-id'), n = state.notes[id], st = state.status[id];
        if (!n && !st) return;
        items.push('### ' + $('h4', ex).textContent + ' (' + STAT[st || 'new'] + ')', '', n ? n.text : '_No notes._', '');
      });
      if (items.length || state.lessons[sec.id]) {
        L.push('## ' + $('h2', sec).textContent + (state.lessons[sec.id] ? ' (lesson marked complete)' : ''), '');
        L = L.concat(items);
      }
    });
    if (state.chapter.text) L.push('## Chapter notes', '', state.chapter.text, '');
    return L.join('\n');
  }
  function download(name, text, type) {
    var b = new Blob([text], { type: type }), a = document.createElement('a');
    a.href = URL.createObjectURL(b); a.download = name; document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }
  function slug() { return KEY.replace(/[^a-z0-9]+/gi, '-'); }
  function on(id, fn) { var b = $(id); if (b) b.addEventListener('click', fn); }
  on('#export-md', function () { download(slug() + '-notes.md', notesMarkdown(), 'text/markdown'); });
  function backupFile() { return { schema: SCHEMA, chapterKey: KEY, chapterTitle: TITLE, exported: new Date().toISOString(), data: state }; }
  on('#export-json', function () { download(slug() + '-backup.json', JSON.stringify(backupFile(), null, 1), 'application/json'); });
  on('#copy-notes', function (e) { var b = e.target; copyText(notesMarkdown(), function () { b.textContent = 'Copied'; setTimeout(function () { b.textContent = 'Copy notes'; }, 1200); }); });
  var imp = $('#import-json');
  if (imp) imp.addEventListener('change', function () {
    var f = imp.files && imp.files[0]; if (!f) return;
    var r = new FileReader();
    r.onload = function () {
      imp.value = '';
      var o;
      try { o = JSON.parse(r.result); } catch (e) { alert('That file is not valid JSON, so it cannot be a notes backup.'); return; }
      if (!o || typeof o !== 'object' || o.schema === undefined || !o.data || typeof o.data !== 'object') { alert('That file is not a notes backup for this textbook (missing schema or data).'); return; }
      if (o.schema !== SCHEMA) { alert('Unsupported backup format (' + o.schema + '). This textbook reads format ' + SCHEMA + '.'); return; }
      if (o.chapterKey !== KEY) {
        alert('This backup belongs to a different chapter (' + (o.chapterTitle || o.chapterKey || 'unknown') + '), so it was not imported. Open that chapter and import it there.');
        return;
      }
      var data = o.data;
      var have = Object.keys(state.notes).length || Object.keys(state.status).length || Object.keys(state.lessons).length || state.chapter.text;
      if (have && !confirm('Importing replaces the notes and progress currently saved for this chapter. Continue?')) return;
      state = normalize(data); save(); applyState(); alert('Backup imported.');
    };
    r.readAsText(f);
  });
  on('#reset-all', function () {
    if (!confirm('Erase all notes, statuses and progress for this chapter? Export a backup first if unsure.')) return;
    state = blank(); save(); applyState();
  });

  /* ---------- chrome ---------- */
  on('#menu-btn', function () { document.body.classList.toggle('nav-open'); });
  $$('nav.side a[href^="#"]').forEach(function (a) { a.addEventListener('click', function () { document.body.classList.remove('nav-open'); }); });
  on('#print-btn', function () { window.print(); });
  window.addEventListener('beforeprint', function () { $$('details.hint').forEach(function (d) { d.open = true; }); });

  applyState();
})();
