# The World in One Day — 18 November 2026

[![make.fun](https://img.shields.io/badge/make.fun-news--image--20261118-blue)](https://make.fun/c/news-image-20261118)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A newspaper-style front page summing up the world news of **Wednesday, 18 November 2026** — eight stories from eight beats, drawn entirely in code with Python and Pillow.

## The eight stories

1. **Middle East** — U.S. sinks five Iranian tankers. Iran fires missiles at a U.S. base in Jordan and ships near Hormuz; oil tops $100.
2. **Politics** — Peltola wins Alaska Senate seat. Democrat beats Dan Sullivan; Democrats take a 56–44 Senate majority.
3. **Russia** — Russian military plane crashes in Siberia. An-12 transport goes down near Kemerovo; all 19 aboard killed.
4. **Weather** — Category 5 Cyclone Xavier hits Cook Islands. Gusts reach 315 km/h; wharves damaged on Manihiki, no deaths reported.
5. **Asia** — North Korea fires missile toward the sea. Seoul says a ballistic missile flew toward the Sea of Japan amid border tensions.
6. **Europe** — Deep 5.3 quake rattles Romania. Felt in Bucharest and Ukraine; no major damage reported.
7. **Americas** — U.S. report traces $12bn in Venezuelan oil revenue. 53-page State Department report details funds handled since Maduro's capture.
8. **Diplomacy** — Four nations urge Israel to let aid into Gaza. Australia, Canada, Italy and the UK call for open aid access as floods worsen.

Sources: Al Jazeera · Reuters · AP · MetService · The Paris Eye · The Munich Eye · USGS. All events happened, or were first reported, on 18 November 2026.

## How it runs

`draw_news.py` draws the 1024×1024 front page (`entry.png`) with PIL — navy masthead, a 2×4 grid of story cards with tag chips, serif headlines and short summaries, and a sources footer. The drawing program wraps text greedily and asserts that no headline exceeds 3 lines, no summary exceeds 2 lines, and nothing overflows its card.

`main.ts` (Node 22, standard library only) copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`):

```sh
python3 draw_news.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Repository

https://github.com/edwardlau2028/news-image-20261118
