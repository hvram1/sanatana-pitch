# sanatana-pitch

The source of the two pages Sanatana Sampatti sends to trustees, funders and
CSR officers. Both are published as private Claude artifacts and shared by link.

| page | source | published at |
|---|---|---|
| The pitch | `src/pitch.html` + `src/images/` | https://claude.ai/artifact/J3XQCuGh4AhhZp3f8ZfUzE |
| The funding page | `src/ask.html` + `src/asks.json` | https://claude.ai/artifact/RHAxouvYiRFwdCxdjFGxzx |
| For heads of CSR | `src/csr.html` + `src/asks.json` | https://claude.ai/artifact/BYGH7ZaAMHHuFrhFU7WrJ7 |

**This repo is the master.** Edit here, run `./publish.py --site`, republish
`dist/` to the same URLs, and commit `docs/`. Never edit an artifact without updating this copy. A
republish changes the page for everyone who already has the link, on their next load.

## Publishing

    ./publish.py            # check the figures, then build dist/
    ./publish.py --check    # check the figures only

`dist/pitch.html` has the images inlined, so it is one self-contained page.
`dist/asks.json` is published beside `dist/ask.html` as a file named `asks.json`;
the funding page fetches it by that name. Its list of asks, prices and meters lives
only there, so to change an ask, edit `src/asks.json`.

The Artifact tool only accepts supporting files from the session's working
directory or scratchpad, so when publishing from another repo's session, copy
`dist/ask.html` and `dist/asks.json` there first.

## The coverage map

The map of the tradition in the pitch's Section III is drawn by `coverage_map.py`
from the data at its top: each branch, its state (live, beta, with a partner,
under way, not yet) and the page it links to. `publish.py` redraws it on every
build, between the `coverage-map` markers in `src/pitch.html`; edit the data, not
the SVG. A dark branch with a result on the funding page links to that result
(`#namakosa`), and the funding page scrolls to it once its list has loaded.

## The figure check

Every number the pages print that has a local source is checked against it:
`purana-atlas/data/stats.json`, `sharadapeetham/build/index.db`, the Ṛgveda
site's sync files, and the Kane synopsis audio. These repos are expected beside
this one in `~/projects`. A wrong number stops the build. Figures without a
local source are printed as UNCHECKED, with where they come from. That is not a pass.

Note: "513,887 verses in one index" is index.db's occurrence count. Distinct
verses (the `verse` table) number 507,977. The Kane line's "493,992 verses" is
the index as it was when the footnotes were matched, before the Vālmīki
Rāmāyaṇa was added (6 October 2026); it is not checked against the index now.

## Two copies: the artifacts and github.io

The same two pages are served in two places, and both are kept for now:

| | pitch | funding page | who can see it |
|---|---|---|---|
| Claude artifacts | J3XQ… | RHAx… | only the people each link is shared with |
| GitHub Pages | https://hvram1.github.io/sanatana-pitch/ | …/sanatana-pitch/ask.html | anyone; the pages are public and can be indexed |

The showcase for Anthropic (`showcase/`) is served there too, at
https://hvram1.github.io/sanatana-pitch/showcase/: `--site` copies its page and
images (not its notes) into `docs/showcase/`.

`./publish.py --site` builds both: `dist/` for the artifacts, `docs/` for Pages
(served from `main`, folder `/docs`). `docs/` is committed and `dist/` is not.
In `docs/`, the two pages link to each other's github.io copy, because the
artifact links are private. Rebuild and commit `docs/` whenever you republish
the artifacts, or the two copies drift apart.

The github.io copy is public, so it shows the draft prices, the beta figures and
the trustees' names to anyone.

## PDFs

    ./publish.py --site
    ~/projects/audio-ingest/myenv/bin/python make_pdf.py      # needs playwright + chromium

`docs/pdf/sanatana-sampatti-{pitch,funding,csr}.pdf`, each link live and pointing at
the public github.io pages (the artifact links are private). The price
breakdowns are printed open. Remake them after any change to the pages, or they
fall behind.
