import { RGB, SDF, Mat, hex, mix, sat, lerp, hash, put, glow, paint, push, pop, circle, ell, rbox, capsule, blend, union, toWorld } from "./gfx";
import { arc, body, headArt, Face, Label, Suit } from "./art";
import { W, H, vgrad, rect, addPx, noise } from "./gfx";

const SKIN: Mat = { base: hex("#f7c49a"), lite: hex("#ffe6c8"), dark: hex("#c9765e"), puff: 12 };
// stage outfit for this video: red hoodie, purple sneakers (not the green striped PJ)
export const HOODIE: Suit = { pj: hex("#e8384f"), pjLite: hex("#ff8a8a"), pjDark: hex("#6a1040"), stripe: null, shoe: hex("#9a6aff") };
const PJ: Mat = { base: HOODIE.pj, lite: HOODIE.pjLite, dark: HOODIE.pjDark, puff: 8 };
const flat = (c: string, a = 1): Mat => ({ base: hex(c), flat: true, line: null, rim: 0, alpha: a });

// arm angle for a hand resting on the nose (see armEnd in art.ts: shoulder at (27,-102), arm length 46)
export const PINCH_ANGLE = -2.52;

/** The hero, optionally pinching the nose with the right hand and puffing the cheeks. */
export const pinchHero = (cx: number, feet: number, armR: number, puff: number, face: Face, armL = 0.2) => {
  for (let j = -7; j <= 7; j++) for (let i = -56; i <= 56; i++) if ((i * i) / 3136 + (j * j) / 49 <= 1) put(cx + i, feet + j, hex("#1a0418"), 0.55);
  push(cx, feet, 0, 1, 1);
  const b = body({ armL, armR }, HOODIE);
  headArt(0, -146, face, "#3a2a6a");
  if (b.raisedL) b.backArm(b.lx, b.ly, -1);
  if (b.raisedR && armR >= -0.3) b.backArm(b.rx, b.ry, 1);
  if (puff > 0.02) for (const s of [-1, 1]) {
    const r = 2 + 6 * puff;
    paint(s * 23 - 10, -146 + 12 - 10, s * 23 + 10, -146 + 12 + 10, circle(s * (22 + puff * 3), -146 + 12, r), { ...SKIN, puff: 6, tex: () => mix(hex("#ffb0a0"), hex("#f7c49a"), 0.4) });
  }
  if (armR < -0.3) { // bent arm: elbow on the chest, forearm up to a pinching hand, drawn over the cheeks
    const k = sat((-armR - 0.3) / (-PINCH_ANGLE - 0.3));
    const ex = lerp(36, 16, k), ey = lerp(-60, -96, k), hx = lerp(40, 3, k), hy = lerp(-20, -133, k);
    paint(Math.min(27, ex) - 11, Math.min(-102, ey) - 11, Math.max(27, ex) + 11, Math.max(-102, ey) + 11, capsule(27, -102, ex, ey, 8, 7), PJ);
    paint(Math.min(ex, hx) - 10, Math.min(ey, hy) - 10, Math.max(ex, hx) + 10, Math.max(ey, hy) + 10, capsule(ex, ey, hx, hy + 6, 7, 6), PJ);
    paint(hx - 10, hy - 14, hx + 10, hy + 10, union(circle(hx, hy + 2, 6.5), capsule(hx - 4, hy, hx - 2, hy - 9, 2.4), capsule(hx + 4, hy, hx + 2, hy - 9, 2.4)), { ...SKIN, puff: 6 });
  }
  pop();
};

/** Sound-wave arcs coming off a point, both sides; amp 0..1 fades and shrinks them. */
export const waves = (x: number, y: number, amp: number, f: number, c = "#ffe600", sides: number[] = [-1, 1], r0 = 34) => {
  if (amp <= 0.01) return;
  for (let i = 0; i < 3; i++) {
    const r = r0 + ((f * 0.9 + i * 10) % 30), a = amp * (1 - ((f * 0.9 + i * 10) % 30) / 30);
    for (const s of sides) {
      const a0 = s > 0 ? -0.55 : Math.PI - 0.55, a1 = s > 0 ? 0.55 : Math.PI + 0.55;
      paint(x - r - 4, y - r - 4, x + r + 4, y + r + 4, arc(x, y, r, a0, a1, 1.3), flat(c, a));
    }
  }
};

// ---------- side cross-section of the head (facing right) ----------
// local frame: (0,0) is mid-head; nostril at (74,12); lips at x≈62, y 36; windpipe runs down x≈-15
const HEAD: SDF = blend(10, ell(-10, -40, 72, 66), ell(22, 10, 56, 52), capsule(10, 40, 46, 54, 18), capsule(58, -16, 76, 10, 9, 6), rbox(-14, 104, 26, 56, 12));
const NASAL = capsule(-8, -8, 64, 4, 7, 5), NOSTRIL = capsule(64, 4, 78, 13, 4.2), THROAT = capsule(-15, -6, -16, 160, 8, 7), MOUTH = ell(26, 34, 30, 8);
const AIRWAY = union(NASAL, NOSTRIL, THROAT, MOUTH);
const PATH: [number, number][] = [[-16, 150], [-15, 0], [10, -6], [64, 4], [76, 12], [120, 26]];
const SEG = PATH.slice(1).map((p, i) => Math.hypot(p[0] - PATH[i][0], p[1] - PATH[i][1]));
const TOTAL = SEG.reduce((a, b) => a + b, 0);
export const S_NOSTRIL = (SEG[0] + SEG[1] + SEG[2] + SEG[3] * 0.9) / TOTAL;
const along = (s: number): [number, number] => {
  let d = s * TOTAL;
  for (let i = 0; i < SEG.length; i++) {
    if (d <= SEG[i] || i === SEG.length - 1) { const t = d / SEG[i]; return [lerp(PATH[i][0], PATH[i + 1][0], t), lerp(PATH[i][1], PATH[i + 1][1], t)]; }
    d -= SEG[i];
  }
  return PATH[PATH.length - 1];
};

/**
 * pressure 0..1 (air piling up), flow 0..1 (air streaming out of the nose), buzz 0..1 (vocal folds vibrating),
 * finger 0..1 (1 = fingertip sealing the nostril).
 */
export const section = (cx: number, cy: number, s: number, pressure: number, flow: number, buzz: number, finger: number, f: number, L: Label[]) => {
  push(cx, cy, 0, s, s);
  paint(-90, -112, 90, 160, HEAD, {
    ...SKIN, puff: 40,
    tex: (x, y, d) => {
      const a = AIRWAY(x, y);
      if (a < -1.5) return mix(hex("#7a1a44"), hex("#ff6a8a"), sat(pressure * 0.6 + 0.1 * Math.sin(f * 0.3 + x * 0.2)) * (pressure > 0 ? 1 : 0.3));
      if (a < 0) return hex("#c0406a");
      if (ell(-14, -50, 48, 36)(x, y) < 0) return mix(hex("#ffb8c8"), hex("#f7c49a"), 0.45); // brain silhouette, faint
      if (y > 40 && y < 46 && x > 4 && x < 60) return hex("#e05a7a"); // tongue line
      return null;
    },
  });
  // closed lips
  paint(56, 28, 76, 44, union(ell(68, 33, 7, 3.4), ell(68, 39, 7, 3.4)), { base: hex("#e0607a"), lite: hex("#ff9ab0"), dark: hex("#8a2a4a"), puff: 3 });
  // vocal folds: two flaps across the windpipe, buzzing when sound is made
  const vy = 88, j = buzz * Math.sin(f * 2.1) * 2.2;
  for (const sd of [-1, 1]) paint(-30, vy - 6, 0, vy + 6, capsule(-15 + sd * 10, vy, -15 + sd * (2 + Math.abs(j)), vy, 2.2), { base: hex("#ffe0e8"), lite: hex("#ffffff"), dark: hex("#c06080"), puff: 2 });
  pop();

  const W_ = (x: number, y: number) => toWorldAt(cx, cy, s, x, y);
  // vocal-fold buzz rings
  if (buzz > 0.02) { const [vx, vy2] = W_(-15, 88); for (let i = 0; i < 2; i++) { const r = 6 + ((f * 1.2 + i * 8) % 16); paint(vx - r - 3, vy2 - r - 3, vx + r + 3, vy2 + r + 3, arc(vx, vy2, r, -2.6, -0.5, 0.8), flat("#ffe600", buzz * (1 - ((f * 1.2 + i * 8) % 16) / 16))); } }

  // air particles
  const N = 46;
  for (let i = 0; i < N; i++) {
    let u: number, a = 1;
    if (flow > 0.01) {
      u = ((i / N) + f * 0.011 * (0.8 + 0.4 * hash(i, 3))) % 1;
      a = flow * (u > S_NOSTRIL ? sat(1 - (u - S_NOSTRIL) / (1 - S_NOSTRIL)) : 1);
    } else {
      // trapped air: the more pressure, the more particles crowd the upper airway and the slower they move
      const crowd = 0.25 + 0.75 * pressure;
      if (i > N * crowd) continue;
      const base = (i / N + f * 0.011 * (1 - pressure)) % 1;
      u = Math.min(base, 0.3 + 0.7 * hash(i, 7)) * S_NOSTRIL;
    }
    const [px, py] = along(u), jx = (hash(i, 1) - 0.5) * 9 + Math.sin(f * 0.4 + i) * pressure * 1.6, jy = (hash(i, 2) - 0.5) * 9 + Math.cos(f * 0.37 + i) * pressure * 1.6;
    const [X, Y] = W_(px + jx, py + jy);
    const c: RGB = flow > 0.01 ? hex("#bff6ff") : mix(hex("#bff6ff"), hex("#ff8aa0"), pressure);
    put(X, Y, c, a); put(X + 1, Y, c, a * 0.8); put(X, Y + 1, c, a * 0.8); put(X + 1, Y + 1, c, a * 0.6);
  }

  // fingertip sealing the nostril
  if (finger > 0.01) {
    const off = (1 - finger) * 40;
    push(cx, cy, 0, s, s);
    paint(60, -4, 130, 60, union(capsule(80 + off, 14 + off * 0.5, 104 + off, 34 + off * 0.5, 7, 9), circle(112 + off, 44 + off * 0.5, 13)), { ...SKIN, alpha: sat(finger * 1.4) });
    pop();
  }
  const [nx, ny] = W_(78, 12);
  if (flow > 0.05) waves(nx + 4, ny + 4, flow, f, "#ffe600", [1], 10);
  return { nx, ny, vocal: W_(-15, 88), lips: W_(68, 36) };
};
const toWorldAt = (cx: number, cy: number, s: number, x: number, y: number): [number, number] => [cx + x * s, cy + y * s];

/** Half-dial gauge: v 0..1 swings the needle from green to red. */
export const gauge = (x: number, y: number, v: number, L: Label[]) => {
  paint(x - 30, y - 30, x + 30, y + 6, (px, py) => Math.max(circle(x, y, 26)(px, py), py - y - 3), {
    base: hex("#20264a"), lite: hex("#3a4478"), dark: hex("#0a0c24"), puff: 8,
    tex: (px, py, d) => {
      if (d > -6 && d < -2 && py < y) { const t = sat((Math.atan2(py - y, px - x) + Math.PI) / Math.PI); return mix(hex("#55efc4"), hex("#ff4a6a"), t); }
      return null;
    },
  });
  const ang = Math.PI + v * Math.PI, ex = x + Math.cos(ang) * 20, ey = y + Math.sin(ang) * 20;
  paint(x - 24, y - 24, x + 24, y + 4, capsule(x, y, ex, ey, 1.4), flat("#ffffff"));
  paint(x - 4, y - 4, x + 4, y + 4, circle(x, y, 3), flat("#ffe600"));
  L.push({ s: "PRESSURE", x: x - 23, y: y + 7, c: v > 0.6 ? "#ff5a7a" : "#a9bce6" });
};

/** Stopwatch face drawn behind a time label (the label goes in L). */
export const stopwatch = (x: number, y: number, txt: string, red: boolean, L: Label[], size = 24) => {
  paint(x - 6, y - 12, x + 6, y - 2, rbox(x, y - 8, 4, 4, 1), { base: hex("#c8cce8"), puff: 2 });
  paint(x - 34, y - 34, x + 34, y + 34, circle(x, y + 16, 30), { base: hex("#fff6e0"), lite: hex("#ffffff"), dark: hex("#b8a8c8"), puff: 10 });
  L.push({ s: txt, x: Math.round(x - txt.length * (size === 32 ? 13 : 9) / 2) + 1, y: y + 16 - (size === 32 ? 11 : 8), c: red ? "#ff3a5a" : "#2a1450", size, plain: true });
};

export const sparkBurst = (x: number, y: number, t: number, c: RGB) => {
  if (t <= 0 || t >= 1) return;
  for (let i = 0; i < 8; i++) { const a = i / 8 * Math.PI * 2, r = 6 + t * 26; put(x + Math.cos(a) * r, y + Math.sin(a) * r, c, 1 - t); put(x + Math.cos(a) * (r - 2), y + Math.sin(a) * (r - 2), c, (1 - t) * 0.6); }
};
export { glow };

// ---------- the stage: velvet curtain, spotlight, wooden floor, mic stand ----------
export const stage = (f: number, spot: number, L: Label[], micX = 206) => {
  // curtain folds
  for (let y = 0; y < 330; y++) for (let x = 0; x < W; x++) {
    const fold = 0.5 + 0.5 * Math.sin(x * 0.19 + Math.sin(y * 0.01 + f * 0.01) * 0.6);
    const sh = 0.45 + 0.55 * Math.pow(fold, 1.6);
    put(x, y, mix(hex("#2a0418"), hex("#a0183c"), sh * (0.55 + 0.45 * (y / 330))));
  }
  // valance with gold fringe
  for (let y = 0; y < 34; y++) for (let x = 0; x < W; x++) put(x, y, mix(hex("#5a0a2a"), hex("#c0284c"), 0.5 + 0.5 * Math.sin(x * 0.42)) );
  for (let x = 0; x < W; x++) { const h = 3 + ((x >> 1) % 2) * 2; for (let y = 34; y < 34 + h; y++) put(x, y, hex(y - 34 < 2 ? "#ffd84e" : "#c08a2a")); }
  // floor boards with perspective
  for (let y = 330; y < H; y++) {
    const z = (y - 330) / (H - 330);
    for (let x = 0; x < W; x++) {
      const u = (x - 135) / (0.5 + z * 1.6), board = Math.abs(((u / 22) % 1 + 1) % 1 - 0.5) < 0.04;
      put(x, y, board ? hex("#3a1a10") : mix(hex("#5a2a14"), hex("#a8642a"), 0.3 + 0.5 * z + 0.08 * noise(u * 0.2, y * 0.6)));
    }
  }
  for (let x = 0; x < W; x++) { put(x, 330, hex("#ffd84e"), 0.7); put(x, 331, hex("#2a0a08")); }
  // spotlight cone + pool on the floor
  if (spot > 0) {
    for (let y = 0; y < H; y++) { const hw = 18 + y * 0.2; for (let x = Math.max(0, Math.floor(128 - hw)); x < Math.min(W, 128 + hw); x++) { const e = Math.max(0, 1 - Math.abs(x - 128) / hw); addPx(x, y, hex("#fff0c0"), 0.16 * spot * Math.pow(e, 0.7)); } }
    glow(128, 376, 90, hex("#fff0c0"), 0.45 * spot, 0.28);
    for (let i = 0; i < 14; i++) { const px = 128 + (hash(i, 4) - 0.5) * 80, py = (hash(i, 5) * 480 + f * (0.3 + hash(i, 6) * 0.4)) % 470; put(px, py, hex("#fff6d8"), 0.5 * spot); }
  }
  // footlights
  for (let i = 0; i < 6; i++) { const x = 22 + i * 45; glow(x, 470, 16, hex("#ffd84e"), 0.5, 0.6); rect(x - 6, 470, 12, 6, hex("#2a1a1a")); rect(x - 4, 469, 8, 2, hex("#fff2b0")); }
  // mic stand
  rect(micX - 1, 242, 2, 130, hex("#2a2a3a")); rect(micX, 242, 1, 130, hex("#8a8aa8"));
  paint(micX - 16, 366, micX + 16, 378, ell(micX, 372, 14, 4), { base: hex("#2a2a3a"), lite: hex("#7a7a9a"), puff: 3 });
  paint(micX - 8, 222, micX + 8, 250, capsule(micX, 230, micX, 244, 6, 4), { base: hex("#4a4a6a"), lite: hex("#c8c8e8"), dark: hex("#1a1a2a"), puff: 5, tex: (x, y) => (y < 236 && (Math.floor(x) + Math.floor(y)) % 2 === 0 ? hex("#2a2a3a") : null) });
};

// x-ray light-table background for the cross-section scenes (teal grid, not navy)
export const lightTable = (f: number) => {
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const g = (x % 18 === 0 || (y + Math.floor(f * 0.3)) % 18 === 0) ? 0.06 : 0;
    put(x, y, mix(hex("#063a3e"), hex("#021418"), sat(Math.hypot((x - 135) / 220, (y - 290) / 280))).map(v => v + g) as RGB);
  }
};
