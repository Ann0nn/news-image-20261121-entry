# The World Today, Saturday 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![Rank](https://make.fun/badge/news-image-20261121/Ann0nn/news-image-20261121-entry/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![Reward](https://make.fun/badge/news-image-20261121/Ann0nn/news-image-20261121-entry/reward.svg)](https://make.fun/bounty/news-image-20261121)

Entry for the [make.fun bounty "Sum up 21 November's world news in one image"](https://make.fun/bounty/news-image-20261121).

## What it is

A one-page newspaper front page, 1024x1024, summing up the world news of
Saturday 21 November 2026. The lead story is the Houthi missile attack on
Riyadh, intercepted in the early hours of Saturday morning, with a night
skyline illustration of the interceptions. Below it, five stories from
around the world (Iran, Peru, Europe, the United States, Denmark) and six
short briefs, from New York to Washington. Every story happened, or was
first reported, on 21 November 2026.

## Files

- `entry.png`, the finished front page (1024x1024, under 1 MiB).
- `draw.py`, the Python + PIL script that draws it, deterministically.
- `main.ts`, the entrypoint: copies `entry.png` to the output directory.

## How it runs

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

That writes `out/entry.png`. With no `MAKEFUN_OUTPUT_DIR` set, it writes
to `/output` instead. To redraw the image from scratch:

```sh
python3 draw.py
```

## Referral

Built on [make.fun](https://make.fun/r/s27wgn68).
