import { W, H, RGB, hex, sat, lerp, easeOut, easeInOut, backOut, makeFB, target, quantize, textBlock, glyphRun, put, light, darken, Line } from "./gfx";
import { Label } from "./art";
import { kitchen, cake, fishPlate, iceCream, cat, CatPose, tongueBg, socket, sugarCube, umami, hearts, COUNTER } from "./art7";
import timing from "./timing.json";

export { W, H };
const B = timing.beats, T = timing as any;
const fbA = makeFB(), fbB = makeFB();
type Txt = [string, string][][];
export const BEATS: Line[][] = (timing.texts as unknown as Txt).map(lines => lines.map(segs => ({ segs: segs.map(([t, c]) => (c ? { t, c } : { t })) })));
type Out = { ui: number; zoom?: number; zx?: number; zy?: number; shx?: number; shy?: number };
const CX = 76, PROP = 196;
const pose = (p: Partial<CatPose>): CatPose => ({ lean: 0, tail: 1, eyes: "open", tongue: 0, lick: 0, headTilt: 0, mouth: "smile", ear: 0, ...p });
const shake = (f: number, at: number, len = 8, amp = 2.5) => (f >= at && f < at + len ? Math.sin(f * 2.7) * amp * (1 - (f - at) / len) : 0);

// 1. hook: the cat sniffs the cake... and pulls a disgusted face
const s1 = (f: number, L: Label[]): Out => {
  kitchen(f, L);
  cake(PROP, COUNTER);
  const bleh = f >= T.bleh;
  const lean = bleh ? lerp(0.9, -0.15, easeOut((f - T.bleh) / 8)) : 0.9 + Math.sin(f * 0.9) * 0.05 * (f > T.sniff - 10 ? 1 : 0);
  cat(CX, COUNTER, 1, pose({ lean, eyes: bleh ? "squint" : "open", tongue: bleh ? easeOut((f - T.bleh) / 6) : 0, mouth: bleh ? "bleh" : "smile", headTilt: bleh ? -0.15 : 0.05, ear: bleh ? -1 : 0.5 }), f);
  return { ui: L.length, zoom: lerp(1.3, 1, backOut(f / 16)), zx: 140, zy: 330, shx: shake(f, T.bleh), shy: shake(f + 2, T.bleh) };
};

// 2. on the tongue: sugar bounces off the broken sweet receptor
const s2 = (f: number, L: Label[]): Out => {
  tongueBg(f);
  socket(80, 300, true, 0, L, "SWEET", "#ff7ab0");
  socket(192, 300, false, 0, L, "UMAMI", "#ffb347");
  for (const at of T.bounce as number[]) {
    const t = f - at;
    if (t < -30 || t > 40) continue;
    if (t < 0) sugarCube(80, lerp(140, 280, easeInOut((t + 30) / 30)), t * 0.05);
    else sugarCube(80 - t * 2.2, 280 - t * 4 + t * t * 0.14, t * 0.3);
  }
  return { ui: L.length, shx: (T.bounce as number[]).reduce((a: number, at: number) => a + shake(f, at, 6, 2), 0) };
};

// 3a. umami molecules click into the working receptor; 3b. the cat finds the fish
const s3 = (f: number, L: Label[]): Out => {
  if (f < T.fishCut) {
    tongueBg(f);
    const docked = (T.dock as number[]).filter((d: number) => f >= d).length;
    socket(80, 300, true, 0, L, "SWEET", "#ff7ab0");
    socket(192, 300, false, sat(docked * 0.6) * (0.7 + 0.3 * Math.sin(f * 0.5)), L, "UMAMI", "#ffb347");
    (T.dock as number[]).forEach((d: number, i: number) => { const t = f - d; if (t < -26) return; const y = t < 0 ? lerp(140, 296, easeInOut((t + 26) / 26)) : 296 + Math.sin(t * 0.4) * 1.5 - i * 6; umami(192 + (i ? 8 : -8) * (t > 0 ? 1 : 0), y, t < 0 ? t * 0.08 : 0); });
    return { ui: L.length };
  }
  kitchen(f, L);
  const l = f - T.fishCut;
  fishPlate(PROP, COUNTER, f);
  cat(CX, COUNTER, 1, pose({ lean: 0.6 + Math.sin(l * 0.25) * 0.08, eyes: "wide", mouth: "o", tail: 2.5, ear: 1, headTilt: 0.08 }), f);
  hearts(CX + 30, COUNTER - 150, l * 0.02);
  return { ui: L.length, zoom: 1.12, zx: 140, zy: 330 };
};

// 4. ice cream: it licks happily — for the fat, not the sugar
const s4 = (f: number, L: Label[]): Out => {
  const l = f - B[3];
  kitchen(f, L);
  iceCream(140, COUNTER, sat(l / 110));
  const lick = Math.max(0, Math.sin(l * 0.35));
  cat(CX + 6, COUNTER, 1, pose({ lean: 0.6, duck: 1, tongue: lick * 0.8, eyes: "closed", mouth: "smile", tail: 1.5, ear: 0.5 }), f);
  if (l > 30) L.push({ s: "FAT + MILK", x: 176, y: COUNTER - 70, c: "#ffe14e" });
  if (l > 50) L.push({ s: "SUGAR: ???", x: 176, y: COUNTER - 54, c: "#ff7ab0" });
  return { ui: L.length, zoom: 1.08, zx: 150, zy: 340 };
};

// 5. the ask; then lean back to the cake so it loops into frame 1
const s5 = (f: number, L: Label[]): Out => {
  const l = f - B[4], back = easeInOut((f - (B[5] - 24)) / 22);
  kitchen(f, L);
  cake(PROP, COUNTER);
  cat(CX, COUNTER, 1, pose({ lean: lerp(-0.1, 0.9, back), eyes: back > 0.3 ? "open" : l > 20 && l < 50 ? "wink" : "open", tail: 2, mouth: "smile", ear: 0.4, headTilt: lerp(-0.12, 0.05, back) }), f);
  return { ui: L.length, zoom: lerp(1, 1.3, back), zx: 140, zy: 330 };
};

const SCENES = [s1, s2, s3, s4, s5];
export const beatIndex = (f: number) => { let i = 0; while (i < SCENES.length - 1 && f >= B[i + 1]) i++; return i; };

const draw = (f: number, L: Label[]) => {
  light.dir = [-0.55, -0.6, 0.6]; light.rimDir = [0.8, -0.45]; light.tint = [1, 1, 1]; light.rim = hex("#ffd890"); light.rimAmt = 0.75;
  target(fbA);
  const o = SCENES[beatIndex(f)](f, L);
  const z = o.zoom ?? 1, sx = o.shx ?? 0, sy = o.shy ?? 0;
  if (Math.abs(z - 1) > 1e-3 || sx || sy) {
    const cx = o.zx ?? 135, cy = o.zy ?? 240;
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      const X = Math.floor(cx + (x + 0.5 - cx) / z + sx), Y = Math.floor(cy + (y + 0.5 - cy) / z + sy), i = (y * W + x) * 3;
      const j = (Math.min(H - 1, Math.max(0, Y)) * W + Math.min(W - 1, Math.max(0, X))) * 3;
      fbB[i] = fbA[j]; fbB[i + 1] = fbA[j + 1]; fbB[i + 2] = fbA[j + 2];
    }
    fbA.set(fbB);
    for (let k = 0; k < o.ui; k++) { const l = L[k]; l.x = Math.round(cx + (l.x - cx - sx) * z); l.y = Math.round(cy + (l.y - cy - sy) * z); }
  }
  const d = hex("#1a0a20");
  darken(56, 72, d, 0, 0.55); for (let y = 72; y < 134; y++) for (let x = 0; x < W; x++) put(x, y, d, 0.55); darken(134, 150, d, 0.55, 0);
};

// diagonal pixel-tile wipe with a pink edge
const CUTS = [B[1], B[2], T.fishCut, B[3], B[4]];
const HALF = 6, TILE = 10;
export const CHARS_PER_FRAME = 1.6;
const flush = (out: Uint8ClampedArray, L: Label[]) => { for (const l of L) if (l.s) glyphRun(out, l.s, l.x, l.y, hex(l.c), l.size ?? 16, !l.plain); };

export const renderFrame = (f: number, out: Uint8ClampedArray) => {
  const L: Label[] = [];
  const cut = CUTS.find((c: number) => f >= c - HALF && f < c + HALF);
  draw(f, L);
  if (cut !== undefined) {
    const cur = fbA.slice(), lc = L.slice();
    L.length = 0; draw(f < cut ? cut : cut - 1, L);
    const other = fbA.slice(), lo = L.slice();
    const prev = f < cut ? cur : other, next = f < cut ? other : cur;
    const p = (f - (cut - HALF)) / (HALF * 2), mixed = new Float32Array(W * H * 3), edge: RGB = hex("#ff7ab0");
    const span = (W + H) / TILE;
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      const tdiag = (Math.floor(x / TILE) + Math.floor(y / TILE)) / span, i = (y * W + x) * 3;
      const k = p * 1.25 - tdiag * 0.25 - tdiag;
      const src = k > 0 ? next : prev;
      mixed[i] = src[i]; mixed[i + 1] = src[i + 1]; mixed[i + 2] = src[i + 2];
      if (k > 0 && k < 0.06) { mixed[i] = edge[0]; mixed[i + 1] = edge[1]; mixed[i + 2] = edge[2]; }
    }
    quantize(mixed, out);
    flush(out, p > 0.5 ? (f < cut ? lo : lc) : (f < cut ? lc : lo));
  } else { quantize(fbA, out); flush(out, L); }
  const bi = beatIndex(f), lf = f - B[bi], lines = BEATS[bi].map((l, i) => (bi === 0 && i === 1 ? { ...l, big: true } : l));
  if (bi === 0) textBlock(out, lines, 80, 999);
  else if (lf >= 3 && (bi === BEATS.length - 1 || B[bi + 1] - f > 3)) textBlock(out, lines, 88, (lf - 3) * CHARS_PER_FRAME);
};
