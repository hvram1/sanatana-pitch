# The new-book loop

How a new book reaches the site, followed through one real case: the Smṛtimuktāphalam (seven parts, 4,333 scanned pages) from the scans to hvram1.github.io/smp and its links with Kane. Eight steps; the vidvān's read of the text is marked not started.

A sibling of `../namakosa/` and `../corrections/`, in the same look: one real case,
round markers for agent work, diamonds for people's decisions, the engineering in
an appendix. Figures come from `dharmasastra-gcp/smp/README.md`, `smp/WORKPLAN.md`, and the commits of 14 and 17 September 2026. No scan is reproduced: the scans belong to svradhakrishnasastri.in.

`index.html` is in artifact form (no doctype or charset; `publish.py` adds them).
Local only for now; `./publish.py --site` would serve it, publicly, at
https://hvram1.github.io/sanatana-pitch/newbook/. To view locally:

    python3 -c "import publish; [publish.build_loop(n, 'dist') for n in publish.LOOPS]"
    cd dist && python3 -m http.server 8767   # then open http://localhost:8767/newbook/
