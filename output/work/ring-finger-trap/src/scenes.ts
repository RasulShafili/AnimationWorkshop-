import { W, H, RGB, hex, sat, lerp, easeOut, easeIn, easeInOut, backOut, makeFB, target, quantize, textBlock, glyphRun, put, light, darken, Line } from "./gfx";
import { Label } from "./art";
import { desk, hand, tipOf, xrayBg, xrayHand, padlock, sparkle, HandState } from "./art6";
import timing from "./timing.json";

export { W, H };
const B = timing.beats, SLAM = timing.slam, FOLD = timing.fold, LIFTS = timing.lifts, UNFOLD = timing.unfold, FREE = timing.freeLift;
const fbA = makeFB(), fbB = makeFB();
type Txt = [string, string][][];
export const BEATS: Line[][] = (timing.texts as unknown as Txt).map(lines => lines.map(segs => ({ segs: segs.map(([t, c]) => (c ? { t, c } : { t })) })));
const CX = 135, CY = 318, S = 1.55, LOOP_ZOOM = 1.15, AIR = 34, AIR_S = 1.8;
type Out = { ui: number; zoom?: number; zx?: number; zy?: number; shx?: number; shy?: number };
const shake = (f: number, at: number, len = 9, amp = 4) => (f >= at && f < at + len ? Math.sin(f * 2.7) * amp * (1 - (f - at) / len) : 0);
// a finger pops up then settles back: 0 → 1 → 0
const bump = (f: number, at: number, up = 7, hold = 12, down = 8) => (f < at ? 0 : f < at + up ? easeOut((f - at) / up) : f < at + up + hold ? 1 : 1 - easeInOut((f - at - up - hold) / down));
const st = (lift: number[], fold: number, strain: number): HandState => ({ lift, fold, strain });

// 1. hook: the hand slams down, middle folds, the ring finger is locked
const s1 = (f: number, L: Label[]): Out => {
  desk(f);
  const k = easeIn(f / SLAM), y = lerp(AIR, 0, k), s = lerp(AIR_S, S, k);
  const fold = easeInOut((f - FOLD) / 14), strain = f > 52 ? 0.6 + 0.4 * Math.sin(f * 0.5) : 0;
  hand(CX, CY + y, s, { ...st([0, 0, 0, 0, 0], fold, strain), air: 1 - k }, f);
  if (f > 52) { const [tx, ty] = tipOf(CX, CY, S, 2, st([0, 0, 0, 0, 0], fold, 0)); padlock(tx + 22, ty - 4, lerp(0.2, 1.1, backOut((f - 52) / 10)), 0, Math.sin(f * 2.3) * 1.5); }
  return { ui: L.length, zoom: lerp(LOOP_ZOOM, 1, backOut(f / 16)), zx: CX, zy: 300, shx: shake(f, SLAM), shy: shake(f + 2, SLAM) };
};

// 2. the test: thumb, index, pinky lift; the ring finger cannot
const s2 = (f: number, L: Label[]): Out => {
  desk(f);
  const [lt, li, lp, lr] = LIFTS;
  const lift = [bump(f, lt), bump(f, li), 0, f > lr ? 0.06 * Math.abs(Math.sin(f * 0.7)) : 0, bump(f, lp)];
  const strain = f > lr ? 0.7 + 0.3 * Math.sin(f * 0.6) : 0, S2 = st(lift, 1, strain);
  hand(CX, CY, S, S2, f);
  const ok = (i: number, at: number) => { if (f > at + 3 && f < at + 30) { const [x, y] = i === 0 ? [CX - 50 * S, CY - 36 * S] : tipOf(CX, CY, S, i - 1, S2); L.push({ s: "OK", x: Math.round(x - 6), y: Math.round(y - 30), c: "#55efc4", size: 24 }); } };
  ok(0, lt); ok(1, li); ok(4, lp);
  if (f > lr + 4) { const [x, y] = tipOf(CX, CY, S, 2, S2); L.push({ s: "NO!", x: Math.round(x - 12), y: Math.round(y - 32), c: "#ff4a4a", size: 24 }); }
  return { ui: L.length, shx: shake(f, lr + 4, 8, 2) };
};

// 3. x-ray: the tendons and the band that ties middle to ring
const s3 = (f: number, L: Label[]): Out => {
  const l = f - B[2];
  xrayBg(f);
  const pulse = l > 30 ? 0.5 + 0.5 * Math.sin((l - 30) * 0.32) : 0;
  const [bx, by] = xrayHand(CX, CY, S, st([0, 0, 0, 0, 0], 1, pulse), f, pulse);
  if (l > 12) L.push({ s: "TENDONS", x: 20, y: 380, c: "#ffd84e" });
  if (l > 40) L.push({ s: "LINKED!", x: Math.round(bx + 34), y: Math.round(by - 4), c: "#ff5a5a", size: 24 });
  return { ui: L.length };
};

// 4. unfold the middle finger and the ring finger lifts freely
const s4 = (f: number, L: Label[]): Out => {
  desk(f);
  const fold = 1 - easeInOut((f - UNFOLD) / 14), up = f < FREE ? 0 : easeOut((f - FREE) / 8) * (0.62 + 0.38 * Math.cos((f - FREE) * 0.33));
  const S4 = st([0, 0, 0, up, 0], fold, 0);
  hand(CX, CY, S, S4, f);
  if (f > FREE + 4) {
    const [x, y] = tipOf(CX, CY, S, 2, S4);
    L.push({ s: "FREE!", x: Math.round(x - 20), y: Math.round(y - 32), c: "#55efc4", size: 24 });
    for (let i = 0; i < 6; i++) { const a = i / 6 * Math.PI * 2 + f * 0.08, r = 24 + Math.sin(f * 0.2 + i) * 4; sparkle(x + Math.cos(a) * r, y + Math.sin(a) * r, i % 2 ? 1 : 2, hex(i % 2 ? "#ffd84e" : "#55efc4"), 0.9); }
  }
  return { ui: L.length };
};

// 5. the question; then the hand lifts off the desk so the reel loops into frame 1
const s5 = (f: number, L: Label[]): Out => {
  const l = f - B[4], back = easeInOut((f - (B[5] - 26)) / 24);
  desk(f);
  const fold = easeInOut(l / 12) * (1 - back), strain = l > 14 && back === 0 ? 0.5 + 0.5 * Math.sin(l * 0.5) : 0;
  const S5 = st([0, 0, 0, 0, 0], fold, strain);
  hand(CX, CY + lerp(0, AIR, easeIn(back)), lerp(S, AIR_S, easeIn(back)), { ...S5, air: easeIn(back) }, f);
  if (l > 14 && back < 0.2) { const [tx, ty] = tipOf(CX, CY, S, 2, S5); padlock(tx + 22, ty - 4, 1.1, 0, Math.sin(f * 2.3) * 1.5); }
  return { ui: L.length, zoom: lerp(1, LOOP_ZOOM, back), zx: CX, zy: 300 };
};

const SCENES = [s1, s2, s3, s4, s5];
export const beatIndex = (f: number) => { let i = 0; while (i < SCENES.length - 1 && f >= B[i + 1]) i++; return i; };

const draw = (f: number, L: Label[]) => {
  light.dir = [-0.55, -0.6, 0.6]; light.rimDir = [0.8, -0.45]; light.tint = [1, 1, 1]; light.rim = hex("#ffd890"); light.rimAmt = 0.7;
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
  const d = hex("#120604");
  darken(56, 72, d, 0, 0.6); for (let y = 72; y < 134; y++) for (let x = 0; x < W; x++) put(x, y, d, 0.6); darken(134, 150, d, 0.6, 0);
};

// iris transition: the next scene opens as a growing circle with a warm edge
const CUTS = [B[1], B[2], B[3], B[4]];
const HALF = 7, IX = 135, IY = 300, IR = Math.hypot(150, 320);
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
    const p = easeInOut((f - (cut - HALF)) / (HALF * 2)), r = p * IR, mixed = new Float32Array(W * H * 3), edge: RGB = hex("#ffcf7a");
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      const d = Math.hypot(x - IX, y - IY), i = (y * W + x) * 3, src = d < r ? next : prev;
      mixed[i] = src[i]; mixed[i + 1] = src[i + 1]; mixed[i + 2] = src[i + 2];
      if (p > 0 && p < 1 && Math.abs(d - r) < 1.6) { mixed[i] = edge[0]; mixed[i + 1] = edge[1]; mixed[i + 2] = edge[2]; }
    }
    quantize(mixed, out);
    flush(out, p > 0.5 ? (f < cut ? lo : lc) : (f < cut ? lc : lo));
  } else { quantize(fbA, out); flush(out, L); }
  const bi = beatIndex(f), lf = f - B[bi], lines = BEATS[bi].map((l, i) => (bi === 0 && i === 1 ? { ...l, big: true } : l));
  if (bi === 0) textBlock(out, lines, 80, 999);
  else if (lf >= 3 && (bi === BEATS.length - 1 || B[bi + 1] - f > 3)) textBlock(out, lines, 88, (lf - 3) * CHARS_PER_FRAME);
};
