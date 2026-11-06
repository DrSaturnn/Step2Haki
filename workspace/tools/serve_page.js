// serve_page: a static HTTP server for a built page's folder (s164c), so the page can fetch search.json beside it.
//   const { serve } = require('./serve_page'); const srv = await serve(PAGE); url = srv.url + '?axall'
'use strict';
const http = require('http');
const fs = require('fs');
const path = require('path');

function serve(file) {
  const dir = path.dirname(path.resolve(file)), name = path.basename(file);
  const srv = http.createServer((req, res) => {
    const u = decodeURIComponent(req.url.split('?')[0]);
    const p = u === '/' ? path.join(dir, name) : path.join(dir, u);
    if (!p.startsWith(dir) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); res.end(); return; }
    const type = p.endsWith('.html') ? 'text/html; charset=utf-8' : p.endsWith('.json') ? 'application/json' : 'application/octet-stream';
    res.writeHead(200, { 'content-type': type });
    fs.createReadStream(p).pipe(res);
  });
  return new Promise(r => srv.listen(0, '127.0.0.1', () => { srv.url = 'http://127.0.0.1:' + srv.address().port + '/'; r(srv); }));
}
module.exports = { serve };
