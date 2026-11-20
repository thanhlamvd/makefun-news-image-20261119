# makefun-news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/thanhlamvd/makefun-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/thanhlamvd/makefun-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Entry for the [news-image-20261119](https://make.fun/bounty/news-image-20261119)
competition on make.fun: one image that sums up the world's news of
Thursday 19 November 2026.

## What the image shows

A newspaper front page — "THE WORLD IN ONE DAY / THURSDAY, 19 NOVEMBER 2026"
— with the six stories that defined the day, as reported on 19 November 2026
by Reuters, AP, AFP, BBC, TechCrunch and PTI:

1. **Diplomacy** — Trump, Xi and Putin hold the first three-way summit in
   Shenzhen, at APEC.
2. **Justice** — The ICJ rules 9–6 that Myanmar committed genocide against
   the Rohingya in 2017; about 10,000 were killed.
3. **Middle East** — A Houthi strike hits Riyadh's PIF Tower, the Saudi
   sovereign wealth fund's HQ.
4. **Europe · War** — Ukraine strikes the Kerch Bridge rail section for the
   third time in four days; train traffic halts.
5. **Technology** — Anthropic debuts on Nasdaq in a record $81.3B IPO;
   shares open at $111, 33% above the $83 price.
6. **South Asia** — Bangladesh burns as the Awami League lockdown bites:
   Yunus's ancestral home is torched, four people killed.

## How it works

`main.py` (Python 3.13, standard library only) copies `entry.png` to
`/output/entry.png`. `entry.png` is drawn by `generate_image.py` (Pillow,
build-time only) from the six verified stories embedded in it — the image
is the entry's own work, no photograph or artwork copied from anyone else.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

- **Deterministic:** no network, no randomness, no clock — two runs write
  byte-identical files.
- **Within limits:** PNG, 1024×1024, 121,498 bytes (limit 1 MiB).

## Licence

MIT — see [LICENSE](LICENSE).

---

<sub>Entered on [make.fun](https://make.fun/?ref=814bp22d&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
