# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/arsheearanjbar-sudo/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/arsheearanjbar-sudo/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image summing up the world news of Monday 23 November 2026, drawn as a newspaper front page; main.ts copies the pre-rendered entry.png to /output/entry.png (and verifies the copy byte-for-byte with SHA-256); rendered with PIL so every headline is typeset exactly — no image generator was used for text.

## Run it

```sh
node main.ts   # Node 22; writes /output/entry.png
```

## The news in the image

The board was redrawn in the evening of 23 November 2026 with the full day's news. Morning stories updated: the cricket draw, the Indonesia toll at 24 dead, and the Modi–Nepal package; the Sparta II and the Korea minister story were dropped as no longer the day's news. Every item was verified against a live source before use.

| # | Headline as shown | Fact stated | Source |
|---|---|---|---|
| 1 | COP31 ends with no deal | UN climate talks in Antalya collapse without a political agreement; the final draft drops any mention of fossil fuels; the UN chief voices "profound frustration" as the EU refuses to endorse the weak text. | Reuters — https://www.reuters.com/sustainability/cop/can-climate-diplomacy-build-collapse-cop31-2026-11-22/ ; Al Jazeera — https://www.aljazeera.com/amp/news/2026/11/22/countries-react-after-cop31-climate-talks-end-in-collapse |
| 2 | India post record 720/9 — but NZ hold on for a draw | Mitchell and Phillips bat out day five in Wellington as New Zealand finish 239/5 after India's record total. | CricTracker — https://www.crictracker.com/cricket-news/nz-vs-ind-2026-new-zealand-vs-india-highlights-review-1st-test-8936/ ; Times of India |
| 3 | Modi gives Nepal Rs 24,000-crore package | PM Modi announces a Rs 24,000-crore development package for Nepal, signs eight pacts, and flags a new Ayodhya–Janakpur train. | NDTV ; The Hindu |
| 4 | 24 dead confirmed in Indonesia factory fire | Rescuers search for about 30 people still missing after the weekend blaze at a candy factory in Banten. | Reuters |
| 5 | Trump warns of Iran strikes after New Year | Trump says he is inclined to resume major strikes if no deal is reached, and threatens vessels defying the Gulf blockade. | Fox News via NDTV ; Dawn |
| 6 | Tajikistan quits ICC on day of Putin visit | Tajikistan becomes the fourth country to begin withdrawing from the court since the US push. | Reuters via The Hindu |
| 7 | 450 German schools hit by emailed bomb threats | Schools across Germany — and Denmark — receive emailed threats; police say there is no credible danger. | Reuters |

## Files

- `entry.png` — the image (1024x1024, 140,868 bytes)
- `main.ts` — entrypoint
- `draw_news_evening.py` — the PIL script that renders entry.png (evening redraw with the full day's news)
- `draw_news.py` — the morning render script
- `LICENSE` — MIT
- `README.md` — this file

<sub>Entered on [make.fun](https://make.fun/?ref=sh01ee1y&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
