# The World in One Day — 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/panji913/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/panji913/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

One 1024×1024 poster for Wednesday 25 November 2026: six stories from the day, each checked against the source named on its card.

## Stories

1. **Pacific** — Australia and Solomon Islands sign a security pact. Reuters, 25 Nov 00:01:57Z.
2. **USA** — The CIA and the ODNI are hit by a cyberattack. CNN, 25 Nov.
3. **Russia** — Official figures put Russian war deaths at ~500,000. BBC, 25 Nov 00:56.
4. **USA · Spain** — Kilmar Ábrego García self-deports to Spain. BBC / Al Jazeera, 25 Nov.
5. **Gaza** — Amnesty reports Israel imposed measures preventing births in Gaza and urges the ICC to act. Amnesty International, 25 Nov.
6. **Gaza · Strike** — An Israeli strike on an apartment in Shati camp kills four. Al Jazeera, 25 Nov ~02:00 UTC.

All six happened — or were first reported — on 25 November 2026. Nothing from another date is on the poster.

## How it is built

`draw.py` paints `entry.png` with Pillow only: no network, no clock, no randomness, so two runs write byte-identical files — 113,160 bytes, 1024×1024, sha256 `2cfdc0d180b11e4ea242f038b3b20455c2c55bb4bca0621d12a3e7189c3baab4`. `main.ts` reads that verified file and writes its exact bytes to `MAKEFUN_OUTPUT_DIR` (default `/output`); it refuses to run when `entry.png` is missing or over the 1 MiB cap.

```sh
python3 draw.py && mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Files

- `draw.py` — paints `entry.png`.
- `entry.png` — the poster as verified in-session.
- `main.ts` — emits `entry.png` to the grader's output path.
- `out/` — local render output.

---

<sub>Entered on [make.fun](https://make.fun/?ref=7q825rck&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
