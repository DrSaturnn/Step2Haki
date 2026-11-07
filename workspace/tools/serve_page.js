// serve_page: a static HTTP server for a built page's folder (s164c), so the page can fetch search.json beside it and
// register the offline worker sw.js (s165). srv.use(PAGE2) switches the served page and its folder (a newer build).
//   const { serve } = require('./serve_page'); const srv = await serve(PAGE); url = srv.url + '?axall'
'use strict';
const http = require('http');
const fs = require('fs');
const path = require('path');

function serve(file) {
  let dir, name;
  const use = f => { dir = path.dirname(path.resolve(f)); name = path.basename(f); };
  use(file);
  const srv = http.createServer((req, res) => {
    const u = decodeURIComponent(req.url.split('?')[0]);
    const p = u === '/' || u === '/index.html' ? path.join(dir, name) : path.join(dir, u);
    if (!p.startsWith(dir) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); res.end(); return; }
    const TYPES = { '.html': 'text/html; charset=utf-8', '.json': 'application/json', '.js': 'text/javascript; charset=utf-8',
      '.webmanifest': 'application/manifest+json', '.png': 'image/png' };
    const type = TYPES[path.extname(p)] || 'application/octet-stream';
    res.writeHead(200, { 'content-type': type });
    fs.createReadStream(p).pipe(res);
  });
  return new Promise(r => srv.listen(0, '127.0.0.1', () => { srv.url = 'http://127.0.0.1:' + srv.address().port + '/'; srv.use = use; r(srv); }));
}
module.exports = { serve };
