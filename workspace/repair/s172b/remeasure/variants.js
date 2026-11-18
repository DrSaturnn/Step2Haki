// trial styles for the Two-pane options; all apply only while the sidebar is open (html.ax2-nav) unless noted
const O = 'html[data-layout="two"].ax2-nav ';
exports.css = {
  P2: O + '.ax2-cols{column-gap:28px}' + O + '.ax2-col{column-gap:28px}' + O + 'main .wrap{padding-right:20px}' + O + 'main{margin-left:calc(var(--ax2-left) - 12px)}',
  P4: O + 'main{zoom:.84}',
};
// P1 styling of the narrow sidebar (looks); width is set separately
exports.p1look = O + `#nav.axn .axn-head{padding:14px 12px 10px;gap:8px}` +
  O + `#nav.axn .axn-head > div:nth-child(2){display:none}` +
  O + `#nav.axn .axn-mark{width:34px;height:34px;font-size:14px}` +
  O + `#nav.axn .axn-srch{margin:0 10px 8px;height:34px;padding:0 10px}` +
  O + `#nav.axn .axn-srch input{font-size:13px}` +
  O + `#nav.axn .axn-shelfrow{margin:0 10px 8px;grid-template-columns:28px minmax(0,1fr) auto;gap:8px;padding:5px 10px 5px 5px}` +
  O + `#nav.axn .axn-shelfrow .ic{width:28px;height:28px}` +
  O + `#nav.axn .axn-shelfrow .v{font-size:14px}` +
  O + `#nav.axn #navscroll{padding:4px 6px 18px}` +
  O + `#axn .axn-sys{height:30px;padding:0 8px;gap:6px}` + O + `#axn .axn-sys .nm{font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}` +
  O + `#axn a.axn-b{padding:5px 8px 5px 12px;font-size:13px;line-height:17px;min-height:30px}` +
  O + `#axn a.axn-b[data-also]::before{left:3px}` +
  O + `#axn .axn-rail{padding:4px 0 6px 10px;gap:6px}` +
  O + `#axn a.axn-s{padding:0 8px;grid-template-columns:16px minmax(0,1fr) auto}` + O + `#axn a.axn-s .l{font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}`;
// set the open sidebar to W px on screen
exports.navW = async (p, W) => p.evaluate(W => {
  const nav = document.getElementById('nav'), r = nav.getBoundingClientRect().width / parseFloat(getComputedStyle(nav).width);
  const s = document.createElement('style'); s.textContent = 'html[data-layout="two"].ax2-nav #nav{width:' + (W / r) + 'px}'; document.head.appendChild(s);
}, W);
exports.apply = async (p, v) => {
  let css = (v.css || []).map(k => exports.css[k]).join('\n'); if (v.look) css += exports.p1look;
  if (css) await p.addStyleTag({ content: css });
  if (v.nav) await exports.navW(p, v.nav);
  if (v.p3) await p.evaluate(t => { window.__P3 = true; if (t) window.__P3T = t; }, v.p3t || 0);
};
