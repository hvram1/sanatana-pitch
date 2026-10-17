# A report button for the vidvān, and keeping bots out

17 October 2026. A proposal, nothing built yet. It follows on from the report
button page in this folder (`index.html`).

## What we want

The vidvān reviewing the Taittirīya Saṃhitā on the Yajurveda review pages
(hvram1.github.io/yajurveda.sanatana.in/review/TS/) should be able to do two
things from the same page:

1. **Rule on each item**, as the review pages already allow: the numbers, the
   footnotes and the paragraph openings, each checked against the printed page.
2. **Raise a problem** the buttons cannot express: the review page itself is
   wrong, the scan or the reading is wrong in some other way, or a question.

The worry is misuse. A button that sends reports somewhere is something an
automatic bot can fire off, hundreds of times, with nobody behind it.

## The answer in one line

The risk depends on whether a report is *sent* anywhere automatically. So we do
this in two stages: first a button that sends nothing, then one that sends only
with a key that belongs to one vidvān.

## Stage 1: a report button that sends nothing

The review pages already keep the vidvān's decisions in their own browser, under
one key (`review-decisions:TS`). A Download button on any page gives one file
with everything, `decisions_TS_<date>.json`, which comes back to us and goes in
the site repository's `corrections/` folder.

Stage 1 adds a **Report a problem** button beside each item, with three choices:

| Choice | What it is for |
|---|---|
| This review page is wrong | a bug: the page shows the wrong scan, a button does nothing, the text runs off the screen |
| The scan or the reading is wrong | something the three ruling buttons cannot say |
| A question | anything else, in the vidvān's own words |

Each report records which item it is about, which printed page, the screen width
and the browser, and the vidvān's comment. It goes into **the same browser store
and the same download file** as the rulings.

**Why no bot can misuse it:** there is nowhere to send anything. No address
receives reports, so there is nothing for a bot to call.

**What it costs:** the limitation the review already has. Nothing reaches us
until the vidvān downloads the file and sends it, and the reports do not follow
the vidvān to another device.

## Stage 2: reports that arrive by themselves, behind a key

When we want reports to arrive without a download, the button sends each one to
the same report table the Mahābhārata site uses (`passage_reports`, with a new
`site` column so one table serves every site). The defences, in order of how
much they matter:

1. **The agents cannot act on a report.** They only sort it and attach evidence.
   Every change to a text needs a person. A flood of junk can fill a queue; it
   cannot change the text or the site. This is the main defence, and it holds
   whatever else fails.
2. **Each vidvān gets a private link carrying their own key.** This is the same
   "no accounts, a private link" model the Nāma-Kośa readers use. The server
   refuses any report without a valid key. If a key leaks, it is switched off
   and the vidvān gets a new link. Nobody else is affected.
3. **A daily cap per key.** Something like 150 reports a day. That is well above
   the busiest real reader: the Mahābhārata's most active proofreader sent 778
   reports in three weeks, about 40 a day. Duplicates are joined, and a
   report's text has a length limit.
4. **Two smaller details:**
   - The key goes in the link's fragment (after the `#`) and is kept in the
     browser. It never goes in the query string, which the server's logs would
     record.
   - The server accepts reports only from the review site's own address.

**No CAPTCHA.** It burdens exactly the people we want, older vidvāns on phones,
and a determined bot can get past it anyway. The key does the same job without
asking the vidvān to do anything.

## The Mahābhārata button needs the same care

The button on sanatana.in/mahabharata already sends reports to the server. Its
barrier is Google sign-in, which helps, but anyone can make a Google account. It
needs:

- **A daily cap per account**, as in Stage 2.
- **The report list behind an editor's sign-in.** Today
  sanatana.in/mahabharata/mail/report opens without signing in and shows every
  reporter's name, and their email address wherever one is stored.
- **"Mark as done" as a form, not a link.** Today it is a plain link
  (`mail/markReportDone?id=…`) that needs no sign-in. A search engine crawling
  the list would follow all 583 links and mark every open report done. That is
  a bot misusing the button system, and it can happen today.

These three are site changes, for the site's developer, in
`Sriraghunandana92/mahabharata` (`application/controllers/mail.php`,
`application/views/mail/report.php`).

## Where the work would go

| Stage | Where | What |
|---|---|---|
| 1 | `dharmasastra-gcp/complete_pipeline_yajurveda`, `stage2_analysis/review_page.py` and the three review modules | the Report button, stored with the rulings and downloaded with them |
| 2 | the site repository, `controllers/mail.php` and `config/schema.php` | the keyed endpoint, the daily cap, the `site` column, origin check |
| 2 | the review pages | read the key from the link's fragment, send each report, keep a copy in the browser if sending fails |
| now | the site repository | the two Mahābhārata fixes above, and a per-account cap |

The review code is on the `ts-bhashya-kanda1` branch, which has uncommitted
work (see `docs/TS_review_handoff_2026-10-15.md`). Stage 1 should be built and
checked locally first. The live review the vidvān is using changes only when we
choose to publish.

## For the team to decide

- Is Stage 1 enough for the Kāṇḍa 1 review, or do we need reports to arrive
  without a download from the start?
- Who issues the vidvāns' keys, and who switches one off if it leaks?
- What daily cap per key? 150 is a guess, set well above real use.
- Who makes the Mahābhārata fixes, and when? The "Mark as done" link is a risk
  today, not a future one.
