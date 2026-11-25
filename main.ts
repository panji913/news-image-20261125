// news-image-20261125 — poster for Wednesday 25 November 2026.
// Entry for @panji913. The poster is entry.png, painted in-session
// by draw.py with Pillow: six stories verified from the 25 November
// 2026 news cycle — the Australia–Solomon Islands security pact, the
// cyberattack on the CIA and the ODNI, the ~500,000 Russian war dead
// in the official figures, Kilmar Ábrego García self-deporting to
// Spain, Amnesty's report on measures preventing births in Gaza, and
// the strike on a Shati camp apartment that killed four.
//
// main.ts does one job: it reads the verified entry.png beside it
// and writes those exact bytes to the grader's output folder. The
// entrypoint draws nothing at grade time, so the graded image is
// byte-for-byte the image that was checked in-session (see the
// render log for the sha256).
//
// Why read-and-write instead of a copy call: the guardrails below
// are the point. The script bails out when entry.png is missing
// rather than emitting an empty file, bails out when the file is
// over the competition's 1 MiB cap, makes the output folder itself,
// and touches nothing else — no network, no clock, no environment
// besides MAKEFUN_OUTPUT_DIR — so every run emits identical bytes.
//
// Run locally:  python3 draw.py && mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import * as fs from 'node:fs';
import * as path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

if (!fs.existsSync(src)) {
  throw new Error(`entry.png not found next to main.ts (${here})`);
}
const bytes = fs.readFileSync(src);
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
}

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, 'entry.png'), bytes);
console.log(`wrote entry.png (${bytes.length} bytes) to ${outDir}`);
