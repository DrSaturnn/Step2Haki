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

  var AX = { module: module, on: on, off: off, emit: emit, teardown: teardown, modules: mods,
    brief: { each: each, build: build, ensure: ensure, isBuilt: isBuilt, content: content, fresh: fresh, holder: holder, all: briefs, pending: pending, buildAll: buildAll } };
  return AX;
})();
