# The report button

What triggers the four loops (`../corrections/`, `../namakosa/`, `../fixes/`,
`../newbook/`): the existing "report a passage" button on sanatana.in/mahabharata,
extended so an agent can route each report. The page covers the button as it is
(820 reports, 21 Sep to 10 Oct 2026; 583 open), two access problems to fix first
(the report list is public, and "Mark as done" is a plain link anyone can follow),
the extended popup (four kinds, "it should read"), the routing table, report 818
followed end to end, and the site and agent changes needed.

Sources: the live list at sanatana.in/mahabharata/mail/report, read on 17 October
2026; the site code on `main` of `Sriraghunandana92/mahabharata`
(`application/controllers/mail.php`, `views/listing/parva.php`, `config/schema.php`),
fetched into `../../sriranga/mahabharata`; `mbh_src/qa/witness_check.py --control`
(345 open verse reports: 158 flagged by both editions, 37 by one, 150 not).

`index.html` is in artifact form; to view locally:

    python3 -c "import publish; [publish.build_loop(n, 'dist') for n in publish.LOOPS]"
    cd dist && python3 -m http.server 8767   # then open http://localhost:8767/trigger/
