var AX = (function () {
  'use strict';
  var mods = {}, list = [], handlers = {};
  function module(name, init) {
    var m = { name: name, init: init, api: null, error: null };
    mods[name] = m; list.push(m);
    try { m.api = init(AX) || null; } catch (e) { m.error = e; if (window.console) console.error('AX module ' + name + ':', e); }
    return m.api;
  }
  function on(type, fn) { (handlers[type] = handlers[type] || []).push(fn); return function () { off(type, fn); }; }
  function off(type, fn) { var h = handlers[type]; if (h) { var i = h.indexOf(fn); if (i >= 0) h.splice(i, 1); } }
  function emit(type, detail) { (handlers[type] || []).slice().forEach(function (fn) { try { fn(detail); } catch (e) { if (window.console) console.error('AX event ' + type + ':', e); } }); }
  function teardown(name) { var m = mods[name]; if (m && m.api && typeof m.api.teardown === 'function') m.api.teardown(); }

  /* Briefs arrive in the page as <div class="brief"> shells holding a <template class="axl">. build() moves the
     template content into the shell and runs every registered per-brief pass on it, in registration order. */
  var passes = [], building = false, queue = [], recent = [], clearing = 0;
  function tpl(b) { for (var t = b && b.firstElementChild; t; t = t.nextElementSibling) if (t.tagName === 'TEMPLATE' && t.classList.contains('axl')) return t; return null; }
  function isBuilt(b) { return !!b && !tpl(b); }
  function runPasses(b, from) {
    for (var i = from || 0; i < passes.length; i++) {
      try { passes[i].fn(b); } catch (e) { if (window.console) console.error('AX pass ' + passes[i].name + ' on ' + b.id + ':', e); }
    }
  }
  function build(b) {
    var t = tpl(b); if (!t) return b;
    if (building) { if (queue.indexOf(b) < 0) queue.push(b); return b; }
    building = true;
    recent.push(b); if (!clearing) clearing = setTimeout(function () { recent = []; clearing = 0; }, 0);
    b.replaceChild(t.content, t);
    runPasses(b, 0);
    building = false;
    emit('brief:built', b);
    if (queue.length) build(queue.shift());
    return b;
  }
  function each(name, fn) {
    passes.push({ name: name, fn: fn });
    var all = document.querySelectorAll('.brief');
    for (var i = 0; i < all.length; i++) { if (tpl(all[i])) continue; try { fn(all[i]); } catch (e) { if (window.console) console.error('AX pass ' + name + ':', e); } }
  }
  function briefs() { return document.querySelectorAll('.brief'); }
  function holder(id) {
    if (!id) return null;
    var el = document.getElementById(id);
    if (el) return el.classList.contains('brief') ? el : el.closest('.brief');
    var all = document.querySelectorAll('.brief > template.axl');
    for (var i = 0; i < all.length; i++) { if (all[i].content.getElementById(id)) return all[i].parentNode; }
    return null;
  }
  function ensure(x) {
    var b = typeof x === 'string' ? holder(x) : (x && x.classList && x.classList.contains('brief') ? x : x && x.closest ? x.closest('.brief') : null);
    if (b) build(b);
    return typeof x === 'string' ? document.getElementById(x) : x;
  }
  /* true for a node a build has just placed: observers that lay out brief copies (drawers, hover cards) skip it */
  function fresh(n) { var b = n && n.closest ? n.closest('.brief') : null; return !!b && recent.indexOf(b) >= 0; }
  function content(b) { var t = tpl(b); return t ? t.content : b; }
  function pending() { return Array.prototype.map.call(document.querySelectorAll('.brief > template.axl'), function (t) { return t.parentNode; }); }
  function buildAll() { pending().forEach(build); }
  /* question types of bank items and the lead-in each type shows when an item has none of its own */
  var PROMPT = {next:'Which of the following is the most appropriate next step in management?',
                dx:'Which of the following is the most likely diagnosis?',
                test:'Which of the following is the most appropriate test?',
                mech:'Which of the following is the most likely cause, organism, or complication?',
                avoid:'Which of the following is contraindicated or should be avoided?',
                screen:'Which of the following is the most appropriate screening or preventive measure?',
                stage:'Which of the following best describes the stage or classification?',
                claim:'Which of the following statements is correct?',
                untyped:'Which of the following is correct for this patient?'};
  function qtype(t) { t = (t || '').toLowerCase(); return PROMPT[t] ? t : 'untyped'; }
  function prompt(t) { return PROMPT[qtype(t)]; }
  /* a brief's bank items: the .mcq cards of a built brief; for an unbuilt brief, the template items the build turns
     into cards (stem and answer split by an arrow, both distractors present). */
  function items(b) {
    if (isBuilt(b)) return Array.prototype.map.call(b.querySelectorAll('.mcq'), function (m) {
      var qp = m.querySelector('.qp');
      return { type: (qp && qp.dataset.type) || 'untyped', status: m.dataset.itemStatus || '' };
    });
    var out = [];
    content(b).querySelectorAll('ol.bank > li').forEach(function (li) {
      var segs = 0, cur = 0;
      li.childNodes.forEach(function (n) {
        if (n.nodeType === 3 && n.nodeValue.indexOf('\u2192') > -1) {
          n.nodeValue.split('\u2192').forEach(function (t, i) { if (i > 0) { if (cur) segs++; cur = 0; } if (t.trim()) cur = 1; });
        } else if ((n.textContent || '').trim()) cur = 1;
      });
      if (cur) segs++;
      var d1 = (li.getAttribute('data-label-d1') || li.getAttribute('data-d1') || '').trim(), d2 = (li.getAttribute('data-label-d2') || li.getAttribute('data-d2') || '').trim();
      if (segs >= 2 && d1 && d2) out.push({ type: qtype(li.getAttribute('data-type')), status: li.getAttribute('data-item-status') || '' });
    });
    return out;
  }
  /* every per-brief pass on a detached copy of a brief (search reads unbuilt briefs this way); no event, no build */
  function copy(b) {
    var root = document.createElement('div');
    for (var i = 0; i < b.attributes.length; i++) root.setAttribute(b.attributes[i].name, b.attributes[i].value);
    root.appendChild(content(b).cloneNode(true));
    runPasses(root, 0);
    return root;
  }

  /* Reader settings: one versioned record in localStorage ('ax-settings', {v, s}). VERSION goes up with a MIGRATE step
     whenever a setting is renamed or its values change, so a reader's choices carry over. Version 1 reads the earlier
     one-key-per-setting storage once; set() also writes that key, so a page cached before version 1 still reads it. */
  var settings = (function () {
    var KEY = 'ax-settings', VERSION = 1;
    var LEGACY = { study: 'ax-study', flat: 'ax-flat', shelf: 'ax-shelf', bankview: 'ax-bankview', theme: 'ax-theme', accent: 'ax-accent' };
    var MIGRATE = {
      1: function (ls) { var s = {}; for (var k in LEGACY) { var v = ls.getItem(LEGACY[k]); if (v !== null) s[k] = v; } return s; }
    };
    var rec = null;
    function ls() { try { return window.localStorage; } catch (e) { return null; } }
    function load() {
      if (rec) return rec;
      var st = ls(), r = null;
      try { r = st && JSON.parse(st.getItem(KEY) || 'null'); } catch (e) { r = null; }
      if (!r || typeof r !== 'object' || typeof r.s !== 'object') r = { v: 0, s: {} };
      for (var v = (r.v || 0) + 1; v <= VERSION; v++) {
        var add = st && MIGRATE[v] ? MIGRATE[v](st, r.s) : {};
        for (var k in add) if (!(k in r.s)) r.s[k] = add[k];
        r.v = v;
      }
      rec = r;
      try { if (st) st.setItem(KEY, JSON.stringify(r)); } catch (e) {}
      return rec;
    }
    function get(name, dflt) { var r = load(); return name in r.s ? r.s[name] : (dflt === undefined ? null : dflt); }
    function set(name, val) {
      var r = load(), st = ls(); r.s[name] = String(val);
      try { if (st) { st.setItem(KEY, JSON.stringify(r)); if (LEGACY[name]) st.setItem(LEGACY[name], String(val)); } } catch (e) {}
    }
    function remove(name) { var r = load(), st = ls(); delete r.s[name]; try { if (st) { st.setItem(KEY, JSON.stringify(r)); if (LEGACY[name]) st.removeItem(LEGACY[name]); } } catch (e) {} }
    return { get: get, set: set, remove: remove, version: VERSION };
  })();

  var AX = { module: module, on: on, off: off, emit: emit, teardown: teardown, modules: mods, settings: settings,
    brief: { each: each, build: build, ensure: ensure, isBuilt: isBuilt, content: content, fresh: fresh, holder: holder, all: briefs, pending: pending, buildAll: buildAll, copy: copy, items: items, qtype: qtype, prompt: prompt } };
  return AX;
})();
