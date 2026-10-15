# The Nāma-Kośa loop

How the Purāṇa Nāma-Kośa gets built with agents running the workflow while
vidvāns and pāṭhaśālā students do the reading and ruling. It follows one story,
Yayāti and Pūru's line, from the Mahābhārata into the Bhāgavata and the Garuḍa
Purāṇa, and shows three flows (light a character, catch a wrong link, open a
door), how a reader's name reaches the verse they read, and the eight agents.

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
| `yayati-map.svg` | the family map: Yayāti, his gurus and queens, Pūru's line to Parīkṣit, the Purāṇa doors |
| `flow-request.svg`, `flow-correction.svg`, `flow-link.svg` | the three flows as swimlane diagrams |
| `flow-credit.svg` | from a student's decision to their name on the page |
| `map.py` | writes `yayati-map.svg` |
| `flows.py` | writes the four `flow-*.svg`; edit a flow's boxes and arrows here |

Run `python3 map.py` or `python3 flows.py` from this folder to regenerate.

Where the figures come from: counts of entities, relations and scholar rulings
are from `dharmasastra-gcp/workbench/data/substrate/corpus.db`; Purāṇa verse
counts are string matches in the Śāradā Pīṭham texts
(`sharadapeetham/data/purana/*.json`), not resolved people. Mahābhārata chapter
numbers are working references (Dutt) still to be checked against the site's own
addresses. Names in the mock-ups (Student A, Vidvān C) are placeholders.
