# The World in One Day — 18 November 2026

[![make.fun](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/edwardlau2028/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/edwardlau2028/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

An entry for the make.fun competition
[news-image-20261118](https://make.fun/c/news-image-20261118):
one 1024×1024 image that sums up the world news of
**Wednesday, 18 November 2026**.

## The image

`entry.png` is a newspaper-style front page drawn in code
(`draw_news.py`, Python + PIL, system fonts only — no AI image
generator, so every headline is pixel-accurate text). It covers the
day's eight biggest stories, across regions and beats:

1. **Middle East** — the U.S. sinks five Iranian tankers, after Iran
   fires missiles at a U.S. base in Jordan and ships near Hormuz;
   oil tops $100.
2. **Politics** — Peltola wins the Alaska Senate seat; Democrats take
   a 56–44 Senate majority.
3. **Russia** — a Russian military An-12 transport crashes in Siberia
   near Kemerovo; all 19 aboard killed.
4. **Weather** — Category 5 Cyclone Xavier hits the Cook Islands,
   with gusts of 315 km/h; wharves damaged on Manihiki, no deaths
   reported.
5. **Asia** — North Korea fires a ballistic missile toward the Sea of
   Japan amid border tensions.
6. **Europe** — a deep magnitude 5.3 earthquake rattles Romania,
   felt in Bucharest and Ukraine.
7. **Americas** — a U.S. State Department report traces $12bn in
   Venezuelan oil revenue handled since Maduro's capture.
8. **Diplomacy** — Australia, Canada, Italy and the UK urge Israel to
   let aid into Gaza as floods worsen suffering.

Sources are credited in the image footer: Al Jazeera, Reuters, AP,
MetService, The Paris Eye, The Munich Eye, USGS.

## How it runs

`main.ts` (Node 22, standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`):

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

To redraw the image from scratch: `python3 draw_news.py`
(requires Pillow and the Noto fonts; it asserts that no headline or
summary overflows its card).

## Repository

GitHub: [edwardlau2028/news-image-20261118](https://github.com/edwardlau2028/news-image-20261118)
