#!/usr/bin/env python3
"""ship_times.py: the step table of one ship.sh run.

  python3 tools/ship_times.py TIMES.tsv BATCH START EXIT [MODE] [UI_GATE_OUTPUT]

TIMES.tsv holds one line per step (name, start, end; epoch seconds) written by ship.sh's tm. Prints one line with the
wall time and every step of 1 s or more, and writes local/<batch>/ship_times.json: the steps, the ui_gate tests with the
seconds ui_gate printed for each, the wall time, the mode, the exit code and whether stamps were off. The time between
the last closed step and the exit is listed as "(after last step)", so the steps always sum to the wall time.
"""
import json
import os
import re
import sys
import time

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def table(tsv, start, end):
    steps = []
    for line in open(tsv, encoding='utf-8').read().splitlines():
        name, a, b = line.split('\t')
        steps.append({'step': name, 'seconds': round(float(b) - float(a), 1)})
    last = start + sum(s['seconds'] for s in steps)
    if end - last >= 0.05:
        steps.append({'step': '(after last step)', 'seconds': round(end - last, 1)})
    return steps


def ui_tests(path):
    out = []
    if path and os.path.exists(path):
        for line in open(path, encoding='utf-8').read().splitlines():
            m = re.match(r'(parity|theme|a11y|perf|twopane)\s+(PASS|FAIL)\b.*?(?:\((\d+) s\))?$', line)
            if m:
                out.append({'test': m.group(1), 'verdict': m.group(2), 'seconds': int(m.group(3)) if m.group(3) else 0,
                            'ran': bool(m.group(3))})
    return out


def main(a):
    tsv, batch, start, rc = a[0], a[1], float(a[2]), int(a[3])
    mode = a[4] if len(a) > 4 and a[4] else 'ship'
    end = time.time()
    steps = table(tsv, start, end)
    rec = {'batch': batch, 'mode': mode, 'date': time.strftime('%Y-%m-%d %H:%M'), 'exit': rc,
           'stamps': 'off' if os.environ.get('AX_STAMPS', '').lower() in ('off', '0', 'no', 'false') else 'on',
           'wall_seconds': round(end - start, 1), 'steps': steps, 'ui_gate': ui_tests(a[5] if len(a) > 5 else None)}
    d = os.path.join(WS, 'local', batch)
    os.makedirs(d, exist_ok=True)
    json.dump(rec, open(os.path.join(d, 'ship_times.json'), 'w', encoding='utf-8'), indent=1)
    shown = ', '.join('%s %d' % (s['step'], round(s['seconds'])) for s in steps if s['seconds'] >= 1)
    print('times: %d s (%s); steps in s: %s' % (round(rec['wall_seconds']), mode, shown or 'none over 1'))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
