# The fix loop

How a fault or a request becomes a change, followed through one real report: "I click a link and nothing happens" on the Smṛtimuktāphalam edition on a phone, through four fixes, one of which (two views with a switch) is a feature. A second section covers the same day's related fixes and a suggestion that went through the same loop.

A sibling of `../namakosa/` and `../corrections/`, in the same look: one real case,
round markers for agent work, diamonds for people's decisions, the engineering in
an appendix. Figures come from the `dharmasastra-gcp` commits of 17 September 2026 (ea46fe6f, f313b713, 5fb3b5fc, 1c659b37, 5d7fa39c, 649abdb7, 48629f71, d37b5701). Who reported the fault is not recorded there.

`index.html` is in artifact form (no doctype or charset; `publish.py` adds them).
Published with the team map (`./publish.py --site`), publicly, at
https://hvram1.github.io/sanatana-pitch/fixes/. To view locally:

    python3 -c "import publish; [publish.build_loop(n, 'dist') for n in publish.LOOPS]"
    cd dist && python3 -m http.server 8767   # then open http://localhost:8767/fixes/
