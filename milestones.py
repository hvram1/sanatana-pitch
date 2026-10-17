#!/usr/bin/env python3
"""Write the journey timeline from src/milestones.json into the pages that show it.

Each page carries a marked block, <!-- milestones:AUDIENCE --> ... <!-- /milestones:AUDIENCE -->,
and this replaces what is between the markers. The pages stay self-contained and
viewable as files; the facts live in one place, so the two audiences cannot drift.

    python3 milestones.py           # rewrite the blocks
    python3 milestones.py --check   # exit 1 if a block is stale, write nothing
"""
import argparse, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'src', 'milestones.json')
PAGES = {'anthropic': os.path.join(HERE, 'showcase', 'index.html'),
         'funder': os.path.join(HERE, 'src', 'pitch.html'),
         'team': os.path.join(HERE, 'team', 'index.html')}
# the middle column names the software's part: Claude Code to Anthropic, plain software to a funder
WHO = {'anthropic': ('Claude Code', 'claude'), 'funder': ('Software does', 'software')}
ASKS = os.path.join(HERE, 'src', 'asks.json')
ASK_URL = 'https://claude.ai/artifact/RHAxouvYiRFwdCxdjFGxzx'   # publish.ASK_URL; the site build rewrites it to ask.html
STATUS = {'done': 'done', 'running': 'running now', 'waiting': 'waiting', 'proposed': 'proposed'}
e = html.escape


def card(i, m, audience, asks):
    a = m[audience]
    title = a.get('title', m['title'])
    number = a['number'] if 'number' in a else m.get('number')
    num = ''
    if number:
        num = (f'<div class="j-num"><b>{e(number["value"])}</b>'
               f'<span>{e(number["label"])}</span></div>')
    more = f' <a class="j-more" href="{e(a["link"])}">↑ on this page</a>' if a.get('link') else ''
    ask = ''
    if a.get('ask'):
        ask = (f'<a class="j-ask" href="{ASK_URL}#{e(a["ask"])}" target="_blank" rel="noopener">'
               f'Fund this: {e(asks[a["ask"]])} →</a>')
    label, key = WHO[audience]
    return f'''<li class="j-m s-{m["status"]}" id="m-{m["id"]}">
        <div class="j-dot"><span>{i}</span></div>
        <div class="j-body">
          <div class="j-meta"><span class="j-when">{e(m["when"])}</span><span class="j-status">{STATUS[m["status"]]}</span></div>
          <h3>{e(title)}</h3>
          <p>{e(a["line"])}{more}</p>
          {num}
          <dl class="j-who"><div><dt>Starts it</dt><dd>{e(a["starts"])}</dd></div><div><dt>{label}</dt><dd>{e(a[key])}</dd></div><div><dt>Decides</dt><dd>{e(a["decides"])}</dd></div></dl>
          {ask}
        </div>
      </li>'''


def block(d, audience, asks):
    out, today_done = [], False
    for i, m in enumerate(d['milestones'], 1):
        if m['status'] == 'proposed' and not today_done:
            out.append(f'<li class="j-today"><span>Today · {e(d["today"])}</span></li>')
            today_done = True
        out.append(card(i, m, audience, asks))
    return '\n      <ol class="j-line">\n      ' + '\n      '.join(out) + '\n      </ol>\n      '


def block_team(d, asks):
    """The team map: each milestone with both outside wordings side by side, and the
    internal pages and sources behind it. Links are relative to dist/, where it is served."""
    rows = []
    for i, m in enumerate(d['milestones'], 1):
        if m['status'] == 'proposed' and not any('j-today' in r for r in rows):
            rows.append(f'<li class="j-today"><span>Today · {e(d["today"])}</span></li>')
        an, fu, t = m['anthropic'], m['funder'], m['team']
        pages = ''.join(f'<li><a href="../{e(h)}">{e(label)}</a></li>' for h, label in t['pages'])
        src = ''.join(f'<li><code>{e(x)}</code></li>' for x in t['sources']) or '<li class="small">none</li>'
        ask = f'<p class="small">Funds: {e(asks[fu["ask"]])}</p>' if fu.get('ask') else ''
        rows.append(f'''<li class="j-m s-{m["status"]}" id="m-{m["id"]}">
        <div class="j-dot"><span>{i}</span></div>
        <div class="j-body">
          <div class="j-meta"><span class="j-when">{e(m["when"])}</span><span class="j-status">{STATUS[m["status"]]}</span></div>
          <div class="two">
            <div><span class="mk-l">To Anthropic · <a href="../showcase/#m-{m["id"]}">in the showcase</a></span><h3>{e(an.get("title", m["title"]))}</h3><p>{e(an["line"])}</p></div>
            <div><span class="mk-l">To funders · <a href="../view/pitch.html#m-{m["id"]}">in the pitch</a></span><h3>{e(fu.get("title", m["title"]))}</h3><p>{e(fu["line"])}</p>{ask}</div>
          </div>
          <div class="two inside"><div><span class="mk-l">Pages behind it</span><ul>{pages}</ul></div><div><span class="mk-l">Where the work lives</span><ul>{src}</ul></div></div>
        </div>
      </li>''')
    return '\n      <ol class="j-line">\n      ' + '\n      '.join(rows) + '\n      </ol>\n      '


def run(check=False):
    """Rewrite each page's block (or, with check, only report); returns the stale pages."""
    d = json.load(open(DATA, encoding='utf8'))
    asks = {x['id']: x['title'] for x in json.load(open(ASKS, encoding='utf8'))['asks']}
    stale = []
    for audience, path in PAGES.items():
        s = open(path, encoding='utf8').read()
        pat = re.compile(rf'(<!-- milestones:{audience} -->)(.*?)(<!-- /milestones:{audience} -->)', re.S)
        if not pat.search(s):
            sys.exit(f'{path}: no <!-- milestones:{audience} --> block')
        body = block_team(d, asks) if audience == 'team' else block(d, audience, asks)
        new = pat.sub(lambda mo: mo.group(1) + body + mo.group(3), s)
        if new != s:
            stale.append(path)
            if not check:
                open(path, 'w', encoding='utf8').write(new)
    return stale


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    stale = run(args.check)
    if args.check:
        if stale:
            sys.exit('stale: ' + ', '.join(stale) + ' (run milestones.py)')
        print('milestones: up to date')
    else:
        print('milestones: wrote ' + (', '.join(stale) if stale else 'nothing, already up to date'))


if __name__ == '__main__':
    main()
