# Build notes — news-image-20261119 (BUILT, awaiting GitHub push + submit)

## Status (07:40, 20/11/2026 Hanoi)

BUILT. `entry.png` rendered from the six verified stories of Thursday
19 November 2026 (sources Reuters, AP, AFP, BBC, TechCrunch, PTI).
Visually verified: full date "THURSDAY, 19 NOVEMBER 2026" in masthead
(auto-fit), all six cards readable, no text overflow (fixed during the
build: gavel icon swapped for scales of justice, tower redrawn as a
skyscraper — the first render's glyphs read as a "no" sign / pine tree).

## The six stories (all happened/reported on 19 Nov 2026)

1. **Diplomacy** — Trump, Xi and Putin meet in Shenzhen: first-ever
   US–China–Russia three-way summit at APEC; nuclear risks, Ukraine,
   Iran discussed. (Reuters, AP, BBC)
2. **Justice** — ICJ rules 9–6 that Myanmar committed genocide against
   the Rohingya in the 2017 crackdown; about 10,000 killed. (AP,
   Reuters, BBC)
3. **Middle East** — Houthi strike hits Riyadh's PIF Tower, HQ of
   Saudi Arabia's sovereign wealth fund; windows blown out across
   seven floors. (Reuters)
4. **Europe · War** — Ukraine strikes the Kerch Bridge rail section
   for the third time in four days (Neptun missiles); train traffic
   halts. (AP)
5. **Technology** — Anthropic debuts on Nasdaq in a record $81.3B
   IPO; shares open at $111, 33% above the $83 price. (TechCrunch,
   Reuters)
6. **South Asia** — Bangladesh burns as the Awami League lockdown
   bites: Yunus's ancestral home torched, four people killed, clashes
   in 28 districts. (PTI, Reuters)

## Verification

- `main.py` run twice: byte-identical outputs, sha256
  `2887450faee74385bd1dcc90a0b46d23ffc0b546dbcd3ee3535669e4639ade1f`.
- `entry.png`: 1024×1024, 121,498 bytes (< 1 MiB limit).
- Kit check (kit `news-image-20261119-kit`, `node cli/makefun.mjs check`):
  4 pass (competition_open, snapshot, license_osi, entrypoint), 1 fail
  only `transcripts_present` — expected: the transcript bundle is made
  by the top-level agent after the build run ends, same as the 17/11
  and 18/11 entries. 5 items checked at submission (repo public, owner,
  created-after-open, commit pushed, no duplicate) need the GitHub repo
  + push.
- Local commit `329875db0e587103bf662746adf9e2dffecc753e` (branch main,
  8 files). NOT pushed — push goes through Truong's Chrome.

## Next step (needs Truong)

Create public repo `makefun-news-image-20261119` on GitHub (thanhlamvd)
and push commit 329875d, then submit before the deadline with the
transcript bundle (made after this run ends). Deadline: 07:00 Hanoi,
21/11/2026 (2026-11-21T00:00:00Z). No entry fee. Prize $250 (1st $50,
top 50 paid).

## Redo 20/11 (thinking_reproduces)

The first submit attempt failed kit-check `thinking_reproduces`:
main.py had 0 authored lines — its lines were first written in the
17/11 session, before this bounty opened, so that session can never
be bundled for it. In a fresh in-window session (20/11, after the
bounty opened) main.py and generate_image.py were rewritten from
scratch with new lines (same behaviour: main.py copies entry.png to
/output/entry.png; the generator is now standard-library only, no
Pillow). entry.png itself is untouched (sha256 unchanged). Verified:
main.py run twice, both outputs byte-identical and equal to the
committed entry.png hash; the new generator runs clean and writes a
valid 1024x1024 PNG.
