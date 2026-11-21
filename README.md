[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/gamingjancok11-ctrl/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/gamingjancok11-ctrl/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# The World Today — Saturday 21 November 2026

A dense front-page newspaper image summing up one day's world news:
**35 verified stories across six continents**, with three lead stories, a
15-story brief grid, a world map with 19 numbered markers and a key, 17
more briefs, and a sources footer.

Leads: COP31 slips into overtime in Antalya with no deal in sight; a
Russian "triple-tap" strike kills a 7-year-old boy in Kryvyi Rih; an
Israeli strike kills three World Central Kitchen aid workers in Gaza City.

Every story was verified against reporting published on Saturday
21 November 2026 (Reuters, AP, BBC, CNN, Al Jazeera, NYT, AFP, Ukrinform,
ESA, UKMTO, FIFA, Yonhap, AAP). The image is rendered deterministically
with Python/PIL from `render.py` — exactly 1024×1024 pixels.

## Run it

```sh
node main.ts        # copies entry.png to /output/entry.png
```

`main.ts` uses only the Node standard library. Re-running it always
produces identical bytes. To re-render the image from scratch:

```sh
python3 render.py   # regenerates entry.png (1024x1024)
```

## Files

- `entry.png` — the entry image (1024×1024, ≤1 MiB)
- `main.ts` — copies `entry.png` to `/output/entry.png`
- `render.py` — the deterministic PIL renderer (stories + map data live here)
- `LICENSE` — MIT

<sub>Entered on [make.fun](https://make.fun/?ref=fz2026e2&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
