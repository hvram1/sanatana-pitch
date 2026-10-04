#!/usr/bin/env python3
"""PDFs of the three pages, with their links live, for sending as files.

    ~/projects/audio-ingest/myenv/bin/python make_pdf.py      (needs playwright + chromium)

Renders docs/ (run ./publish.py --site first) in headless Chromium, which keeps
every link clickable in the PDF. Five changes for print:

- every link points to the public github.io pages: the artifact links are
  private, and a relative link means nothing inside a file;
- the "How the price is made up" details are opened, so the PDF shows them;
- the light theme on a white page, whatever the viewer's setting (the grey
  page colour sits oddly inside the white print margins);
- a card, an ask or a table row is not split across a page break;
- the sticky nav is static, so it does not sit over the top of every page.

Writes docs/pdf/sanatana-sampatti-{pitch,funding,csr}.pdf, which GitHub Pages
also serves.
"""
import functools
import http.server
import os
import re
import shutil
import tempfile
import threading

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HERE, 'docs')
SITE = 'https://hvram1.github.io/sanatana-pitch/'
PAGES = [('index.html', 'sanatana-sampatti-pitch.pdf'),
         ('ask.html', 'sanatana-sampatti-funding.pdf'),
         ('csr.html', 'sanatana-sampatti-csr.pdf')]
PRINT_CSS = """
nav.top{position:static!important}
article,.ask,.prob,.card,.tier,.doc,.person,.node,.site,.reason,.thanks div,.letter,tr,figure{break-inside:avoid}
h2,h3{break-after:avoid}
section{padding-block:24px 4px!important}
body{padding-block-end:0!important;background:#fff!important}
nav.top{background:#fff!important}
"""


def absolute(html):
    """Relative links to the pages here become their github.io addresses."""
    def fix(m):
        url = m.group(2)
        # absolute links, anchors, and the funding page's script templates (${esc(o.url)})
        if re.match(r'^(https?:|mailto:|#|data:)', url) or '${' in url:
            return m.group(0)
        return f'{m.group(1)}"{SITE}{"" if url in ("./", "") else url}"'
    return re.sub(r'(href=)"([^"]*)"', fix, html)


def main():
    out = os.path.join(DOCS, 'pdf')
    os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp()
    try:
        for name in ('index.html', 'ask.html', 'csr.html', 'asks.json'):
            body = open(os.path.join(DOCS, name), encoding='utf-8').read()
            open(os.path.join(tmp, name), 'w', encoding='utf-8').write(absolute(body) if name.endswith('.html') else body)
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=tmp)
        handler.log_message = lambda *a: None
        srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        base = f'http://127.0.0.1:{srv.server_address[1]}/'
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(color_scheme='light', viewport={'width': 1100, 'height': 1400})
            for page, pdf in PAGES:
                pg.goto(base + page, wait_until='networkidle')
                pg.wait_for_timeout(800)                       # asks.json, fonts
                pg.add_style_tag(content=PRINT_CSS)
                pg.evaluate("document.documentElement.dataset.theme='light';"
                            "document.querySelectorAll('details').forEach(d=>d.open=true)")
                pg.emulate_media(media='print', color_scheme='light')
                path = os.path.join(out, pdf)
                pg.pdf(path=path, format='A4', print_background=True,
                       margin={'top': '14mm', 'bottom': '14mm', 'left': '12mm', 'right': '12mm'})
                print(f'{pdf}: {os.path.getsize(path) / 1e6:.1f} MB')
            b.close()
        srv.shutdown()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main()
