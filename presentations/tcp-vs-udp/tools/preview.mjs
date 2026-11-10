// Fast no-browser preview: node tools/preview.mjs out.png cols scale f1 f2 ...
import { build } from "esbuild";
import { spawnSync } from "node:child_process";
import { pathToFileURL } from "node:url";
import path from "node:path";
const [out, cols, scale, ...frames] = process.argv.slice(2);
const tmp = path.join(path.dirname(out), "_bundle.mjs");
await build({ entryPoints: ["src/scenes.ts"], bundle: true, format: "esm", platform: "node", outfile: tmp, loader: { ".json": "json" }, logLevel: "error" });
const { renderFrame, W, H } = await import(pathToFileURL(tmp).href + "?" + Date.now());
const fr = frames.map(Number), buf = Buffer.alloc(W * H * 4 * fr.length);
const t0 = Date.now();
fr.forEach((f, i) => { const o = new Uint8ClampedArray(W * H * 4); renderFrame(f, o); buf.set(o, i * W * H * 4); });
console.log(`${fr.length} frames, ${(Date.now() - t0) / fr.length | 0} ms/frame`);
const r = spawnSync("ffmpeg", ["-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", `${W}x${H}`, "-r", "1", "-i", "-",
  "-vf", `scale=iw*${scale}:ih*${scale}:flags=neighbor,tile=${cols}x${Math.ceil(fr.length / cols)}:padding=4`, "-frames:v", "1", out], { input: buf });
if (r.status) console.error(r.stderr.toString());
