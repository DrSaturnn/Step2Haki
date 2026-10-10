"""fetch: the only writer of the web source cache (plan 0.6). Agents give URLs; this script fetches and stores.

  python3 tools/spine/fetch.py <url> [<url> ...]          fetch and cache; prints sha, domain, title, size
  python3 tools/spine/fetch.py --list                      list the cache

Cache: repair/sources/web/<sha>.txt (page text, one block per line) plus repair/sources/web/index.json
(url, sha, domain, title, fetched date, chars). Local-only (repair/sources/), never committed.

Only allowlisted domains are fetched. A domain that refuses scripted access (a CAPTCHA or bot challenge, an
access-denied page: NCBI Bookshelf/StatPearls and cdc.gov did on 2026-10-10) is reported and NOT worked around;
for those, a fact may still be cited from a WebFetch reading, but it is stored by quote_check as via=relayed
(model-processed text, lower trust) and the auditor checks it; prefer a directly fetched source that says the same.
"""
import datetime
import hashlib
import html as H
import json
import os
import re
import sys
from urllib.parse import urlparse

import requests

WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CACHE = os.path.join(WS, 'repair', 'sources', 'web')
ALLOW = ('msdmanuals.com', 'merckmanuals.com', 'uspreventiveservicestaskforce.org', 'aafp.org', 'psychdb.com',
         'dailymed.nlm.nih.gov', 'accessdata.fda.gov', 'fda.gov', 'aap.org', 'publications.aap.org', 'acog.org',
         'ahajournals.org', 'acc.org', 'idsociety.org', 'diabetesjournals.org', 'goldcopd.org', 'nih.gov',
         'niaaa.nih.gov', 'nida.nih.gov', 'ncbi.nlm.nih.gov', 'cdc.gov', 'who.int', 'kdigo.org', 'heart.org')
BLOCK = re.compile(r'captcha|access denied|are you a robot|unusual traffic|enable javascript and cookies', re.I)


def allowed(host):
    return any(host == d or host.endswith('.' + d) for d in ALLOW)


def page_text(raw):
    t = re.sub(r'<(script|style|noscript|svg)\b.*?</\1>', ' ', raw, flags=re.S | re.I)
    t = re.sub(r'<(br|/p|/div|/li|/h[1-6]|/tr|/td|/th|/caption|/section|/article)\b[^>]*>', '\n', t, flags=re.I)
    # strip only real tags: a bare "<" in text ("FEV1/FVC < 0.70") must survive (COPD golden, 2026-10-10)
    t = H.unescape(re.sub(r'</?[A-Za-z!][^<>]*>', ' ', t))
    lines = [' '.join(l.split()) for l in t.split('\n')]
    return '\n'.join(l for l in lines if l)


def load_index():
    """index.json is rebuilt from one <sha>.json sidecar per page, so parallel fetches cannot drop each
    other's rows (two goldens lost entries to a read-modify-write race on 2026-10-10)."""
    ix = {}
    p = os.path.join(CACHE, 'index.json')
    if os.path.exists(p):
        try:
            ix.update(json.load(open(p, encoding='utf-8')))
        except ValueError:
            pass
    if os.path.isdir(CACHE):
        for f in os.listdir(CACHE):
            if f.endswith('.json') and f != 'index.json':
                try:
                    ix[f[:-5]] = json.load(open(os.path.join(CACHE, f), encoding='utf-8'))
                except ValueError:
                    pass
    return ix


def save_index(ix):
    p = os.path.join(CACHE, 'index.json')
    tmp = '%s.%d.tmp' % (p, os.getpid())
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(ix, f, indent=1, ensure_ascii=False)
    os.replace(tmp, p)


def fetch(url, ix):
    host = urlparse(url).hostname or ''
    if not allowed(host):
        return 'REFUSED %s: domain not on the allowlist (the Lead may add it)' % host
    try:
        r = requests.get(url, timeout=40, headers={'User-Agent': 'Mozilla/5.0 (Step2Haki source check)'})
    except requests.RequestException as e:
        return 'FAILED %s: %s' % (url, e)
    raw = r.text
    if r.status_code != 200 or BLOCK.search(raw[:4000]):
        return 'BLOCKED %s: HTTP %d%s; not worked around (use a directly fetched source, or a relayed reading)' % (
            url, r.status_code, ', bot check' if BLOCK.search(raw[:4000]) else '')
    text = page_text(raw)
    if len(text) < 500:
        return 'EMPTY %s: %d characters of text (scripted page?)' % (url, len(text))
    sha = hashlib.sha1(text.encode()).hexdigest()[:16]
    os.makedirs(CACHE, exist_ok=True)
    with open(os.path.join(CACHE, sha + '.txt'), 'w', encoding='utf-8') as f:
        f.write(text)
    title = (re.search(r'<title[^>]*>(.*?)</title>', raw, re.S | re.I) or [None, ''])[1]
    ix[sha] = {'url': url, 'domain': host, 'title': ' '.join(H.unescape(title).split())[:160],
               'fetched': datetime.date.today().isoformat(), 'chars': len(text)}
    with open(os.path.join(CACHE, sha + '.json'), 'w', encoding='utf-8') as f:   # the sidecar is the record
        json.dump(ix[sha], f, ensure_ascii=False)
    return 'OK %s %s %s (%d chars)' % (sha, host, ix[sha]['title'][:70], len(text))


def main(argv):
    ix = load_index()
    if not argv or argv == ['--list']:
        for sha, e in sorted(ix.items(), key=lambda kv: kv[1]['fetched']):
            print(sha, e['fetched'], e['domain'], e['title'][:70])
        return 0
    bad = 0
    for url in argv:
        msg = fetch(url, ix)
        bad += not msg.startswith('OK')
        print(msg)
    save_index(ix)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
