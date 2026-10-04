#!/usr/bin/env python3
"""Build the two published pages from src/ and check their figures against their sources.

    ./publish.py                 check figures, then build dist/
    ./publish.py --check         check figures only
    ./publish.py --out DIR       build into DIR instead of dist/

dist/pitch.html   the pitch, with src/images/* inlined as data URIs, so it is
                  one self-contained file (publish it as the page itself)
dist/ask.html     the funding page, unchanged
dist/asks.json    published beside ask.html; the page fetches it by that name

A figure the pages print is checked against the file that produced it. Each
check prints OK, MISMATCH, or UNCHECKED (no local source), and the build stops
on MISMATCH or on a missing source file. UNCHECKED is not a pass: it means
nobody has wired that figure to a source yet, and the line says where it comes from.
"""
import argparse
import base64
import glob
import json
import os
import re
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'src')
PROJECTS = os.path.dirname(HERE)


def p(*parts):
    return os.path.join(PROJECTS, *parts)


# --- sources ---------------------------------------------------------------

def atlas_stats():
    return json.load(open(p('purana-atlas', 'data', 'stats.json')))['atlases']


def atlas_reached():
    return sum(a['reached'] for a in atlas_stats().values())


def atlas_recordings():
    return sum(a['recordings'] for a in atlas_stats().values())


def atlas_count():
    return len(atlas_stats())


def index_occurrences():
    # The pitch's "verses in one index" is index.db's occurrence count;
    # distinct verses (the verse table) are fewer.
    db = sqlite3.connect('file:%s?mode=ro' % p('sharadapeetham', 'build', 'index.db'), uri=True)
    return db.execute('select count(*) from occurrence').fetchone()[0]


def rv_suktas_with_word_timing():
    files = glob.glob(p('rigveda.sanatana.in', 'src', 'data', 'sync', '[0-9]*', '*.json'))
    if not files:
        raise FileNotFoundError('rigveda.sanatana.in/src/data/sync')
    return sum(1 for f in files if '"word' in open(f, encoding='utf8').read())


def rv_riks():
    return json.load(open(p('rigveda.sanatana.in', 'src', 'data', 'sync', 'summary.json')))['total_verses']


def kane_synopses():
    files = glob.glob(p('historyofdharmasastra', 'audio', 'synopsis', '**', '*.mp3'), recursive=True)
    if not files:
        raise FileNotFoundError('historyofdharmasastra/audio/synopsis')
    return len(files)


def asks_meter(ask_id):
    asks = json.load(open(os.path.join(SRC, 'asks.json'), encoding='utf8'))['asks']
    return next(a for a in asks if a['id'] == ask_id)['meter']['now']


# (page, the text as the page prints it with {} for the number, source label, function)
CHECKS = [
    ('pitch.html', '<span class="n">{}</span><span class="l">purāṇa verses', 'purana-atlas stats.json, sum of reached', atlas_reached),
    ('pitch.html', '{} verses on the clock from', 'purana-atlas stats.json, sum of reached', atlas_reached),
    ('pitch.html', 'from {} recordings', 'purana-atlas stats.json, sum of recordings', atlas_recordings),
    ('pitch.html', '>{} atlases in beta<', 'purana-atlas stats.json, number of atlases', atlas_count),
    ('pitch.html', '<span class="n">{}</span><span class="l">verses in one index', 'sharadapeetham index.db, occurrence rows', index_occurrences),
    ('pitch.html', '<span class="n">{}</span><span class="l">Ṛgveda sūktas', 'rigveda.sanatana.in sync files with word starts', rv_suktas_with_word_timing),
    ('pitch.html', 'word timing on {} sūktas', 'rigveda.sanatana.in sync files with word starts', rv_suktas_with_word_timing),
    ('pitch.html', '~{} ṛks', 'rigveda.sanatana.in sync/summary.json total_verses', rv_riks),
    ('pitch.html', '{} spoken synopses', 'historyofdharmasastra audio/synopsis mp3 files', kane_synopses),
    ('ask.html', '<span>{} verses on the clock', 'purana-atlas stats.json, sum of reached', atlas_reached),
    ('asks.json:audio', '{}', 'purana-atlas stats.json, sum of reached', atlas_reached),
    ('ask.html', 'Word timing on {} sūktas', 'rigveda.sanatana.in sync files with word starts', rv_suktas_with_word_timing),
    ('ask.html', 'Kane, with {} spoken synopses', 'historyofdharmasastra audio/synopsis mp3 files', kane_synopses),
]

# Printed figures with no local source yet. Listed so they are never mistaken for checked.
UNCHECKED = [
    ('13,772', 'Mahābhārata named entities', 'sanatana.in/mahabharata (not in a local repo)'),
    ('611', "Kane's footnotes located by their words", 'the Kane matching run; no output file found locally'),
    ('61.5 hours', 'Yajurveda audio aligned', 'NOTE-veda-shazam.md in audio-ingest'),
]


def fmt(n):
    return f'{n:,}'


def check():
    pages = {name: open(os.path.join(SRC, name), encoding='utf8').read() for name in ('pitch.html', 'ask.html')}
    bad = 0
    for page, pattern, label, fn in CHECKS:
        try:
            want = fn()
        except (FileNotFoundError, sqlite3.OperationalError, KeyError) as e:
            print(f'  SOURCE MISSING  {pattern!r} on {page}: {label} ({e})')
            bad += 1
            continue
        if page.startswith('asks.json:'):
            got = asks_meter(page.split(':', 1)[1])
            ok = got == want
            shown = f'meter.now = {got}'
        else:
            ok = pattern.format(fmt(want)) in pages[page]
            shown = 'printed' if ok else _printed(pages[page], pattern)
        print(f'  {"OK" if ok else "MISMATCH":14s}  {fmt(want):>9s}  {page}: {pattern.format("N")}   [{label}]' + ('' if ok else f'  -> {shown}'))
        bad += not ok
    for value, what, where in UNCHECKED:
        print(f'  {"UNCHECKED":14s}  {value:>9s}  {what}   [{where}]')
    return bad


def _printed(text, pattern):
    head, _, tail = pattern.partition('{}')
    m = re.search(re.escape(head) + r'([0-9][0-9,.]*)' + re.escape(tail), text)
    return f'page prints {m.group(1)}' if m else 'pattern not found on the page'


def build(out):
    os.makedirs(out, exist_ok=True)
    html = open(os.path.join(SRC, 'pitch.html'), encoding='utf8').read()

    def inline(m):
        path = os.path.join(SRC, m.group(1))
        data = base64.b64encode(open(path, 'rb').read()).decode('ascii')
        return f'src="data:image/jpeg;base64,{data}"'

    html, n = re.subn(r'src="(images/[^"]+\.jpg)"', inline, html)
    open(os.path.join(out, 'pitch.html'), 'w', encoding='utf8').write(html)
    for name in ('ask.html', 'asks.json'):
        open(os.path.join(out, name), 'w', encoding='utf8').write(open(os.path.join(SRC, name), encoding='utf8').read())
    json.load(open(os.path.join(out, 'asks.json'), encoding='utf8'))
    print(f'built {out}: pitch.html ({n} images inlined, {os.path.getsize(os.path.join(out, "pitch.html")):,} bytes), ask.html, asks.json')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true', help='check figures only, build nothing')
    ap.add_argument('--out', default=os.path.join(HERE, 'dist'))
    a = ap.parse_args()
    print('figures:')
    bad = check()
    if bad:
        print(f'{bad} figure(s) wrong or unsourced; not building.')
        return 1
    if not a.check:
        build(a.out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
