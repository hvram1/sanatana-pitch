# sanatana-pitch

The source of the two pages Sanatana Sampatti sends to trustees, funders and
CSR officers. Both are published as private Claude artifacts and shared by link.

| page | source | published at |
|---|---|---|
| The pitch | `src/pitch.html` + `src/images/` | https://claude.ai/artifact/J3XQCuGh4AhhZp3f8ZfUzE |
| The funding page | `src/ask.html` + `src/asks.json` | https://claude.ai/artifact/RHAxouvYiRFwdCxdjFGxzx |

**This repo is the master.** Edit here, run `./publish.py`, then republish
`dist/` to the same URLs. Never edit an artifact without updating this copy. A
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

## The figure check

Every number the pages print that has a local source is checked against it:
`purana-atlas/data/stats.json`, `sharadapeetham/build/index.db`, the Ṛgveda
site's sync files, and the Kane synopsis audio. These repos are expected beside
this one in `~/projects`. A wrong number stops the build. Figures without a
local source are printed as UNCHECKED, with where they come from. That is not a pass.

Note: "493,992 verses in one index" is index.db's occurrence count. Distinct
verses (the `verse` table) number 488,149.

## Not for GitHub Pages

The repo is private, and the pages stay private artifacts. A github.io page would
be public and searchable, and these pages carry draft prices, beta figures and
the trustees' names.
