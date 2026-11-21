# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/rapppae/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/rapppae/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A one-image summary of the world's news of Saturday 21 November 2026, pre-rendered by the Python renderer in `draw.py`: a Russian missile lands in Poland during Moscow's biggest bombardment of Ukraine, Anthropic's shares slide 8.5% on their second day as the AI sell-off goes global, Kushner floats a NATO path for Kyiv, and Kosovo's ex-president Thaci is jailed for 17 months.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Writes `out/entry.png` (1024×1024 PNG, under 1 MiB). Deterministic: two runs write the same bytes. The entrypoint is standard library only, so it runs in the grader's sandbox: it copies the pre-rendered `entry.png` to the output. `draw.py` is the renderer that produced that image; its fonts are bundled in `assets/` (DejaVu, OFL).

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
