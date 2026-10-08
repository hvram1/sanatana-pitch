#!/usr/bin/env python3
"""Draw the coverage map: the branches of Sanātana Dharma's literature, each
shaded by where our work on it stands, as an inline SVG in src/pitch.html.

    ./coverage_map.py          rewrite the map between its markers in src/pitch.html

publish.py runs this before every build, so the map is always drawn from the
data below. To move a branch from "not yet" to "beta", change its state here.

Every lit branch links to the page that shows it; a dark branch with a result on
the funding page links there instead. States:

    live      open to everyone, final
    beta      open to everyone, still being verified
    partner   built by a partner, with our technical support
    progress  being built, not yet open, or open but not yet working as intended
    none      not started
"""
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PITCH = os.path.join(HERE, 'src', 'pitch.html')
START, END = '<!-- coverage-map:start -->', '<!-- coverage-map:end -->'

ASK = 'https://claude.ai/artifact/RHAxouvYiRFwdCxdjFGxzx'   # publish.py points this at github.io in docs/
YV = 'https://hvram1.github.io/yajurveda.sanatana.in/'
RV = 'https://hvram1.github.io/rigveda.sanatana.in/'
AB = 'https://hvram1.github.io/advaitabharati.sanatanasampatti.in/'

# The Veda: one row per śākhā we hold or can name, one column per layer.
# None is a layer that śākhā does not have.
LAYERS = ['Saṃhitā', 'Brāhmaṇa', 'Āraṇyaka', 'Upaniṣad']
VEDA = [
    ('Ṛgveda', '', [
        ('beta', '10,552 ṛks', 'with Sāyaṇa', RV),
        ('beta', 'Aitareya', 'adhyāyas 1–10', RV),
        ('none', 'Aitareya', '', None),
        ('beta', 'Aitareya', 'with Śaṅkara', AB + 'aitareya/'),
    ]),
    ('Yajurveda', 'Kṛṣṇa', [
        ('beta', 'Taittirīya', 'with padapāṭha', YV + 'ts/anuvaka/1/1/1/'),
        ('beta', 'Taittirīya', '1,752 pañcāśats', YV + 'tb/'),
        ('beta', 'Taittirīya', '577 pañcāśats', YV + 'ta/'),
        ('beta', 'Taittirīya', 'Kaṭha · with Śaṅkara', AB + 'taittiriya/'),
    ]),
    ('Yajurveda', 'Śukla', [
        ('none', 'Vājasaneyi', '', None),
        ('none', 'Śatapatha', '', None),
        ('beta', 'Bṛhadāraṇyaka', 'with Śaṅkara', AB + 'brihadaranyaka/'),
        ('beta', 'Īśa', 'with Śaṅkara', AB + 'isha/'),
    ]),
    ('Sāmaveda', '', [
        ('partner', 'Jaiminīya', 'with a partner', 'https://sekharnarayanaswamy-del.github.io/jaimineeyasamavedam/'),
        ('none', 'Tāṇḍya', '', None),
        None,
        ('beta', 'Chāndogya', 'Kena · with Śaṅkara', AB + 'chandogya/'),
    ]),
    ('Atharvaveda', '', [
        ('none', 'Śaunaka', '', None),
        ('none', 'Gopatha', '', None),
        None,
        ('beta', 'Muṇḍaka', 'Praśna, Māṇḍūkya', AB + 'mundaka/'),
    ]),
]

# Groups of branches: (label, columns, [(state, title, sub, href), ...])
VEDANGA = ('Vedāṅga', 6, [
    ('progress', 'Śikṣā', 'svara tutor', ASK + '#abhyasa'),
    ('none', 'Vyākaraṇa', '', None), ('none', 'Chandas', '', None),
    ('none', 'Nirukta', '', None), ('none', 'Jyotiṣa', '', None), ('none', 'Kalpa', '', None),
])
UPAVEDA = ('Upaveda', 4, [
    ('none', 'Āyurveda', '', None), ('none', 'Dhanurveda', '', None),
    ('none', 'Gāndharvaveda', '', None), ('none', 'Arthaśāstra', '', None),
])
RIGHT = [
    ('Itihāsa', 2, [
        ('live', 'Mahābhārata', 'with Nīlakaṇṭha, Harivaṃśa', 'https://sanatana.in/mahabharata'),
        ('progress', 'Rāmāyaṇa', 'Vālmīki, 20,051 verses', 'https://hvram1.github.io/valmiki-ramayana.sanatana.in/'),
    ]),
    ('Purāṇa', 2, [
        ('beta', '18 Mahāpurāṇas', '7 atlases, verses heard', 'https://hvram1.github.io/purana-atlas/'),
        ('none', 'Their names', 'Nāma-Kośa · fund this →', ASK + '#namakosa'),
    ]),
    ('Dharmaśāstra', 3, [
        ('beta', 'Kane', 'History of Dharmaśāstra', 'https://hvram1.github.io/historyofdharmasastra/'),
        ('beta', 'Smṛtimuktāphalam', 'with the Tamil', 'https://hvram1.github.io/smp/'),
        ('none', 'Manu, Yājñavalkya…', 'fund this →', ASK + '#smritis'),
    ]),
    ('Darśana', 3, [
        ('none', 'Nyāya', '', None), ('none', 'Vaiśeṣika', '', None), ('none', 'Sāṅkhya', '', None),
        ('none', 'Yoga', '', None), ('none', 'Mīmāṃsā', '', None),
        ('beta', 'Vedānta', 'Śaṅkara\'s bhāṣyas', AB),
    ]),
    ('Āgama', 3, [
        ('none', 'Śaiva', '', None), ('none', 'Śākta', '', None), ('none', 'Vaiṣṇava', '', None),
    ]),
]

# The principal Upaniṣads, one chip each: (name, Veda, page, translations, chant).
# chant is None (no recording yet) or (label, href) for a result that would add it.
UPANISHADS = [
    ('Īśa', 'Śukla Yajurveda', 'isha/', 'Tamil, English', None),
    ('Kena', 'Sāmaveda', 'kena-pada/', 'Tamil · pada and vākya', None),
    ('Kaṭha', 'Kṛṣṇa Yajurveda', 'katha/', 'Tamil', None),
    ('Praśna', 'Atharvaveda', 'prashna/', 'Tamil', None),
    ('Muṇḍaka', 'Atharvaveda', 'mundaka/', 'Tamil', None),
    ('Māṇḍūkya', 'Atharvaveda', 'mandukya/', 'Tamil · with the kārikās', None),
    ('Taittirīya', 'Kṛṣṇa Yajurveda', 'taittiriya/', 'Tamil', ('fund the recording →', ASK + '#tbta-audio')),
    ('Aitareya', 'Ṛgveda', 'aitareya/', 'Tamil', None),
    ('Chāndogya', 'Sāmaveda', 'chandogya/', 'Tamil', None),
    ('Bṛhadāraṇyaka', 'Śukla Yajurveda', 'brihadaranyaka/', 'Tamil', None),
    ('Śvetāśvatara', 'Kṛṣṇa Yajurveda', None, '', None),
]

STATE_NAME = {'live': 'live', 'beta': 'beta', 'partner': 'with a partner', 'progress': 'under way', 'none': 'not yet'}

W, H = 1040, 720
CELL_H, GAP = 46, 6


def esc(s):
    return html.escape(s, quote=True)


def fit(text, w, size, per_char):
    """A smaller font size when the text would overrun its box (per_char: width of one character at `size`)."""
    need = len(text) * per_char
    return '' if need <= w - 10 else f' style="font-size:{size * (w - 10) / need:.1f}px"'


def cell(x, y, w, h, state, title, sub, href):
    tip = f'{title} — {STATE_NAME[state]}' + (f' · {sub}' if sub else '')
    body = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>'
            f'<text class="t" x="{x + w / 2:g}" y="{y + (h / 2 - 3 if sub else h / 2 + 4):g}"{fit(title, w, 12.5, 7.4)}>{esc(title)}</text>')
    if sub:
        body += f'<text class="s" x="{x + w / 2:g}" y="{y + h / 2 + 12:g}"{fit(sub, w, 10.5, 5.6)}>{esc(sub)}</text>'
    g = f'<g class="cm-{state}"><title>{esc(tip)}</title>{body}</g>'
    if href:
        g = f'<a href="{esc(href)}" target="_blank" rel="noopener">{g}</a>'
    return g


def group(x, y, width, label, cols, items):
    """A labelled group of cells laid out in rows of `cols`; returns (svg, bottom y)."""
    out = [f'<text class="cm-label" x="{x}" y="{y}">{esc(label.upper())}</text>']
    w = (width - GAP * (cols - 1)) / cols
    top = y + 10
    for i, it in enumerate(items):
        r, c = divmod(i, cols)
        out.append(cell(round(x + c * (w + GAP), 1), top + r * (CELL_H + GAP), round(w, 1), CELL_H, *it))
    rows = (len(items) + cols - 1) // cols
    return ''.join(out), top + rows * (CELL_H + GAP)


def upanishads(y):
    """The strip of principal Upaniṣads under the map; returns (svg, bottom y)."""
    out = [f'<text class="cm-label" x="20" y="{y}">THE PRINCIPAL UPANIṢADS, ONE BY ONE</text>']
    cols, w, h = 6, (1000 - GAP * 5) / 6, 76
    top = y + 10
    for i, (name, veda, page, tr, chant) in enumerate(UPANISHADS):
        r, c = divmod(i, cols)
        x, yy = round(20 + c * (w + GAP), 1), top + r * (h + GAP)
        state = 'beta' if page else 'none'
        mid = x + w / 2
        lines = [f'<rect x="{x}" y="{yy}" width="{w:.1f}" height="{h}" rx="6"/>',
                 f'<text class="t" x="{mid:g}" y="{yy + 18}">{esc(name)}</text>',
                 f'<text class="s" x="{mid:g}" y="{yy + 32}">{esc(veda)}</text>']
        if page:
            lines.append(f'<text class="u" x="{mid:g}" y="{yy + 48}"{fit(tr, w, 10.5, 5.6)}>bhāṣya · {esc(tr)}</text>')
        else:
            lines.append(f'<text class="u" x="{mid:g}" y="{yy + 48}">not on the site yet</text>')
        tip = f'{name}, {veda} — ' + (f"Śaṅkara's bhāṣya, {tr}" if page else 'not yet')
        g = f'<g class="cm-{state}"><title>{esc(tip)}</title>{"".join(lines)}</g>'
        if page:
            g = f'<a href="{esc(AB + page)}" target="_blank" rel="noopener">{g}</a>'
        out.append(g)
        if chant:
            out.append(f'<a href="{esc(chant[1])}" target="_blank" rel="noopener"><text class="ch fund" '
                       f'x="{mid:g}" y="{yy + 65}">♪ chant: {esc(chant[0])}</text></a>')
        else:
            out.append(f'<text class="ch" x="{mid:g}" y="{yy + 65}">♪ chant: not yet</text>')
    rows = (len(UPANISHADS) + cols - 1) // cols
    return ''.join(out), top + rows * (h + GAP)


def draw():
    out = []
    # root and trunks
    out.append('<g class="cm-root"><rect x="400" y="8" width="240" height="44" rx="22"/>'
               '<text x="520" y="36">Sanātana Dharma</text></g>')
    out.append('<path class="cm-trunk" d="M520 52 V66 M265 66 H780 M265 66 V80 M780 66 V80"/>')
    out.append('<text class="cm-head" x="265" y="96">ŚRUTI · THE VEDA</text>')
    out.append('<text class="cm-head" x="780" y="96">SMṚTI AND THE ŚĀSTRAS</text>')

    # the Veda matrix
    lx, cx, cw = 20, 112, 95
    out.append(f'<text class="cm-label" x="{lx}" y="128">ŚĀKHĀ</text>')
    for j, layer in enumerate(LAYERS):
        out.append(f'<text class="cm-col" x="{cx + j * (cw + 5) + cw / 2:g}" y="128">{esc(layer)}</text>')
    y = 138
    for name, kind, cells in VEDA:
        out.append(f'<text class="cm-row" x="{lx}" y="{y + 20}">{esc(name)}</text>')
        if kind:
            out.append(f'<text class="cm-rowsub" x="{lx}" y="{y + 35}">{esc(kind)}</text>')
        for j, c in enumerate(cells):
            if c:
                out.append(cell(cx + j * (cw + 5), y, cw, CELL_H, *c))
        y += CELL_H + GAP
    svg, y = group(lx, y + 22, 489, *VEDANGA)
    out.append(svg)
    svg, y_left = group(lx, y + 22, 489, *UPAVEDA)
    out.append(svg)

    # the right-hand branches
    y = 128
    for label, cols, items in RIGHT:
        svg, y = group(540, y, 480, label, cols, items)
        out.append(svg)
        y += 22
    bottom = max(y_left, y - 22)
    svg, bottom = upanishads(bottom + 26)
    out.append(svg)

    # legend
    ly = bottom + 30
    x = 20
    for state in ['live', 'beta', 'partner', 'progress', 'none']:
        out.append(f'<g class="cm-{state}"><rect x="{x}" y="{ly - 12}" width="22" height="14" rx="3"/></g>'
                   f'<text class="cm-leg" x="{x + 30}" y="{ly}">{esc(STATE_NAME[state])}</text>')
        x += 150
    height = ly + 16
    return (f'<svg class="cmap" viewBox="0 0 {W} {height}" role="img" '
            f'aria-labelledby="cmap-title"><title id="cmap-title">The branches of Sanātana Dharma\'s literature, '
            f'each shaded by where our work stands</title>{"".join(out)}</svg>')


def counts():
    cells = [c for _, _, row in VEDA for c in row if c]
    cells += VEDANGA[2] + UPAVEDA[2] + [c for _, _, items in RIGHT for c in items]
    lit = sum(c[0] in ('live', 'beta', 'partner') for c in cells)
    going = sum(c[0] == 'progress' for c in cells)
    return lit, going, len(cells)


def block():
    lit, going, total = counts()
    return (f'{START}\n<figure class="cmapwrap">\n<div class="cmapbox" tabindex="0" '
            f'aria-label="The coverage map; scroll sideways on a small screen">{draw()}</div>\n'
            f'<figcaption>{lit} of these {total} branches have something you can open today, and {going} more '
            f'are under way. Below the map, the principal Upaniṣads one by one: which have Śaṅkara\'s bhāṣya and a translation, and which can be heard. Each lit branch opens the page that shows it; a dark one with a result on the '
            f'funding page opens that result. The classical map has more branches than these; the ones shown '
            f'are those a reader is most likely to look for.</figcaption>\n</figure>\n{END}')


def main():
    src = open(PITCH, encoding='utf-8').read()
    if START not in src:
        raise SystemExit(f'{PITCH} has no {START} marker')
    new = re.sub(re.escape(START) + r'.*?' + re.escape(END), lambda m: block(), src, flags=re.S)
    if new != src:
        open(PITCH, 'w', encoding='utf-8').write(new)
    lit, going, total = counts()
    print(f'coverage map: {lit} of {total} branches open, {going} under way')


if __name__ == '__main__':
    main()
