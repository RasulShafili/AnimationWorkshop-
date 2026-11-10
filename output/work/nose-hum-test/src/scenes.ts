import { W, H, RGB, hex, mix, sat, lerp, easeOut, easeInOut, backOut, makeFB, target, quantize, textBlock, glyphRun, put, light, darken, Line } from "./gfx";
import { Label } from "./art";
import { pinchHero, waves, section, gauge, stopwatch, sparkBurst, stage, lightTable, PINCH_ANGLE } from "./art5";
import timing from "./timing.json";

export { W, H };
const B = timing.beats, PINCH = timing.pinch, STOP = timing.stop, REL = timing.release;
const fbA = makeFB(), fbB = makeFB();
type Txt = [string, string][][];
export const BEATS: Line[][] = (timing.texts as unknown as Txt).map(lines => lines.map(segs => ({ segs: segs.map(([t, c]) => (c ? { t, c } : { t })) })));
const HX = 128, FEET = 372, HEADY = FEET - 146, NOSE: [number, number] = [HX, HEADY + 8];
const LOOP_ZOOM = 1.35;
// zoom/rot/shake are applied to the finished world image; `post` draws screen-space UI afterwards
type Out = { ui: number; zoom?: number; zx?: number; zy?: number; shx?: number; shy?: number; post?: () => void };
const shake = (f: number, at: number, len = 8, amp = 3) => (f >= at && f < at + len ? Math.sin(f * 2.7) * amp * (1 - (f - at) / len) : 0);
const fmt = (t: number) => `${Math.max(0, t).toFixed(1)} S`;

// 1. hook: humming on stage, then the pinch kills the sound
const s1 = (f: number, L: Label[]): Out => {
  stage(f, 1, L);
  const arm = f < PINCH ? 0.2 : lerp(0.2, PINCH_ANGLE, easeOut((f - PINCH) / 8));
  const pinched = f >= PINCH + 6, amp = f < PINCH + 6 ? 1 : sat(1 - (f - PINCH - 6) / 24);
  pinchHero(HX, FEET, arm, pinched ? sat((f - PINCH - 6) / 24) : 0, pinched ? { eye: "wide", mouth: "flat" } : { eye: "closed", mouth: "smile" });
  waves(NOSE[0], NOSE[1], amp, f);
  sparkBurst(HX + 40, HEADY - 40, (f - PINCH - 30) / 16, hex("#ff4a6a"));
  if (f > PINCH + 30) L.push({ s: "?!", x: HX + 34, y: HEADY - 58, c: "#ff4a6a", size: 32 });
  const z = lerp(LOOP_ZOOM, 1, backOut(f / 16));
  return { ui: L.length, zoom: z, zx: HX, zy: HEADY + 20, shx: shake(f, PINCH + 6), shy: shake(f + 3, PINCH + 6) };
};

// 2. the test: close-up, timer runs until the hum dies
const s2 = (f: number, L: Label[]): Out => {
  const l = f - B[1];
  stage(f, 1, L);
  const t = Math.min(f, STOP) - B[1] - 6, sec = t / 30, done = f >= STOP;
  const amp = done ? 0 : sec < 1 ? 1 : sat(1 - (sec - 1) / 1.2);
  pinchHero(HX, FEET, PINCH_ANGLE, sat(l / 60), { eye: done ? "wide" : "open", mouth: "flat", blink: !done && (l + 30) % 70 < 4 });
  waves(NOSE[0], NOSE[1], amp, f);
  return {
    ui: L.length, zoom: 1.6, zx: HX, zy: HEADY + 14, shx: shake(f, STOP, 10, 4), shy: shake(f + 2, STOP, 10, 4),
    post: () => { stopwatch(212, 150, fmt(sec), done, L); sparkBurst(212, 166, (f - STOP) / 14, hex("#ff4a6a")); },
  };
};

// 3. inside: air piles up, the vocal folds stall
const s3 = (f: number, L: Label[]): Out => {
  const l = f - B[2], p = easeOut(l / 80);
  lightTable(f);
  section(120, 272, 1.12, p, 0, 1 - p, 1, f, L);
  gauge(222, 428, p, L);
  if (l > 10) L.push({ s: "AIR", x: 54, y: 404, c: "#bff6ff" });
  if (l > 36) L.push({ s: "BLOCKED", x: 186, y: 228, c: "#ff5a7a" });
  if (l > 56) L.push({ s: "NO SOUND", x: 146, y: 364, c: "#ffe600" });
  return { ui: L.length };
};

// 4. let go: air streams out, the hum is back
const s4 = (f: number, L: Label[]): Out => {
  const l = f - B[3], fin = 1 - easeInOut((f - REL) / 14), p = 1 - sat((f - REL) / 20), flow = sat((f - REL - 8) / 12);
  lightTable(f);
  section(120, 272, 1.12, p, flow, flow, fin, f, L);
  gauge(222, 428, p, L);
  if (flow > 0.5) { L.push({ s: "HUM!", x: 214, y: 268, c: "#ffe600", size: 24 }); L.push({ s: "AIR OUT", x: 170, y: 300, c: "#5ce1e6" }); }
  return { ui: L.length };
};

// 5. the question, then ease back into frame 1 so the reel loops
const s5 = (f: number, L: Label[]): Out => {
  const l = f - B[4], back = easeInOut((f - (B[5] - 26)) / 24);
  stage(f, 1, L);
  const arm = lerp(2.5 + Math.sin(l * 0.3) * 0.25, 0.2, back);
  pinchHero(HX, FEET, arm, 0, back > 0.5 ? { eye: "closed", mouth: "smile" } : { eye: "open", mouth: "grin", blink: (l + 10) % 60 < 4 });
  waves(NOSE[0], NOSE[1], back, f);
  const z = lerp(1, LOOP_ZOOM, back);
  return {
    ui: L.length, zoom: z, zx: HX, zy: HEADY + 20,
    post: back < 0.3 ? () => stopwatch(210, 168, (l >> 3) % 2 ? "?.? S" : "?.? S", (l >> 3) % 2 === 0, L) : undefined,
  };
};

const SCENES = [s1, s2, s3, s4, s5];
export const beatIndex = (f: number) => { let i = 0; while (i < SCENES.length - 1 && f >= B[i + 1]) i++; return i; };

const draw = (f: number, L: Label[]) => {
  light.dir = [-0.5, -0.62, 0.6]; light.rimDir = [0.8, -0.45]; light.tint = [1, 1, 1]; light.rim = hex("#ffd27a"); light.rimAmt = 0.8;
  target(fbA);
  const o = SCENES[beatIndex(f)](f, L);
  const z = o.zoom ?? 1, sx = o.shx ?? 0, sy = o.shy ?? 0;
  if (Math.abs(z - 1) > 1e-3 || sx || sy) {
    const cx = o.zx ?? 135, cy = o.zy ?? 240;
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      // keep the zoom anchor at the same place on screen
      const X = Math.floor(cx + (x + 0.5 - cx) / z + sx), Y = Math.floor(cy + (y + 0.5 - cy) / z + sy), i = (y * W + x) * 3;
      const j = (Math.min(H - 1, Math.max(0, Y)) * W + Math.min(W - 1, Math.max(0, X))) * 3;
      fbB[i] = fbA[j]; fbB[i + 1] = fbA[j + 1]; fbB[i + 2] = fbA[j + 2];
    }
    fbA.set(fbB);
    // world labels: move them with the zoom
    for (let k = 0; k < o.ui; k++) { const l = L[k]; l.x = Math.round(cx + (l.x - cx - sx) * z); l.y = Math.round(cy + (l.y - cy - sy) * z); }
  }
  const d = hex("#14020e");
  darken(58, 74, d, 0, 0.55); for (let y = 74; y < 134; y++) for (let x = 0; x < W; x++) put(x, y, d, 0.55); darken(134, 150, d, 0.55, 0);
  o.post?.();
};

// stage-shutter transition: horizontal bands slide open top to bottom with a gold edge
const CUTS = [B[1], B[2], B[3], B[4]];
const HALF = 6, BAND = 60;
export const CHARS_PER_FRAME = 1.6;
const flush = (out: Uint8ClampedArray, L: Label[]) => { for (const l of L) if (l.s) glyphRun(out, l.s, l.x, l.y, hex(l.c), l.size ?? 16, !l.plain); };

export const renderFrame = (f: number, out: Uint8ClampedArray) => {
  const L: Label[] = [];
  const cut = CUTS.find(c => f >= c - HALF && f < c + HALF);
  draw(f, L);
  if (cut !== undefined) {
    const cur = fbA.slice(), lc = L.slice();
    L.length = 0; draw(f < cut ? cut : cut - 1, L);
    const other = fbA.slice(), lo = L.slice();
    const prev = f < cut ? cur : other, next = f < cut ? other : cur;
    const p = (f - (cut - HALF)) / (HALF * 2), mixed = new Float32Array(W * H * 3), gold: RGB = hex("#ffd84e");
    for (let y = 0; y < H; y++) {
      const band = Math.floor(y / BAND), frac = sat((p - band * 0.06) / 0.52), edge = Math.floor(frac * BAND), r = y % BAND;
      for (let x = 0; x < W; x++) {
        const i = (y * W + x) * 3, src = r < edge ? next : prev;
        mixed[i] = src[i]; mixed[i + 1] = src[i + 1]; mixed[i + 2] = src[i + 2];
        if (frac > 0 && frac < 1 && (r === edge || r === edge + 1)) { mixed[i] = gold[0]; mixed[i + 1] = gold[1]; mixed[i + 2] = gold[2]; }
      }
    }
    quantize(mixed, out);
    flush(out, p > 0.5 ? (f < cut ? lo : lc) : (f < cut ? lc : lo));
  } else { quantize(fbA, out); flush(out, L); }
  const bi = beatIndex(f), lf = f - B[bi], lines = BEATS[bi].map((l, i) => (bi === 0 && i === 1 ? { ...l, big: true } : l));
  if (bi === 0) textBlock(out, lines, 80, 999);
  else if (lf >= 3 && (bi === BEATS.length - 1 || B[bi + 1] - f > 3)) textBlock(out, lines, 88, (lf - 3) * CHARS_PER_FRAME);
};
