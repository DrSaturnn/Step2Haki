/* =====================================================================
   AxBx progress sync.

   Two operations — read a name's schedule, write it — over Upstash Redis
   via its REST API, so this file has NO dependencies and needs no
   package.json or npm install. A folder upload is enough.

   What is stored: which briefs a person has reviewed, the Leitner box each
   one sits in, and when it is next due. No scores, no answers, no email.

   The PIN is not security and the UI says so. It exists so that a
   classmate typing a name that already exists cannot overwrite that
   person's schedule by accident. Reads stay open.

   Environment (injected by the Vercel Marketplace integration — the KV_*
   names are the ones the old Vercel KV used, kept for compatibility, and
   UPSTASH_* are the current ones, so accept either):
     KV_REST_API_URL   / UPSTASH_REDIS_REST_URL
     KV_REST_API_TOKEN / UPSTASH_REDIS_REST_TOKEN
   ===================================================================== */

const STORE_URL   = process.env.KV_REST_API_URL   || process.env.UPSTASH_REDIS_REST_URL;
const STORE_TOKEN = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;

const ROSTER     = 'axbx:names';
const MAX_BYTES  = 64 * 1024;          // a full 152-brief schedule is ~8 KB
const MAX_NAMES  = 50;                 // a study group, not a service
const MAX_BRIEFS = 2000;               // the library is 152; this is generous
const BOXES      = [0, 1, 3, 7, 16, 35];   // must match the client's intervals

/* The day a brief was last reviewed is recoverable — its due date minus the
   interval of the box it sits in — so two devices reconcile on evidence
   rather than on who happened to write last.

   This runs on WRITE, not only on read, and that is the point. Without it the
   store is last-write-wins over the whole blob: review on a laptop, then on a
   phone that never refreshed, and the phone's stale push erases the laptop's
   work. Merging here makes the order of pushes irrelevant. */
function mergeBoxes(mine, theirs) {
  const out = Object.assign({}, mine || {});
  Object.keys(theirs || {}).forEach(k => {
    const t = theirs[k];
    if (!t || !(t.b >= 1 && t.b <= 5) || typeof t.due !== 'number') return;
    const o = out[k];
    if (!o) { out[k] = { b: t.b, due: t.due, ok: t.ok || 0, n: t.n || 0 }; return; }
    const oDay = o.due - (BOXES[o.b] || 0);
    const tDay = t.due - (BOXES[t.b] || 0);
    /* Dates are day-granular, so two reviews of the same brief on the same day
       tie. Break the tie toward the LOWER box: when the evidence is equally
       recent, trust the weaker result. Losing a pass costs one extra review;
       losing a miss leaves a gap you think you have covered. */
    const newer = tDay > oDay || (tDay === oDay && t.b < o.b);
    if (newer) out[k] = { b: t.b, due: t.due, ok: t.ok || o.ok || 0, n: t.n || o.n || 0 };
  });
  return out;
}

function slug(n) {
  return String(n || '').trim().toLowerCase().replace(/\s+/g, ' ').slice(0, 40);
}
function key(n) { return 'axbx:p:' + slug(n); }

async function redis(command) {
  if (!STORE_URL || !STORE_TOKEN) {
    const e = new Error('Storage is not configured on this deployment.');
    e.code = 'NOSTORE';
    throw e;
  }
  const r = await fetch(STORE_URL, {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + STORE_TOKEN, 'Content-Type': 'application/json' },
    body: JSON.stringify(command)
  });
  if (!r.ok) throw new Error('Storage returned ' + r.status);
  const j = await r.json();
  if (j && j.error) throw new Error(String(j.error));
  return j ? j.result : null;
}

function readJSON(raw) {
  if (!raw) return null;
  try { return typeof raw === 'string' ? JSON.parse(raw) : raw; } catch (e) { return null; }
}

/* CommonJS on purpose: this ships as a folder drag-and-drop with no
   package.json and no build step, so `export default` in a .js file would
   be ambiguous to the runtime. module.exports is unambiguous everywhere. */
module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  try {
    /* ---------- read ---------- */
    if (req.method === 'GET') {
      const name = req.query && req.query.name;
      if (!name) {
        const names = (await redis(['SMEMBERS', ROSTER])) || [];
        return res.status(200).json({ names });
      }
      const rec = readJSON(await redis(['GET', key(name)]));
      if (!rec) return res.status(200).json({ found: false });
      return res.status(200).json({
        found: true,
        name: rec.name || name,
        hasPin: !!rec.pin,
        updated: rec.updated || 0,
        data: rec.data || null
      });
    }

    /* ---------- write ---------- */
    if (req.method === 'POST') {
      const body = typeof req.body === 'string' ? readJSON(req.body) : req.body;
      if (!body || !body.name) return res.status(400).json({ error: 'A name is required.' });
      if (!slug(body.name))    return res.status(400).json({ error: 'That name is empty.' });

      const incoming = (body.data && typeof body.data === 'object') ? body.data : {};
      const box = (incoming.box && typeof incoming.box === 'object') ? incoming.box : {};
      if (Object.keys(box).length > MAX_BRIEFS) {
        return res.status(413).json({ error: 'That schedule has too many entries.' });
      }
      if (JSON.stringify(incoming).length > MAX_BYTES) {
        return res.status(413).json({ error: 'That schedule is unexpectedly large.' });
      }

      const existing = readJSON(await redis(['GET', key(body.name)]));
      const pin = body.pin ? String(body.pin).trim().slice(0, 12) : '';

      /* A roster cap is the only real brake on an open endpoint: the page is
         public, so any secret it carries is public too. This stops the store
         filling with junk names without putting a wall in front of a classmate. */
      if (!existing) {
        const count = (await redis(['SCARD', ROSTER])) || 0;
        if (count >= MAX_NAMES) {
          return res.status(429).json({
            error: 'This link already has the maximum number of profiles. Remove one to add another.'
          });
        }
      }

      /* A PIN, once set, guards later writes. Wrong PIN never destroys
         anything — it refuses, and the client keeps its local copy. */
      if (existing && existing.pin && existing.pin !== pin) {
        return res.status(403).json({
          error: 'This name has a PIN set on it. Enter the PIN to save, or choose another name.',
          needPin: true
        });
      }

      const prev = (existing && existing.data) || {};
      const merged = {
        box:  mergeBoxes(prev.box, box),
        runs: Math.max(prev.runs || 0, incoming.runs || 0),
        last: Math.max(prev.last || 0, incoming.last || 0)
      };
      const rec = {
        name: String(body.name).trim().slice(0, 40),
        pin: existing && existing.pin ? existing.pin : (pin || ''),
        data: merged,
        updated: Date.now()
      };
      await redis(['SET', key(body.name), JSON.stringify(rec)]);
      await redis(['SADD', ROSTER, rec.name]);
      /* The merged view goes back so the pusher stops being stale. */
      return res.status(200).json({ ok: true, hasPin: !!rec.pin, updated: rec.updated, data: merged });
    }

    /* ---------- remove ---------- */
    if (req.method === 'DELETE') {
      const name = (req.query && req.query.name) || '';
      if (!slug(name)) return res.status(400).json({ error: 'A name is required.' });
      const existing = readJSON(await redis(['GET', key(name)]));
      if (!existing) return res.status(200).json({ ok: true, alreadyGone: true });
      const pin = (req.query && req.query.pin) ? String(req.query.pin).trim() : '';
      if (existing.pin && existing.pin !== pin) {
        return res.status(403).json({ error: 'That name has a PIN. Enter it to remove the profile.', needPin: true });
      }
      await redis(['DEL', key(name)]);
      await redis(['SREM', ROSTER, existing.name || name]);
      return res.status(200).json({ ok: true });
    }

    res.setHeader('Allow', 'GET, POST, DELETE');
    return res.status(405).json({ error: 'Method not allowed.' });

  } catch (err) {
    /* The page treats any failure here as "offline" and carries on with its
       local copy, so the message matters more than the status. */
    const nostore = err && err.code === 'NOSTORE';
    return res.status(nostore ? 501 : 502).json({
      error: nostore
        ? 'Storage is not connected yet — add the Upstash Redis integration in Vercel.'
        : 'Could not reach storage.'
    });
  }
}
