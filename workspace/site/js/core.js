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
  var AX = { module: module, on: on, off: off, emit: emit, teardown: teardown, modules: mods };
  return AX;
})();
