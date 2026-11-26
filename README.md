[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Teachanjc/news-image-20261125-bot/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Teachanjc/news-image-20261125-bot/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# news-image-20261125-bot

A newspaper front page summing up the world's news of Wednesday 25 November 2026 in one image: two oil tankers ablaze after striking mines in the Strait of Hormuz, a Hamas security chief killed in Gaza, Ukrainian drones setting two Russian refineries on fire, Huawei convicted in a US court, and Asian markets tumbling while the Dow closed above 50,000 for the first time.

The image is drawn programmatically with Pillow (fixed fonts, fixed text, no network, no randomness) and shipped as `entry.png`; `main.py` copies it to `/output/entry.png`, so two runs produce byte-identical output.

## The five stories

1. **Hormuz — two tankers ablaze.** Iran's Revolutionary Guard said two oil tankers struck naval mines in the Strait of Hormuz and caught fire. The vessels were on an unauthorised route through the strait, it said, as fears grow for shipping and oil supplies.
2. **Yemen — Houthis hit a Saudi refinery.** Yemen's Houthis said they attacked Saudi Arabia's Ras Tanura oil refinery, a day after a strike on a Riyadh skyscraper injured 11 people.
3. **Gaza — Hamas security chief killed.** Israel killed Mohammad Abuelouf, a Hamas colonel who ran its internal security service, with his wife and two children, Gaza medics said.
4. **Ukraine war — refineries ablaze, leaked death toll.** Ukrainian drones set two Rosneft refineries in Samara alight overnight. Leaked Russian figures analysed by the BBC put Russian military deaths since 2022 at 490,334.
5. **United States, tech — Huawei convicted.** A Brooklyn jury found Huawei guilty of conspiring to steal trade secrets and bank fraud, but cleared it of racketeering, after a trial of more than two months.

The strip at the foot adds four more items reported that day: Asian markets tumbling (Seoul's KOSPI down 6.16%, Tokyo's Nikkei down 2.78%), the Houthi strike on Riyadh, the Australia–Solomon Islands treaty barring any foreign military base, and China's Shenzhou-24 docking with Tiangong carrying Pakistan's first astronaut. The footer notes two more: the COP31 climate talks ending without a deal, and Trump awarding Rudy Giuliani the Medal of Freedom.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To redraw the image from scratch:

```sh
python3 draw.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=teachan&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
