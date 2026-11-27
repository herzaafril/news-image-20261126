// news-image-20261126 entry program (Node 22, standard library only).
// Validates the entry.png beside this file (exists, non-empty, at most 1 MiB,
// PNG magic bytes, at most 1024x1024 from the IHDR), then copies it
// byte-identically to /output/entry.png. Outside the grader's container,
// MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const MAX_BYTES = 1024 * 1024; // 1 MiB
const MAX_DIM = 1024;

const src = new URL('./entry.png', import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const dest = join(outDir, 'entry.png');

const buf = readFileSync(src);
if (buf.length === 0) throw new Error('entry.png is empty');
if (buf.length > MAX_BYTES) throw new Error(`entry.png is ${buf.length} bytes, over the 1 MiB limit`);

const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
for (let i = 0; i < PNG_MAGIC.length; i++) {
  if (buf[i] !== PNG_MAGIC[i]) throw new Error('entry.png does not start with the PNG magic bytes');
}

// IHDR is the first chunk: 8-byte signature, 4-byte length, "IHDR",
// then width and height as big-endian uint32 at offsets 16 and 20.
if (buf.length < 24 || buf.toString('ascii', 12, 16) !== 'IHDR') {
  throw new Error('entry.png has no IHDR chunk');
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width > MAX_DIM || height > MAX_DIM) {
  throw new Error(`entry.png is ${width}x${height}, over the ${MAX_DIM}x${MAX_DIM} limit`);
}

copyFileSync(src, dest);

// Post-copy check: the file that landed must be the same size as the source.
const landed = statSync(dest).size;
if (landed !== buf.length) {
  throw new Error(`copied entry.png is ${landed} bytes, expected ${buf.length}`);
}
console.log(`entry.png ${width}x${height}, ${buf.length} bytes -> ${dest}`);
