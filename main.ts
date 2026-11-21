import * as fs from "node:fs";
import * as path from "node:path";
import * as crypto from "node:crypto";
import { fileURLToPath } from "node:url";

// Copy the pre-rendered entry image to the output directory, then verify
// the copied bytes are identical to the source. Deterministic: the output
// bytes are always identical to entry.png.
// Output dir: $MAKEFUN_OUTPUT_DIR when set (local runs), else /output
// (the grader's writable output directory).
const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const dest = path.join(outDir, "entry.png");

function sha256(file: string): string {
  return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
}

try {
  fs.mkdirSync(outDir, { recursive: true });
  fs.copyFileSync(src, dest);
  const srcHash = sha256(src);
  const destHash = sha256(dest);
  if (srcHash !== destHash) {
    console.error(`byte mismatch: ${src} (${srcHash}) != ${dest} (${destHash})`);
    process.exit(1);
  }
  console.log(`wrote ${dest} (sha256 ${destHash})`);
} catch (err) {
  console.error(
    `failed to write ${dest}: ${err instanceof Error ? err.message : err}`,
  );
  process.exit(1);
}
