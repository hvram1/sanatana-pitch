# The Nāma-Kośa loop

How the Purāṇa Nāma-Kośa gets built: agents do the legwork, scholars decide.
The page follows one request (a student asks about Yayāti) through seven steps,
each marked as an agent's work or a person's decision, and shows Yayāti's family
in the index today and as it should look after the work. The engineering sits in
an appendix at the end.

It builds on the Scholar Workbench design
(`dharmasastra-gcp/workbench/docs/DESIGN-scholar-workbench-2026-08-21.md`;
published as https://hvram1.github.io/purana-atlas/docs/purana-scholar-workbench.html).
Where the two differ, the design note wins.

Published at https://hvram1.github.io/sanatana-pitch/namakosa/ (`./publish.py --site`
wraps `index.html` and copies the SVGs into `docs/namakosa/`), and privately as
the Claude artifact https://claude.ai/artifact/WvdQBUeofUL4t1ZpY55143.
To view it locally:

    cd namakosa && python3 -m http.server 8766      # then open http://localhost:8766

Serve it rather than opening the file: the page fetches its SVGs and inlines
them so they follow its light and dark themes.

| file | what it is |
|---|---|
| `index.html` | the page, in artifact form (no document skeleton; `publish.py` adds it) |
| `map-today.svg`, `map-after.svg` | Yayāti's family: as the index holds it today, and after the work (expected) |
| `flow-request.svg` | the seven steps as one swimlane diagram |
| `map.py` | writes both maps |
| `flows.py` | writes `flow-request.svg`; edit the boxes and arrows here |

Run `python3 map.py` or `python3 flows.py` from this folder to regenerate.

Where the figures come from: counts of entities, relations and scholar rulings
are from `dharmasastra-gcp/workbench/data/substrate/corpus.db`; Purāṇa verse
counts are string matches in the Śāradā Pīṭham texts
(`sharadapeetham/data/purana/*.json`), not resolved people. Mahābhārata chapter
numbers are working references (Dutt) still to be checked against the site's own
addresses. Names in the mock-ups (Student A, Vidvān C) are placeholders.
