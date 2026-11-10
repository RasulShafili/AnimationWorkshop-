import { W, H, RGB, hex, mix, sat, lerp, sstep, easeOut, easeIn, easeInOut, backOut, hash, bayer, makeFB, target, quantize, textBlock, glyphRun, rect, put, glow, light, scaleAll, Line } from "./gfx";
import { Label, tod, room, rug, hero, bedScene, sparkle } from "./art";
import { chestBg, heartChar, beat, jug, barrel, pool, ecg, fist } from "./art3";
import timing from "./timing.json";

const B = timing.beats, BP = timing.beatPeriod;
const fbA = makeFB(), fbB = makeFB();
type Txt = [string, string][][];
export const BEATS: Line[][] = (timing.texts as unknown as Txt).map(lines => lines.map(segs => ({ segs: segs.map(([t, c]) => (c ? { t, c } : { t })) })));
const fmt = (n: number) => Math.round(n).toLocaleString("en-US");
const warm = () => { light.tint = [1, 1, 1]; light.rim = hex("#ffb0a0"); light.rimAmt = 0.85; light.rimDir = [0.8, -0.45]; };
const panel = (x: number, y: number, w: number, h: number) => { rect(x, y, w, h, hex("#120a2e")); rect(x + 1, y + 1, w - 2, h - 2, hex("#2a1450")); };

const s1 = (f: number, L: Label[]) => {
  warm(); chestBg(f);
  heartChar(135, 290, 1.5, "happy", f);
  // litres rack up beat by beat
  const v = 7200 * (0.18 + 0.82 * easeInOut(f / 100)); // never 0 on the thumbnail
  panel(52, 396, 166, 30);
  L.push({ s: "LITRES " + fmt(v).padStart(5, " "), x: 64, y: 401, c: "#ff8aa0", size: 24, plain: true });
};

const s2 = (f: number, L: Label[]) => {
  warm(); chestBg(f, 260);
  const l = f - B[1], p = sat(l / 98);
  heartChar(80, 250, 0.85, "happy", f);
  // pipe from heart to the jug with pulses of blood travelling along it
  for (let x = 110; x < 170; x++) { rect(x, 300, 1, 8, hex("#7a1a3a")); rect(x, 301, 1, 6, hex("#e8304a")); }
  for (let i = 0; i < 4; i++) { const ph = ((f + i * 6) % BP) / BP; glow(110 + ph * 60, 304, 6, hex("#ff8a9a"), 0.6); }
  jug(196, 400, p, f, L);
  panel(30, 360, 84, 30);
  const sec = Math.min(60, Math.floor(p * 60));
  L.push({ s: "0:" + String(sec).padStart(2, "0"), x: 44, y: 365, c: sec >= 60 ? "#55efc4" : "#ffe600", size: 24, plain: true });
  L.push({ s: sec >= 60 ? "1:00" : "", x: 0, y: 0, c: "#fff" });
};

const s3 = (f: number, L: Label[]) => {
  warm(); chestBg(f, 250);
  heartChar(135, 255, 1.2, "proud", f);
  panel(20, 344, 230, 40); ecg(24, 246, 364, f, hex("#55efc4"));
  const l = f - B[2], v = 100000 * easeInOut(l / 95);
  panel(46, 396, 178, 30);
  L.push({ s: "BEATS " + fmt(v).padStart(7, " "), x: 56, y: 401, c: "#ffe600", size: 24, plain: true });
};

const s4 = (f: number, L: Label[]) => {
  warm(); chestBg(f, 300);
  const l = f - B[3], n = Math.min(36, Math.floor(easeOut(l / 80) * 36.99));
  for (let i = 0; i < n; i++) {
    const r = Math.floor(i / 6), c = i % 6, age = l - (i / 36) * 80 * 0.6;
    const drop = Math.max(0, 1 - easeOut(sat(age / 6))) * 30;
    barrel(37 + c * 39, 416 - r * 46 - drop + (r === 0 ? 0 : 0), 1);
  }
  panel(176, 428, 64, 28);
  L.push({ s: "X" + String(n).padStart(2, " "), x: 188, y: 432, c: "#5ce1e6", size: 24, plain: true });
  L.push({ s: "200 L EACH", x: 30, y: 436, c: "#a8c8ff" });
};

const s5 = (f: number, L: Label[]) => {
  const l = f - B[4], k = tod(0.76);
  room(k, f, L);
  bedScene(k, f, l, 0, L, false);
  scaleAll([0.62, 0.66, 0.85]);
  const p = beat(f);
  glow(150, 330, 40, hex("#ff3a6a"), 0.25 + 0.45 * p);
  glow(150, 330, 12, hex("#ffb0c0"), 0.3 + 0.5 * p);
  // bedside monitor
  panel(150, 196, 96, 52); ecg(154, 242, 228, f, hex("#55efc4"));
  L.push({ s: "BPM 60", x: 156, y: 200, c: "#55efc4" });
  for (let i = 0; i < 3; i++) {
    const t = ((l + i * 32) % 96) / 96;
    L.push({ s: "Z", x: Math.round(92 + t * 26 + Math.sin(t * 9) * 3), y: Math.round(272 - t * 70), c: "#d8e6ff", size: i === 1 ? 32 : 16 });
  }
};

const s6 = (f: number, L: Label[]) => {
  warm(); chestBg(f, 270);
  const l = f - B[5], p = easeInOut(l / 96);
  heartChar(135, 250, 1.1, "proud", f);
  panel(14, 384, 242, 34);
  L.push({ s: fmt(200e6 * p).padStart(11, " ") + " L", x: 20, y: 388, c: "#ff8aa0", size: 24, plain: true });
  L.push({ s: "AGE " + Math.floor(80 * p), x: 96, y: 346, c: "#ffe600", size: 24 });
  for (let i = 0; i < 8; i++) { // calendar pages flying off
    const t = ((l * 1.6 + i * 13) % 40) / 40, x = 70 + i * 18 + t * 60, y = 210 - t * 50 + t * t * 90;
    rect(x, y, 10, 12, hex("#fff6e0"), 1 - t); rect(x, y, 10, 3, hex("#ff4a6a"), 1 - t);
  }
};

const s7 = (f: number, L: Label[]) => {
  light.tint = [1, 1, 1];
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) put(x, y, mix(hex("#0a3a7a"), hex("#061a3a"), y / H));
  const l = f - B[6], n = Math.min(80, Math.floor(easeInOut(l / 85) * 80.99));
  for (let i = 0; i < n; i++) {
    const r = Math.floor(i / 8), c = i % 8, age = l - (i / 80) * 85;
    pool(22 + c * 29, 150 + r * 25, 24, 18, sat(age / 10 + 0.05), f, i);
  }
  panel(96, 412, 78, 30);
  L.push({ s: "X" + String(n).padStart(2, " "), x: 112, y: 417, c: "#ffe600", size: 24, plain: true });
};

const s8 = (f: number, L: Label[]) => {
  const l = f - B[7], k = tod(0.28);
  room(k, f, L); rug(135, 400, k);
  warm(); light.tint = k.tint;
  const a = backOut(l / 18), b2 = backOut((l - 14) / 18);
  if (a > 0.02) fist(88, 268, 1.25 * a);
  if (b2 > 0.02) heartChar(190, 262, 0.95 * b2, l > 50 ? "wink" : "happy", f);
  if (l > 36) { L.push({ s: "FIST", x: 70, y: 352, c: "#ffe600" }, { s: "HEART", x: 172, y: 352, c: "#ff8aa0" }); L.push({ s: "=", x: 128, y: 252, c: "#ffffff", size: 32 }); }
};

const s9 = (f: number, L: Label[]) => {
  const l = f - B[8], k = tod(0.5);
  room(k, f, L); rug(128, 384, k);
  const hand = easeOut((l - 6) / 14);
  hero(128, 372, 1, { armL: 0.2, armR: lerp(0.2, -0.62, hand) }, { eye: l > 40 ? "closed" : "open", mouth: "smile", lookY: 0.4 });
  const p = beat(f) * sstep(14, 24, l);
  glow(122, 288, 34, hex("#ff3a6a"), 0.55 * p);
  const t = ((f % BP) + BP) % BP;
  if (t < 10 && l > 20) for (let i = 0; i < 40; i++) { const ang = i / 40 * Math.PI * 2, rr = 14 + t * 3; put(122 + Math.cos(ang) * rr, 288 + Math.sin(ang) * rr, hex("#ffb0c0"), (1 - t / 10) * 0.8); }
  panel(176, 170, 64, 22); L.push({ s: "BPM 72", x: 182, y: 174, c: "#ff8aa0" });
};

const SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9];
export const beatIndex = (f: number) => { let i = 0; while (i < 8 && f >= B[i + 1]) i++; return i; };
const draw = (f: number, L: Label[]) => { light.dir = [-0.5, -0.62, 0.6]; light.rimDir = [0.8, -0.45]; SCENES[beatIndex(f)](f, L); };
const CUTS = [B[1], B[2], B[3], B[4], B[5], B[6], B[7], B[8]];
const HALF = 7;
export const CHARS_PER_FRAME = 1.6;
const flush = (out: Uint8ClampedArray, L: Label[]) => { for (const l of L) if (l.s) glyphRun(out, l.s, l.x, l.y, hex(l.c), l.size ?? 16, !l.plain); };

export const renderFrame = (f: number, out: Uint8ClampedArray) => {
  const L: Label[] = [];
  const cut = CUTS.find(c => Math.abs(f - c) < HALF);
  target(fbA); draw(f, L);
  if (cut !== undefined) {
    const keep = fbA.slice(), l2: Label[] = [];
    target(fbA); draw(f < cut ? cut : cut - 1, l2);
    const p = (f - (cut - HALF)) / (HALF * 2), from = f < cut ? keep : fbA, to = f < cut ? fbA : keep;
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      const src = bayer(x >> 2, y >> 2) < p ? to : from, i = (y * W + x) * 3;
      fbB[i] = src[i]; fbB[i + 1] = src[i + 1]; fbB[i + 2] = src[i + 2];
    }
    quantize(fbB, out);
    if (p > 0.5 === f >= cut) flush(out, L);
  } else { quantize(fbA, out); flush(out, L); }
  const bi = beatIndex(f), lf = f - B[bi], lines = BEATS[bi].map((l, i) => (bi === 0 && i === 1 ? { ...l, big: true } : l));
  if (bi === 0) textBlock(out, lines, 74, 999);
  else if (lf >= 3 && B[bi + 1] - f > 3) textBlock(out, lines, 88, (lf - 3) * CHARS_PER_FRAME);
};
