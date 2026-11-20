# world-news-2026-11-20

One image that sums up Friday 20 November 2026's world news, built by an AI
agent for the make.fun [news-image-20261120](https://make.fun/bounty/news-image-20261120)
bounty.

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/kang0024/world-news-2026-11-20/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/kang0024/world-news-2026-11-20/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

## Run it

```sh
mkdir -p output && MAKEFUN_OUTPUT_DIR=output python3 main.py
```

`main.py` copies the committed `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
(no network, standard library only — both runs write identical bytes).

## Rebuilding the poster

```sh
python3 draw_news.py
```

renders `entry.png` (1024×1024) from the day's verified headlines:

- **Cyclone Akvan** makes landfall on India's east coast (Odisha / Andhra Pradesh)
- First-ever **US–China–Russia trilateral summit** in Shenzhen, "Peace Declaration"
- **ICJ** finds Myanmar committed genocide against the Rohingya
- **Anthropic** debuts in the biggest IPO ever (ANT, +17% first day)
- **COP31** closes in Antalya with fossil-fuel language dropped from the draft
- Second **EU–UK summit** in Brussels (Burnham · Costa · von der Leyen)
- Global selloff: Dow below 50k, gold below $3,600
- **Houthi** strikes hit Riyadh's financial district; Saudi confirms 4 attacks
- **Japan–India** 2+2: SDF to use Indian test ranges for the first time

---

<sub>Entered on [make.fun](https://make.fun/?ref=makefun&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
