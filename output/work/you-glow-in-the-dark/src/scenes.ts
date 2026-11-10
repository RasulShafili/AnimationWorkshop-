import { W, H, RGB, hex, mix, sat, lerp, sstep, easeOut, easeInOut, backOut, hash, bayer, makeFB, target, quantize, textBlock, glyphRun, rect, put, glow, darken, light, scaleAll, push, pop, Line } from "./gfx";
import { Label, tod, room, rug, hero, headArt, sparkle, Pose, Face } from "./art";
import { aura, photons, eyeChar, gauge, bodyField, viewfinder, heat, cellBg, cellChar, mitoBig, radical, fatChain, clock, firefly } from "./art2";
import timing from "./timing.json";

const B = timing.beats, HITS = timing.hits;
const fbA = makeFB(), fbB = makeFB();
type Txt = [string, string][][];
export const BEATS: Line[][] = (timing.texts as unknown as Txt).map(lines => lines.map(segs => ({ segs: segs.map(([t, c]) => (c ? { t, c } : { t })) })));

const HERO_X = 128, FEET = 372;
const GLOW = hex("#55efc4");
const DARK: RGB = [0.36, 0.4, 0.62];
const blink = (f: number) => (f + 40) % 97 < 4;

// a bedroom at night with the lamp off; the hero is the light source
const darkRoom = (f: number, labels: Label[], glowAmt: number, face: Face, pose: Pose = { armL: 0.2, armR: 0.2 }, extra?: () => void) => {
  const k = tod(0.76);
  room(k, f, labels);
  rug(HERO_X, 384, k);
  extra?.();
  scaleAll(DARK);
  light.tint = [0.42, 0.5, 0.75]; light.rim = GLOW; light.rimAmt = 0.95; light.rimDir = [0.75, -0.5];
  const pulse = 0.85 + 0.15 * Math.sin(f * 0.09);
  glow(HERO_X, 270, 150, GLOW, 0.22 * glowAmt * pulse);
  hero(HERO_X, FEET, 1, pose, face);
  aura(HERO_X, FEET, 1, pose, GLOW, 0.5 * glowAmt * pulse, 20);
  photons(HERO_X, 330, 110, 220, f, Math.round(16 * glowAmt), GLOW, glowAmt);
};

const s1 = (f: number, labels: Label[]) => {
  const amaze = f > 40;
  const up = easeOut((f - 30) / 20);
  darkRoom(f, labels, 0.9 + 0.1 * Math.sin(f * 0.05), { eye: amaze ? "wide" : "open", mouth: amaze ? "o" : "smile", lookY: 0.9, lookX: 0, blink: !amaze && blink(f) },
    { armL: lerp(0.2, 0.75, up), armR: lerp(0.2, 0.75, up) });
};

const s2 = (f: number, labels: Label[]) => {
  const l = f - B[1];
  // the eye strains: lids squint, pupil opens wide, still sees nothing
  light.tint = [1, 1, 1]; light.rim = GLOW; light.rimAmt = 0.6;
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const r = Math.hypot((x - 170) / 180, (y - 270) / 230);
    put(x, y, mix(hex("#1a1460"), hex("#05041a"), sat(r)));
  }
  const open = lerp(1, 0.42, easeInOut((l - 20) / 40)) + Math.sin(l * 0.5) * 0.02 * sstep(40, 60, l);
  const pupil = lerp(0.7, 1.35, easeInOut((l - 15) / 50));
  eyeChar(176, 262, 58, open, Math.sin(l * 0.07) * 0.5, 0.2, pupil, f);
  if (l > 55) { // sweat drop
    const t = ((l - 55) % 40) / 40;
    glow(222, 210 + t * 30, 6, hex("#8ad8ff"), 0.4);
    rect(220, 206 + t * 30, 3, 5, hex("#8ad8ff")); rect(221, 204 + t * 30, 1, 2, hex("#c8f0ff"));
  }
  gauge(24, 160, 360, f, labels);
  if (l > 30) {
    const a = sstep(30, 40, l);
    for (let y = 262; y < 340; y += 2) put(52, y, hex("#ffe600"), a);
    for (let i = 0; i < 4; i++) { put(50 - i + 2, 338 - i, hex("#ffe600"), a); put(54 + i - 2, 338 - i, hex("#ffe600"), a); }
    if (a > 0.5) labels.push({ s: "1000X", x: 58, y: 296, c: "#ffe600", size: 24 });
  }
};

const s3 = (f: number, labels: Label[]) => {
  const l = f - B[2];
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) put(x, y, hex("#04030c"));
  // single photons pile up until a person appears out of nothing
  const pose = { armL: 0.2, armR: 0.2 }, field = bodyField(HERO_X + 7, FEET + 2, pose);
  const acc = easeInOut((l - 4) / 88) * 1.15;
  let count = 0;
  for (let y = 150; y < 418; y++) for (let x = 22; x < 249; x++) {
    const v = field(x, y), h1 = hash(x * 7 + 1, y * 13 + 5), h2 = hash(x, y + 999);
    if (v > 0 && h1 < acc * (0.25 + v)) { put(x, y, heat(v * (0.75 + 0.35 * h2) * Math.min(1, acc + 0.2))); count++; }
    else if (h1 < 0.004 * acc) put(x, y, heat(0.22));
  }
  viewfinder(f, Math.round(count * 37), labels);
  if (l > 70) labels.push({ s: "JAPAN, 2009", x: 172, y: 400, c: "#a8c8ff", plain: true });
};

const s4 = (f: number, labels: Label[]) => {
  light.tint = [1, 1, 1]; light.rim = hex("#b8fff0"); light.rimAmt = 0.8; light.rimDir = [0.8, -0.45];
  cellBg(f);
  const l = f - B[3], s = backOut(l / 22);
  const cx = 135, cy = 290 + Math.sin(f * 0.05) * 3;
  cellChar(cx, cy, 98 * (0.6 + 0.4 * s), f, labels);
};

const s5 = (f: number, labels: Label[]) => {
  light.tint = [1, 1, 1]; light.rim = hex("#ffe0a0"); light.rimAmt = 0.75;
  cellBg(f, 0.6);
  const cy = 300;
  mitoBig(135, cy, f);
  const spots = [[80, cy + 14], [135, cy - 18], [190, cy + 12]];
  HITS.forEach((h, i) => {
    const [fx, fy] = spots[i], t = f - h;
    fatChain(fx, fy, f, t);
    // a radical charges in from the side, slams the fat, recoils
    const side = i % 2 ? 1 : -1;
    const rx = t < 0 ? fx + side * lerp(46, 14, easeInOut((t + 18) / 18)) : fx + side * (14 + easeOut(t / 14) * 26);
    const ry = fy - 12 + Math.sin(f * 0.2 + i) * 3;
    radical(rx, ry, f, t > -10 && t < 12);
    if (t >= 0 && t < 8) { glow(fx, fy, 40 - t * 3, hex("#ffffff"), 0.9 - t * 0.1); sparkle(fx, fy, 5, hex("#ffffff"), 1); }
    if (t >= 0 && t < 60) { // the photon escapes upward
      const p = easeOut(t / 42), px = fx + Math.sin(t * 0.25) * 6 * (1 - p), py = lerp(fy - 6, 150, p);
      for (let k = 1; k < 6; k++) { const q = Math.max(0, p - k * 0.03); sparkle(fx + Math.sin((t - k) * 0.25) * 6 * (1 - q), lerp(fy - 6, 150, q), 1, hex("#b8fff0"), 0.6 - k * 0.1); }
      glow(px, py, 18, hex("#b8fff0"), 0.8 * (1 - sstep(40, 60, t)));
      sparkle(px, py, 3, hex("#ffffff"), 1 - sstep(40, 60, t));
    }
  });
};

const s6 = (f: number, labels: Label[]) => {
  const l = f - B[5];
  light.tint = [0.55, 0.55, 0.8]; light.rim = GLOW; light.rimAmt = 0.6;
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) put(x, y, mix(hex("#0c0a2a"), hex("#05030f"), y / H));
  const cx = 135, cy = 282, S = 2.5;
  push(cx, cy, 0, S, S);
  headArt(0, 0, { eye: l > 50 && l < 75 ? "wink" : "open", mouth: "smile", lookX: 0, lookY: 0, blink: blink(f) });
  pop();
  // thermal-style photon map sweeps across the face
  const sweep = lerp(cx - 100, cx + 100, easeInOut((l - 8) / 40));
  const pulse = 0.9 + 0.1 * Math.sin(f * 0.15);
  for (let y = cy - 90; y < cy + 90; y++) for (let x = cx - 100; x < cx + 100; x++) {
    if (x > sweep) continue;
    const dx = (x - cx) / S, dy = (y - cy) / S, fd = Math.hypot(dx / 33, dy / 31);
    if (fd > 1 || dy < -15) continue; // skin only: hair does not glow
    let v = 0.3 + 0.25 * (1 - fd);
    for (const s of [-1, 1]) v += 0.55 * Math.exp(-((dx - s * 20) ** 2 + (dy - 10) ** 2) / 60);
    v += 0.4 * Math.exp(-(dx ** 2 + (dy + 10) ** 2) / 110);
    v += 0.25 * Math.exp(-(dx ** 2 + (dy - 4) ** 2) / 20);
    put(x, y, heat(v * pulse * (0.94 + 0.12 * bayer(x, y))), 0.62);
  }
  if (sweep < cx + 100) { rect(sweep, cy - 92, 2, 184, hex("#d8fdff")); glow(sweep, cy, 90, hex("#5ce1e6"), 0.3, 1.2); }
  // colour key
  for (let x = 60; x < 210; x++) for (let y = 416; y < 422; y++) put(x, y, heat((x - 60) / 150));
  labels.push({ s: "DIM", x: 60, y: 426, c: "#a8a0d0", plain: true }, { s: "BRIGHT", x: 174, y: 426, c: "#ffe6a0", plain: true });
  if (l > 46) labels.push({ s: "CHEEKS", x: 200, y: 318, c: "#ffe600" }, { s: "FOREHEAD", x: 20, y: 228, c: "#ffb23a" });
};

const s7 = (f: number, labels: Label[]) => {
  const l = f - B[6], p = easeInOut((l - 6) / 86);
  const k = tod(lerp(0.2, 0.4, p));
  room(k, f, labels);
  rug(135, 400, k);
  clock(152, 212, 46, lerp(10, 16, p));
  // meter: photon output through the day
  const x0 = 40, x1 = 230, y = 376;
  rect(x0 - 2, y - 2, x1 - x0 + 4, 14, hex("#1a1038"));
  const fill = lerp(0.12, 1, p);
  for (let x = x0; x < x1; x++) for (let j = 0; j < 10; j++) {
    const t = (x - x0) / (x1 - x0);
    put(x, y + j, t < fill ? heat(0.25 + t * 0.75) : hex("#2c1f66"));
  }
  glow(x0 + (x1 - x0) * fill, y + 5, 22, hex("#ffd86b"), 0.6);
  labels.push({ s: "10 AM", x: x0, y: y + 16, c: "#a8c8ff" }, { s: "4 PM", x: x1 - 23, y: y + 16, c: "#ffe600" });
  labels.push({ s: "GLOW", x: x0, y: y - 16, c: "#55efc4" });
};

const flies = (f: number, n: number, appear: number) => {
  for (let i = 0; i < n; i++) {
    const t = sat((appear - i * 3) / 30);
    if (t <= 0) continue;
    const a = f * (0.02 + hash(i, 41) * 0.02) + i * 2.4, rr = 50 + hash(i, 42) * 60;
    const ox = HERO_X + Math.cos(a) * rr, oy = 250 + Math.sin(a * 1.3) * rr * 0.7;
    const sx = 60, sy = 190; // they drift in from the window
    firefly(lerp(sx, ox, easeOut(t)), lerp(sy, oy, easeOut(t)), f, i);
  }
};

const s8 = (f: number, labels: Label[]) => {
  const l = f - B[7];
  darkRoom(f, labels, 1, { eye: "open", mouth: "grin", lookX: Math.sin(f * 0.05), lookY: -0.6, blink: blink(f) }, { armL: 0.5, armR: 0.5 }, undefined);
  glow(208, 300, 40, hex("#7aff9a"), 0.3);
  flies(f, 14, l + 10);
};

const s9 = (f: number, labels: Label[]) => {
  const l = f - B[8];
  darkRoom(f, labels, 1.15, { eye: l > 30 && l < 62 ? "wink" : "open", mouth: "grin", lookX: 0.2, lookY: 0.1, blink: blink(f) }, { armL: 0.2, armR: lerp(0.2, 2.55, easeOut((l - 22) / 12)) + Math.sin(l * 0.4) * 0.22 * sstep(30, 40, l) });
  flies(f, 14, 200 - l * 2);
  glow(208, 300, 40, hex("#7aff9a"), 0.25);
};

const SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9];
export const beatIndex = (f: number) => { let i = 0; while (i < 8 && f >= B[i + 1]) i++; return i; };
const draw = (f: number, labels: Label[]) => {
  light.dir = [-0.5, -0.62, 0.6]; light.rimDir = [0.8, -0.45];
  SCENES[beatIndex(f)](f, labels);
};

const CUTS = [B[1], B[2], B[3], B[4], B[5], B[6], B[7]];
const HALF = 7;
export const CHARS_PER_FRAME = 1.6;
const flush = (out: Uint8ClampedArray, labels: Label[]) => {
  for (const l of labels) if (l.s) glyphRun(out, l.s, l.x, l.y, hex(l.c), l.size ?? 16, !l.plain);
};

export const renderFrame = (f: number, out: Uint8ClampedArray) => {
  const labels: Label[] = [];
  const cut = CUTS.find(c => Math.abs(f - c) < HALF);
  target(fbA);
  draw(f, labels);
  if (cut !== undefined) {
    const keep = fbA.slice(), l2: Label[] = [];
    target(fbA); draw(f < cut ? cut : cut - 1, l2);
    const p = (f - (cut - HALF)) / (HALF * 2);
    const from = f < cut ? keep : fbA, to = f < cut ? fbA : keep;
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      const src = bayer(x >> 2, y >> 2) < p ? to : from, i = (y * W + x) * 3;
      fbB[i] = src[i]; fbB[i + 1] = src[i + 1]; fbB[i + 2] = src[i + 2];
    }
    quantize(fbB, out);
    if (p > 0.5 === f >= cut) flush(out, labels);
  } else {
    quantize(fbA, out);
    flush(out, labels);
  }
  const bi = beatIndex(f), lf = f - B[bi], lines = BEATS[bi].map((l, i) => (bi === 0 && i === 1 ? { ...l, big: true } : l));
  if (bi === 0) textBlock(out, lines, 80, 999);
  else if (lf >= 3 && B[bi + 1] - f > 3) textBlock(out, lines, 88, (lf - 3) * CHARS_PER_FRAME);
};
