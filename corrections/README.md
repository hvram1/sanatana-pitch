# The correction loop

How a text on the site gets corrected: agents find the differences, people rule.
Two cases. **Case 1, Yajurveda**, against the printed page: the page follows one printed page (Taittirīya
Saṃhitā with Bhaṭṭabhāskara's bhāṣya, Mysore edition, Vol. I pp.66–67, TS 1.1.12)
through seven steps, with its four real disagreements: a typo in the typed file,
a letter the reading agent misread, a manuscript variant the book records (which
the agent silently "corrected"), and a variant footnote misread. A second section
shows the Sāyaṇa joint-commentary fixes. **Case 2, Mahābhārata**, against other
editions (no scans): Mahāprasthānika Parva 3, the dog episode. Verse 3.12, fixed by
the typists on 27 September (`mbh_src` cb6e655: भोक्तुं→मोक्तुं, ब्रुतं→व्रतं,
चार्त→चार्तं), has one witness, since the Critical Edition lacks the verse; verse 3.11
is a live both-edition flag (त्यक्ष्यामेनं against त्यक्ष्याम्येनं). The figures
come from `mbh_src/qa/witness_check.py`: findings at HEAD, and `--score 228512a`
(104 corrections since 4 July: 48 caught by both editions, 14 by one, 42 missed),
both run on 17 October 2026. The engineering for both cases sits in an appendix.
It is a sibling of `../namakosa/` and uses the same look.

Yajurveda source: `dharmasastra-gcp/complete_pipeline_yajurveda`, as of
`docs/TS_review_handoff_2026-10-15.md`; corrections in
`data/corrections/TS/{sayana,bhatta}.json`. Where that note and this page differ,
the note wins. The four readings were checked by eye against the scans.

Local only for now. `./publish.py --site` would serve it at
https://hvram1.github.io/sanatana-pitch/corrections/ (it wraps `index.html` and copies
the images into `docs/corrections/`); that copy is public. An earlier draft, Case 1
only, is the private Claude artifact https://claude.ai/artifact/1Th4egpeJG244ciohXb2i9.
To view locally, view the wrapped copy, not `index.html` itself. The source has
no `<meta charset>` or doctype (the artifact host and `publish.py` add them), so
served raw the browser guesses the encoding and garbles the Devanagari:

    python3 -c "import publish; [publish.build_loop(n, 'dist') for n in publish.LOOPS]"
    cd dist && python3 -m http.server 8767   # then open http://localhost:8767/corrections/

`dist/` is not committed, so this publishes nothing.

| file | what it is |
|---|---|
| `index.html` | the page, in artifact form (no document skeleton; `publish.py` adds it) |
| `page-66.webp` | the full printed page, from the TS review build (`review/pages/01_0066.webp`) |
| `page-67-para6.webp` | p.67, the opening of paragraph 6 (cropped) |
| `page-67-footnote.webp` | p.67, the footnote band (`review/pages/01_0067-band.webp`) |
