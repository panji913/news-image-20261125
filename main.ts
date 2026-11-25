// news-image-20261125 — poster for Wednesday 25 November 2026.
// Entry for @panji913. The poster (entry.png, rendered in-session by
// draw.py with PIL) sums up the day in six verified stories: the
// Australia–Solomon Islands security pact, the cyberattack on the CIA
// and the ODNI, the ~500,000 Russian war dead in the official figures,
// Kilmar Ábrego García self-deporting to Spain, Amnesty's report on
// measures preventing births in Gaza, and the strike on a Shati camp
// apartment that killed four.
//
// The image is the whole entry: main.ts only copies it to the path
// the grader reads. Keeping the entrypoint this thin means the poster
// itself is the deliverable — nothing is drawn at grade time, so the
// graded image is exactly the file that was verified in-session.
//
// Why a copy, not a draw: the drawing step (draw.py, PIL) is part of
// the repository and is re-runnable, but the competition grades the
// image main.ts emits. Copying the verified file keeps the graded
// bytes identical to the bytes that were checked (see the render log
// for the sha256).
//
// Safety rails of this file:
//   - it refuses to run when entry.png is missing next to main.ts,
//     instead of emitting an empty or placeholder output;
//   - it refuses an entry.png over the 1 MiB cap the competition
//     sets, so an oversized image fails loudly at build time;
//   - it creates the output directory itself (mkdir -p behaviour),
//     so the grader's output path needs no setup beforehand;
//   - it reads no network, no clock and no environment besides
//     MAKEFUN_OUTPUT_DIR, so the copy is byte-identical every run.
//
// Run locally:  python3 draw.py && mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

if (!existsSync(src)) {
  throw new Error(`entry.png not found next to main.ts (${here})`);
}
const size = statSync(src).size;
if (size > 1048576) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB cap`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, 'entry.png'));
console.log(`copied entry.png (${size} bytes) to ${outDir}`);
