// news-image-20261123: copies the pre-rendered front page (entry.png)
// to the grader's output directory.
//
// The image is drawn at build time by draw_news.py (PIL) so every
// headline is typeset exactly; this program only places the finished
// file where the competition requires it. After copying it verifies
// the copy byte-for-byte (SHA-256) against the source, so a truncated
// or corrupted write fails loudly instead of passing silently.
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = join(repoDir, "entry.png");
const target = join(outDir, "entry.png");

function sha256(path: string): string {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

const sourceHash = sha256(source);
const targetHash = sha256(target);
if (sourceHash !== targetHash) {
  throw new Error(
    `entry.png copy failed integrity check: source ${sourceHash} != output ${targetHash}`,
  );
}
console.log(
  `entry.png written to ${target} (${statSync(target).size} bytes, sha256 ${targetHash})`,
);
