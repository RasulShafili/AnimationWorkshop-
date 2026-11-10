import { W, H, RGB, hex, mix, sat, lerp, sstep, easeOut, easeInOut, backOut, hash, bayer, makeFB, target, quantize, textBlock, glyphRun, rect, put, glow, darken, light, Line } from "./gfx";
import {
  Label, tod, room, rug, hero, xrayHero, ruler, vertebra, disc, droplet, books, backpack, ironBlock, tissue, bedScene, space, astronaut, sparkle, DiscFace,
} from "./art";
import timing from "./timing.json";

const B = timing.beats, HITS = timing.hits;
const fbA = makeFB(), fbB = makeFB();

const G = (t: string): { t: string; c: string } => ({ t, c: "#ffe600" });
const Cy = (t: string): { t: string; c: string } => ({ t, c: "#5ce1e6" });
const Em = (t: string): { t: string; c: string } => ({ t, c: "#55efc4" });
const P = (t: string) => ({ t });

export const BEATS: { lines: Line[]; y?: number }[] = [
  { lines: [{ segs: [P("YOU SHRINK")] }, { segs: [G("ABOUT 1 CM")], big: true }, { segs: [P("EVERY SINGLE DAY")] }], y: 74 },
  { lines: [{ segs: [P("THE CULPRIT IS")] }, { segs: [P("HIDING IN YOUR "), Cy("SPINE")] }] },
  { lines: [{ segs: [G("23"), P(" JELLY CUSHIONS")] }, { segs: [P("FULL OF "), Cy("WATER")] }] },
  { lines: [{ segs: [P("ALL DAY, "), G("GRAVITY")] }, { segs: [P("SQUEEZES IT OUT")] }] },
  { lines: [{ segs: [P("LIE DOWN AT NIGHT")] }, { segs: [P("AND THE "), Em("SQUEEZE STOPS")] }] },
  { lines: [{ segs: [P("YOUR DISCS "), Cy("DRINK")] }, { segs: [P("THE WATER BACK")] }] },
  { lines: [{ segs: [P("YOU ARE "), G("TALLEST")] }, { segs: [P("AT SUNRISE")] }] },
  { lines: [{ segs: [P("NO GRAVITY? IN SPACE")] }, { segs: [P("YOU GROW UP TO "), G("5 CM")] }] },
  { lines: [{ segs: [G("TRY IT:"), P(" MEASURE TONIGHT")] }, { segs: [P("THEN AT "), G("SUNRISE")] }] },
];

const RX = 168, FEET = 372, HERO_X = 110, RTOP = 150;
const heroTop = (sy: number) => FEET - 180 * sy;

// exaggerated on screen: 1 cm reads as 8 art px
const tag = (labels: Label[], sy: number, value: string, col = "#ffe600") => {
  const y = Math.round(heroTop(sy));
  rect(HERO_X + 4, y, RX - HERO_X + 2, 1, hex(col));
  rect(RX + 12, y - 11, 52, 22, hex("#1a1038"));
  rect(RX + 13, y - 10, 50, 20, hex("#2c1f66"));
  for (let i = 0; i < 5; i++) rect(RX + 11 - i, y - i, 1, i * 2 + 1, hex(col));
  labels.push({ s: value, x: RX + 16, y: y - 9, c: col, size: 24, plain: true });
};

const blink = (f: number) => (f + 40) % 97 < 4;

const sceneRoom = (f: number, labels: Label[]) => {
  // beat 1 + 2: the day flies past the window
  const p = easeInOut(f / (B[1] - 6));
  const k = tod(lerp(0.03, 0.54, p));
  room(k, f, labels);
  rug(HERO_X + 20, 382, k);
  ruler(RX, RTOP, FEET - 6, k);
  const sy = lerp(1, 0.955, p);
  const tired = p > 0.55;
  const sway = Math.sin(f * 0.11) * 0.05;
  hero(HERO_X, FEET, sy, { armL: 0.2 + sway, armR: 0.2 - sway }, { eye: tired ? "half" : "open", mouth: tired ? "flat" : "smile", lookX: 0.4, lookY: -0.3, blink: blink(f) }, Math.sin(f * 0.07) * 0.008);
  tag(labels, sy, (175 - p).toFixed(1));
  return { sy, k };
};

const sceneXray = (f: number, labels: Label[]) => {
  const l = f - B[1];
  const scanY = lerp(-4, 420, easeInOut(l / 62));
  // layer A: normal
  target(fbB);
  const k = tod(0.54);
  const la: Label[] = [];
  room(k, f, la); rug(HERO_X + 20, 382, k); ruler(RX, RTOP, FEET - 6, k);
  const sy = 0.955;
  hero(HERO_X, FEET, sy, { armL: 0.2, armR: 0.2 }, { eye: "wide", mouth: "o", lookX: 0.2, lookY: 0.7 });
  tag(la, sy, "174.0");
  // layer B: x-ray world
  target(fbA);
  room(k, f, []); rug(HERO_X + 20, 382, k); ruler(RX, RTOP, FEET - 6, k);
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const i = (y * W + x) * 3, g = fbA[i] * 0.3 + fbA[i + 1] * 0.59 + fbA[i + 2] * 0.11;
    fbA[i] = 0.02 + g * 0.1; fbA[i + 1] = 0.05 + g * 0.3; fbA[i + 2] = 0.2 + g * 0.55;
    if ((x % 15 === 0 || y % 15 === 0)) fbA[i + 1] += 0.05, fbA[i + 2] += 0.08;
  }
  light.rimAmt = 0;
  xrayHero(HERO_X, FEET, sy, { armL: 0.2, armR: 0.2 }, f);
  // composite above the scan line = x-ray
  const sl = Math.round(scanY);
  for (let y = sl; y < H; y++) for (let i = y * W * 3; i < (y + 1) * W * 3; i++) fbA[i] = fbB[i];
  if (l < 62) {
    rect(0, sl - 1, W, 3, hex("#d8fdff"));
    glow(135, sl, 150, hex("#35e4ff"), 0.55, 0.14);
  }
  if (l > 58) { // lock-on brackets around the spine
    const a = sat((l - 58) / 8), bx = HERO_X, by = FEET - 90 * sy, r = lerp(70, 42, easeOut((l - 58) / 12)), c = hex("#ffe600");
    for (const sx of [-1, 1]) for (const s2 of [-1, 1]) {
      const X = bx + sx * r * 0.62, Y = by + s2 * r;
      rect(X - (sx > 0 ? 10 : 0), Y, 10, 2, c, a); rect(sx > 0 ? X - 2 : X, Y - (s2 > 0 ? 10 : 0), 2, 10, c, a);
    }
  }
  labels.push(...la.filter(t => t.y > sl)); // the scan line wipes the labels away too
};

// droplets squeezed out on each impact
const squirts = (f: number) => {
  for (let h = 0; h < HITS.length; h++) for (let i = 0; i < 12; i++) {
    const t = (f - HITS[h]) / 30;
    if (t < 0 || t > 1.2) continue;
    const side = i % 2 ? 1 : -1, vx = side * (70 + hash(i, h) * 110), vy = -70 - hash(i, h + 9) * 90;
    const x = 135 + side * 72 + vx * t, y = 322 + vy * t + 260 * t * t;
    droplet(x, y, vx, vy + 520 * t, 3.4 + hash(i, h + 3) * 2.4);
  }
};

const discHeight = (f: number) => {
  const hs = [56, 46, 36, 28];
  if (f < HITS[0]) return 56;
  if (f < B[5]) {
    let i = 0; while (i < 2 && f >= HITS[i + 1]) i++;
    const t = f - HITS[i], from = hs[i], to = hs[i + 1];
    return to + (from - to) * Math.exp(-t * 0.28) * Math.cos(t * 0.75) * 0.9 - (t < 3 ? 5 : 0);
  }
  return lerp(28, 56, easeInOut((f - (B[5] + 12)) / 82));
};

const CY = 310;
const sceneMacro = (f: number, labels: Label[], night: number) => {
  light.dir = [-0.5, -0.62, 0.6]; light.rimDir = [0.82, -0.4];
  light.rim = night > 0.5 ? hex("#7fb8ff") : hex("#ffb45a"); light.rimAmt = 0.85;
  light.tint = night > 0.5 ? [0.72, 0.78, 1.06] : [1, 1, 1];
  tissue(night, f, CY);
  if (night > 0.5) for (let i = 0; i < 60; i++) put(hash(i, 4) * W, hash(i, 5) * H, hex("#ffffff"), 0.35 + 0.5 * Math.sin(f * 0.16 + i) ** 2);
  const l = f - B[2];
  // the camera climbs all 23 discs, then lands on the top one
  const P_ = 128, climb = night > 0.5 ? 1 : easeInOut(l / 78);
  const scroll = (1 - climb) * 22 * P_;
  const h = discHeight(f);
  const dy = (56 - h) / 2;
  const glowA = night > 0.5 ? 0.3 : 0.5;
  glow(135, CY, 150, night > 0.5 ? hex("#4a7cff") : hex("#ff5f9e"), glowA);

  const facePick = (): DiscFace => {
    if (night > 0.5) return "sleep";
    if (f < HITS[0]) return (l < 84 || blink(f)) ? "blink" : "happy";
    return f - HITS[Math.min(2, HITS.filter(t => t <= f).length - 1)] < 16 ? "pain" : "tired";
  };
  const water = lerp(0.2, 0.86, (h - 28) / 28);
  // disc i=0 is the top of the spine; everything below it stays put while it flattens
  for (let i = 22; i >= 0; i--) {
    const yy = CY + i * P_ - scroll;
    if (yy < -90 || yy > H + 90) continue;
    vertebra(135, yy + 64);
    disc(135, yy + (i === 0 ? dy : 0), i === 0 ? h : 56, i === 0 ? water : 0.86, i === 0 ? facePick() : "blink", f + i * 11);
  }
  const topY = CY - 64 + dy * 2 - scroll;
  vertebra(135, topY);
  if (climb >= 0.999) labels.push({ s: "LEARN WITH 8-BIT", x: 87, y: CY + 58, c: "#c49a6c", plain: true });
  // keep the caption readable while the spine rushes past behind it
  const veil = 1 - sstep(0.8, 1, climb);
  if (veil > 0 && night < 0.5) {
    darken(62, 84, hex("#120a3a"), 0, 0.82 * veil); rect(0, 84, W, 44, hex("#120a3a"), 0.82 * veil); darken(128, 150, hex("#120a3a"), 0.82 * veil, 0);
  }
  return topY - 36;
};

const fallY = (f: number, hit: number, land: number) => {
  const t = (f - hit) / 16; // 16 frames before impact
  if (t >= 0) { const b = Math.exp(-(f - hit) * 0.4) * Math.sin((f - hit) * 0.9) * 4; return land - Math.abs(b); }
  return land - 240 * t * t;
};

const sceneSqueeze = (f: number, labels: Label[]) => {
  const top = sceneMacro(f, labels, 0);
  const shake = HITS.some(h => f >= h && f < h + 7) ? ((f % 2) * 2 - 1) * 3 : 0;
  if (f >= HITS[2] - 16) ironBlock(135, fallY(f, HITS[2], top - 28 - 33), labels);
  if (f >= HITS[1] - 16) backpack(135, fallY(f, HITS[1], top - 28));
  if (f >= HITS[0] - 16) books(135, fallY(f, HITS[0], top));
  squirts(f);
  return shake;
};

const sceneBed = (f: number, labels: Label[]) => {
  const l = f - B[4];
  const k = tod(0.75);
  room(k, f, labels);
  const grow = 9 * easeInOut(l / 95);
  bedScene(k, f, l, grow, labels);
  for (let i = 0; i < 3; i++) {
    const t = ((l + i * 32) % 96) / 96;
    labels.push({ s: "Z", x: Math.round(92 + t * 26 + Math.sin(t * 9) * 3), y: Math.round(272 - t * 70), c: t > 0.8 ? "#6a7ae0" : "#d8e6ff", size: i === 1 ? 32 : 16 });
  }
};

const sceneDrink = (f: number, labels: Label[]) => {
  sceneMacro(f, labels, 1);
  const l = f - B[5];
  for (let i = 0; i < 26; i++) { // water returns
    const t = (l - 6 - i * 3) / 26;
    if (t < 0 || t > 1) continue;
    const side = i % 2 ? 1 : -1, sx = 135 + side * (150 + hash(i, 1) * 30), sy = 200 + hash(i, 2) * 190;
    const e = t * t, x = lerp(sx, 135 + side * 44, e), y = lerp(sy, CY, e) + Math.sin(t * 6 + i) * 8 * (1 - e);
    droplet(x, y, (135 - sx), (CY - sy), 3 + hash(i, 3) * 1.8);
  }
  for (let i = 0; i < 3; i++) {
    const t = ((l + i * 30) % 90) / 90;
    labels.push({ s: "Z", x: Math.round(198 + Math.sin(t * 8) * 4 + t * 12), y: Math.round(240 - t * 56), c: "#d8e6ff", size: i === 1 ? 32 : 16 });
  }
};

const sceneSunrise = (f: number, labels: Label[]) => {
  const l = f - B[6];
  const k = tod(lerp(0.97, 1.09, l / 107));
  room(k, f, labels);
  rug(HERO_X + 20, 382, k);
  ruler(RX, RTOP, FEET - 6, k);
  const pop_ = backOut((l - 16) / 20);
  const sy = lerp(0.955, 1, pop_);
  const up = easeOut((l - 16) / 12);
  hero(HERO_X, FEET - Math.max(0, Math.sin(sat((l - 16) / 22) * Math.PI)) * 14, sy, { armL: lerp(0.2, 2.65, up), armR: lerp(0.2, 2.65, up) },
    l < 16 ? { eye: "closed", mouth: "sleep" } : { eye: "open", mouth: "grin", lookY: -0.5 });
  tag(labels, sy, lerp(174, 175, sat(pop_)).toFixed(1), l > 34 ? "#55efc4" : "#ffe600");
  if (l > 30) {
    for (let i = 0; i < 16; i++) {
      const t = (l - 30 - (i % 4) * 3) / 34;
      if (t < 0 || t > 1) continue;
      const a = hash(i, 11) * 6.28, r = 26 + easeOut(t) * (52 + hash(i, 12) * 54);
      sparkle(HERO_X + Math.cos(a) * r, 240 + Math.sin(a) * r * 0.9, t < 0.6 ? 3 : 2, hex(i % 2 ? "#ffe600" : "#ffffff"), 1 - t * t);
    }
    if (l < 96) labels.push({ s: "+1 CM", x: RX + 16, y: Math.round(heroTop(sy)) - 34, c: "#55efc4", size: 24 });
  }
};

const sceneSpace = (f: number, labels: Label[]) => {
  const l = f - B[7];
  space(f, l);
  const sy = 1 + 0.08 * easeInOut((l - 10) / 70);
  astronaut(120 + Math.sin(l * 0.03) * 7, 262 + Math.sin(l * 0.05) * 5, -0.13 + Math.sin(l * 0.024) * 0.09, sy, f);
  if (l > 58) labels.push({ s: "+5 CM", x: 182, y: 205, c: "#ffe600", size: 24 });
};

const sceneTest = (f: number, labels: Label[]) => {
  const l = f - B[8];
  const k = tod(lerp(0.5, 0.56, l / 107));
  room(k, f, labels);
  rug(HERO_X + 20, 382, k);
  ruler(RX, RTOP, FEET - 6, k);
  const pointUp = easeOut(l / 14);
  hero(HERO_X, FEET, 1, { armL: 0.2, armR: lerp(0.2, 1.62, pointUp) }, { eye: l > 22 && l < 60 ? "wink" : "open", mouth: "grin", lookX: 0.8 });
  const m1 = heroTop(0.955), m2 = heroTop(1), a = sstep(24, 32, l), b = sstep(50, 58, l);
  rect(RX - 11, m1, 22, 2, hex("#ff5a7a"), a);
  rect(RX - 11, m2, 22, 2, hex("#55efc4"), b);
  if (a > 0.5) labels.push({ s: "NIGHT", x: RX + 13, y: Math.round(m1) - 3, c: "#ff8fa8" });
  if (b > 0.5) labels.push({ s: "DAWN", x: RX + 13, y: Math.round(m2) - 14, c: "#55efc4" });
};

// which scene owns a frame
const draw = (f: number, labels: Label[]) => {
  light.dir = [-0.5, -0.62, 0.6]; light.rimDir = [0.8, -0.45];
  if (f < B[1]) return void sceneRoom(f, labels);
  if (f < B[2]) return void sceneXray(f, labels);
  if (f < B[3]) return void sceneMacro(f, labels, 0);
  if (f < B[4]) return void sceneSqueeze(f, labels);
  if (f < B[5]) return void sceneBed(f, labels);
  if (f < B[6]) return void sceneDrink(f, labels);
  if (f < B[7]) return void sceneSunrise(f, labels);
  if (f < B[8]) return void sceneSpace(f, labels);
  sceneTest(f, labels);
};

const CUTS = [B[2], B[4], B[5], B[6], B[7], B[8]];
const HALF = 7;

const flush = (out: Uint8ClampedArray, labels: Label[]) => {
  for (const l of labels) if (l.s) glyphRun(out, l.s, l.x, l.y, hex(l.c), l.size ?? 16, !l.plain);
};

export const beatIndex = (f: number) => { let i = 0; while (i < 8 && f >= B[i + 1]) i++; return i; };
export const CHARS_PER_FRAME = 1.6;

export const renderFrame = (f: number, out: Uint8ClampedArray) => {
  const labels: Label[] = [];
  const cut = CUTS.find(c => Math.abs(f - c) < HALF);
  target(fbA);
  draw(f, labels);
  const shake = f >= HITS[0] && f < B[4] && HITS.some(h => f >= h && f < h + 7) ? ((f % 2) * 2 - 1) * 2 : 0;
  if (cut !== undefined) {
    // chunky ordered dissolve between the two scenes
    const other = f < cut ? cut : cut - 1, keep = fbA.slice();
    const l2: Label[] = [];
    target(fbA); draw(other, l2);
    const p = (f - (cut - HALF)) / (HALF * 2);
    const from = f < cut ? keep : fbA, to = f < cut ? fbA : keep;
    const res = fbB;
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      const th = bayer(x >> 2, y >> 2), src = th < p ? to : from, i = (y * W + x) * 3;
      res[i] = src[i]; res[i + 1] = src[i + 1]; res[i + 2] = src[i + 2];
    }
    quantize(res, out);
    if (p > 0.5 === f >= cut) flush(out, labels);
  } else {
      quantize(fbA, out);
    flush(out, labels);
  }
  if (shake) { // impact shake: shift the whole frame
    const copy = out.slice();
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      const sy = Math.min(H - 1, Math.max(0, y - shake)), si = (sy * W + x) * 4, di = (y * W + x) * 4;
      out[di] = copy[si]; out[di + 1] = copy[si + 1]; out[di + 2] = copy[si + 2];
    }
  }
  const bi = beatIndex(f), lf = f - B[bi];
  let b = BEATS[bi];
  if (bi === 2) {
    const n = String(Math.min(23, 1 + Math.floor(easeInOut(lf / 78) * 22.99))).padStart(2, " ");
    b = { lines: [{ segs: [G(n), P(" JELLY CUSHIONS")] }, b.lines[1]] };
  }
  const tail = B[bi + 1] - f;
  // frame 0 doubles as the thumbnail, so the hook is on screen immediately
  if (bi === 0) textBlock(out, b.lines, b.y ?? 88, 999);
  else if (lf >= 3 && tail > 3) textBlock(out, b.lines, b.y ?? 88, (lf - 3) * CHARS_PER_FRAME);
};
