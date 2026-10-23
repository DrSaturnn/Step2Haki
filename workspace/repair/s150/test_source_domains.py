"""Offline regression for Jonathan's 2026-10-22 source-domain approval. No network calls."""
import importlib.util
from pathlib import Path

workspace = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('approved_source_fetch', workspace / 'tools/spine/fetch.py')
fetch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fetch)

approved = ('aaos.org', 'www.aaos.org', 'orthoinfo.aaos.org', 'orthoinfo.org',
            'www.orthoinfo.org', 'aapmr.org', 'now.aapmr.org', 'posna.org')
lookalikes_and_unapproved = ('evilaaos.org', 'aaos.org.evil.example', 'aapmr.org.evil.example',
                            'posna.org.evil.example', 'example.com', 'medlineplus.gov', 'evilorthoinfo.org')
existing = ('nih.gov', 'pmc.ncbi.nlm.nih.gov', 'www.aafp.org', 'www.msdmanuals.com')
for host in approved + existing:
    assert fetch.allowed(host), host
for host in lookalikes_and_unapproved:
    assert not fetch.allowed(host), host
print('19 source-domain cases passed; no network requests')
