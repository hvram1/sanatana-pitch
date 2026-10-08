# The showcase: A Handful of People

A scroll-through page for Anthropic: how a handful of people, with Claude Code in
the team, are carrying the tradition's texts, commentaries and recitation into
the digital age. It is the third front, separate from the funder pitch (`src/`)
and the strategy work.

    cd showcase && python3 -m http.server 8765      # then open http://localhost:8765

Serve it rather than opening the file: the opening plays a YouTube recording,
and YouTube's player does not load from a page opened straight off disk.

| file | what it is |
|---|---|
| `index.html` | the page, self-contained apart from its three images and Google Fonts |
| `images/` | the printed and chanted TS 1.1.1, and one printed line of the Jaiminīya Sāmaveda |
| `note-to-anthropic.md` | the short note to go with the link, for a friend to forward |

Where the figures come from, so they can be refreshed before the page is sent:

- **The conversations**: the trustee's messages and Claude Code's replies, from the
  session transcripts in `~/.claude/projects`. The trustee's words are verbatim;
  Claude Code's are excerpts in its own words, cut with `…`.
- **Ten months**: prompts per month from `~/.claude/history.jsonl` (tradition
  projects only; this machine's history begins in March 2026), and commits per
  month from the git history of the project repositories.
- **The opening**: Musiri's Kārtika Māhātmya discourse, part 3 (`kmm-03`), with
  each half-verse lit at the second the Purāṇa Atlas has it chanted
  (`purana-atlas/data/kartika_4lang.json`).
- **The Jaiminīya Sāmaveda**: Sri Sekhar Narayanaswamy's commit count is from his
  fork, github.com/sekharnarayanaswamy-del/jaimineeyasamavedam, across all its
  branches. It is a snapshot (436 on 8 October 2026); refresh it before sending.
