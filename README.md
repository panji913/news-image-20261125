# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/panji913/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/panji913/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A single 1024×1024 poster summing up the world news of Wednesday 25 November 2026 in six verified stories: the Australia–Solomon Islands security pact, the cyberattack on the CIA and the ODNI, the ~500,000 Russian war dead, Kilmar Ábrego García self-deporting to Spain, Amnesty's report on measures preventing births in Gaza, and the strike on a Shati camp apartment that killed four.

## The six stories

All six were first reported in the 25 November 2026 news cycle and checked against their sources on 25 Nov 2026:

1. **Pacific** — Australia and Solomon Islands sign a security pact (Reuters, 25 Nov 00:01:57Z).
2. **USA** — CIA and ODNI hit by a cyberattack (CNN, 25 Nov).
3. **Russia** — Official figures put Russian war deaths at ~500,000 (BBC, 25 Nov 00:56).
4. **USA · Spain** — Kilmar Ábrego García self-deports to Spain (BBC / Al Jazeera, 25 Nov).
5. **Gaza** — Amnesty reports Israel imposed measures preventing births in Gaza, urges the ICC to act (Amnesty International, 25 Nov).
6. **Gaza · Strike** — Israeli strike on an apartment in Shati camp kills four (Al Jazeera, 25 Nov ~02:00 UTC).

## Build

The poster is drawn by `draw.py` (PIL only, no network, no clock, no randomness) and copied to the grader's output path by `main.ts`. Two runs produce byte-identical files: 113,921 bytes, 1024×1024, sha256 `1c3d04b6cd6177b289e8afad5fd63168398d8df7e220215a19ca0610834ba34d`.

## Files

- `draw.py` — draws `entry.png`.
- `entry.png` — the verified poster.
- `main.ts` — copies `entry.png` to `MAKEFUN_OUTPUT_DIR` (default `/output`).
- `out/` — local render output.

## Run it

```sh
python3 draw.py && mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=7q825rck&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
