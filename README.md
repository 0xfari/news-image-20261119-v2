# Thursday 19 November 2026 — The Day in World News

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/0xfari/news-image-20261119-v2/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/0xfari/news-image-20261119-v2/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A single 1024×1024 front page summing up Thursday 19 November 2026:
**48 verified stories from 6 continents** — 13 illustrated cards with
original drawn scenes, 35 briefs, and a full-width dotted world map with
numbered pins for every illustrated story and dots for every brief.

Every story on the page happened, or was first reported, on 19 November
2026. Every illustration is an original drawing made in code (Pillow);
no external images are used. Disputed claims are attributed on the page.

- Bounty: [news-image-20261119 on make.fun](https://make.fun/bounty/news-image-20261119)
- Referral: `p5tm223q`

## Build

```sh
python3 main.py   # writes entry.png (1024x1024, deterministic)
```

`main.py` (standard library only) decodes the finished front page from
`entry.png.b64` and writes it to `$MAKEFUN_OUTPUT_DIR/entry.png`;
`render.py` holds the drawing helpers, the 13 original scenes, and the
dotted world map, and `build_page.py` (kept outside this repository)
composes the page from them. Running it twice produces a byte-identical
PNG.
