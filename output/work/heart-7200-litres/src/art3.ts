import { W, H, RGB, SDF, Mat, hex, mix, sat, clamp, lerp, sstep, hash, noise, fbm, put, addPx, rect, glow, paint, push, pop,
  circle, ell, rbox, capsule, blend, union, minus, light, easeOut, toWorld } from "./gfx";
import { arc, sparkle, Label } from "./art";
import timing from "./timing.json";

const BP = timing.beatPeriod;
// lub-dub: a strong contraction then a softer one, every beat period
export const beat = (f: number) => {
  const t = ((f % BP) + BP) % BP;
  return Math.exp(-t * 0.45) + 0.55 * (t >= 6 ? Math.exp(-(t - 6) * 0.5) : 0);
};
export const beatIndexAt = (f: number) => Math.floor(f / BP);

// ---------- chest backdrop: warm interior with soft rib bands ----------
export const chestBg = (f: number, cy = 290) => {
  const p = beat(f);
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const r = Math.hypot((x - 135) / 190, (y - cy) / 250);
    let c = mix(mix(hex("#7a1a4a"), hex("#2a0a3a"), sat(r)), hex("#12061e"), sat(r * 1.2 - 0.4));
    // ribs: curved bands
    const ry = (y - cy + 400 + Math.pow(Math.abs(x - 135) / 60, 2) * 12) % 56;
    if (ry < 9 && Math.abs(x - 135) > 34) c = mix(c, hex("#e8b8c8"), 0.16 * (1 - r * 0.6));
    put(x, y, c);
  }
  glow(135, cy, 170, hex("#ff3a6a"), 0.18 + 0.2 * p);
};

// ---------- the heart ----------
export type HeartFace = "happy" | "proud" | "sleep" | "wink" | "strain";
export const heartChar = (cx: number, cy: number, s: number, face: HeartFace, f: number, labels?: Label[]) => {
  const p = beat(f), k = 1 + 0.075 * p, sx = s * k, sy = s * (1 + 0.04 * p);
  push(cx, cy, -0.12, sx, sy);
  // great vessels behind the heart
  const red: Mat = { base: hex("#e8405a"), lite: hex("#ff9aa8"), dark: hex("#7a1040"), puff: 7 };
  const blue: Mat = { base: hex("#4a6ae8"), lite: hex("#9ab0ff"), dark: hex("#1a2a7a"), puff: 7 };
  paint(-48, -88, -10, -20, capsule(-26, -30, -32, -76, 9), blue);
  paint(-6, -100, 60, -20, union(capsule(6, -30, 6, -70, 11), capsule(6, -70, 36, -78, 10), capsule(36, -78, 44, -54, 8)), red);
  // body: two lobes + tapered point
  const body = blend(11, circle(-21, -10, 29), circle(21, -10, 29), capsule(0, -2, 0, 40, 28, 6));
  paint(-56, -46, 56, 52, body, {
    base: hex("#e83a5a"), lite: hex("#ff9aa8"), dark: hex("#6a0a3a"), puff: 30,
    tex: (x, y, d, lam) => {
      // coronary vessels
      const v1 = Math.abs(x + 4 - Math.sin(y * 0.09) * 6 - y * 0.25);
      const v2 = Math.abs(y + 6 - Math.sin(x * 0.12) * 4 + x * 0.2);
      if (d < -4 && ((v1 < 1.1 && y > -20 && y < 30) || (v2 < 1 && x > 4 && x < 34))) return mix(hex("#a8203a"), hex("#ff6a7a"), lam * 0.6);
      return null;
    },
  });
  // face
  const dk = hex("#1a1038"), flat: Mat = { base: dk, flat: true, line: null, rim: 0 };
  for (const sd of [-1, 1]) {
    const ex = sd * 14, ey = -2;
    const shut = face === "sleep" || (face === "wink" && sd > 0) || (face === "happy" && (f + 33) % 97 < 4);
    if (shut) { paint(ex - 8, ey - 6, ex + 8, ey + 6, arc(ex, ey - 3, 5.5, 0.4, 2.75, 1.1), flat); continue; }
    if (face === "strain") { paint(ex - 7, ey - 6, ex + 7, ey + 6, union(capsule(ex - sd * 4, ey - 4, ex + sd * 4, ey, 1.1), capsule(ex - sd * 4, ey + 4, ex + sd * 4, ey, 1.1)), flat); continue; }
    paint(ex - 8, ey - 10, ex + 8, ey + 10, ell(ex, ey, 6.5, 8), { base: hex("#ffffff"), flat: true, rim: 0 });
    paint(ex - 6, ey - 6, ex + 6, ey + 6, circle(ex + 1, ey + 1.5, 4.2), { ...flat, base: hex("#2a1450") });
    paint(ex - 3, ey - 4, ex + 1, ey, circle(ex - 0.5, ey - 1.5, 1.6), { ...flat, base: hex("#ffffff") });
  }
  if (face === "sleep") paint(-5, 8, 5, 18, ell(0, 13, 2.6, 3), { ...flat, base: hex("#7a1a3a") });
  else if (face === "strain") paint(-9, 8, 9, 16, (x, y) => Math.abs(y - 12 - Math.sin(x * 1.1) * 1.3) - 0.9 + Math.max(0, Math.abs(x) - 7) * 9, flat);
  else if (face === "proud") paint(-11, 6, 11, 20, (x, y) => Math.max(circle(0, 8, 9)(x, y), 9 - y), { base: hex("#8a1a3a"), flat: true, rim: 0, tex: (x, y) => (y < 11 ? hex("#ffffff") : null) });
  else paint(-9, 6, 9, 18, arc(0, 8, 6.5, 0.45, 2.7, 1.1), flat);
  for (const sd of [-1, 1]) for (let j = -3; j <= 3; j++) for (let i = -6; i <= 6; i++) {
    if ((i * i) / 36 + (j * j) / 9 > 1) continue;
    const [X, Y] = toWorld(sd * 24 + i, 10 + j); put(Math.floor(X), Math.floor(Y), hex("#ff9ab8"), 0.3);
  }
  pop();
  // pump shockwave rings on each contraction
  const t = ((f % BP) + BP) % BP;
  if (t < 12) {
    const rr = s * (60 + t * 6), a = (1 - t / 12) * 0.5;
    for (let i = 0; i < 90; i++) { const ang = i / 90 * Math.PI * 2; put(cx + Math.cos(ang) * rr, cy + Math.sin(ang) * rr * 0.95, hex("#ffb0c0"), a); }
  }
};

// ---------- props ----------
const GLASS: Mat = { base: hex("#bfe8ff"), lite: hex("#ffffff"), dark: hex("#5a7ab8"), puff: 8, alpha: 0.35, rim: 0 };
export const jug = (cx: number, by: number, level: number, f: number, labels: Label[]) => {
  const hw = 30, hh = 46, cy = by - hh;
  paint(cx + hw - 6, cy - 30, cx + hw + 22, cy + 20, arc(cx + hw, cy - 6, 14, -1.4, 1.4, 4), { ...GLASS, alpha: 0.6 });
  // liquid
  const top = by - 4 - level * (hh * 2 - 14);
  paint(cx - hw, by - hh * 2, cx + hw, by, (x, y) => Math.max(rbox(cx, cy, hw - 3, hh - 3, 8)(x, y), top + Math.sin(x * 0.3 + f * 0.3) * 1.5 - y), {
    base: hex("#e8304a"), lite: hex("#ff7a8a"), dark: hex("#7a0a2a"), puff: 14, line: null, rim: 0,
  });
  paint(cx - hw - 2, by - hh * 2 - 2, cx + hw + 2, by + 2, rbox(cx, cy, hw, hh, 10), GLASS);
  paint(cx - 12, by - hh * 2 - 14, cx + 12, by - hh * 2 + 4, rbox(cx, by - hh * 2 - 5, 10, 8, 3), { base: hex("#5a6ae8"), puff: 4 });
  rect(cx - hw + 5, cy - hh + 14, 3, hh * 1.4, hex("#ffffff"), 0.6);
  labels.push({ s: "5 L", x: cx - 10, y: cy - 8, c: "#ffffff", size: 24 });
};

export const barrel = (cx: number, by: number, s = 1) => {
  const hw = 15 * s, hh = 21 * s;
  paint(cx - hw - 2, by - hh * 2 - 2, cx + hw + 2, by + 2, (x, y) => {
    const dy = (y - (by - hh)) / hh; return rbox(cx, by - hh, hw - 2 + 2 * (1 - dy * dy), hh, 3 * s)(x, y);
  }, {
    base: hex("#2a8ae8"), lite: hex("#8ad0ff"), dark: hex("#0a2a7a"), puff: hw,
    tex: (x, y) => { const r = (y - (by - hh * 2)) / (hh * 2); return Math.abs(r - 0.28) < 0.04 || Math.abs(r - 0.72) < 0.04 ? hex("#1a4ab0") : null; },
  });
  paint(cx - hw, by - hh * 2 - 4 * s, cx + hw, by - hh * 2 + 4 * s, ell(cx, by - hh * 2, hw - 1, 3 * s), { base: hex("#5ab0ff"), lite: hex("#c8ecff"), puff: 3, rim: 0 });
};

export const pool = (x: number, y: number, w: number, h: number, fill: number, f: number, i: number) => {
  rect(x - 1, y - 1, w + 2, h + 2, hex("#e8f0ff"));
  for (let j = 0; j < h; j++) for (let k = 0; k < w; k++) {
    const wet = j / h > 1 - fill;
    let c = wet ? mix(hex("#3ac8ff"), hex("#1a5ad8"), j / h) : hex("#a8c0d8");
    if (wet && Math.sin((k + f * 0.4 + i * 7) * 0.7 + j * 1.3) > 0.85) c = hex("#c8f4ff");
    if (k % Math.max(3, Math.floor(w / 4)) === 0 && j > 0) c = mix(c, hex("#ffffff"), wet ? 0.35 : 0.2); // lane lines
    put(x + k, y + j, c);
  }
};

export const ecg = (x0: number, x1: number, y: number, f: number, col: RGB) => {
  // scrolling trace drawn from the same beat function the heart uses
  const pts: number[] = [];
  for (let x = x0; x < x1; x++) {
    const ff = f - (x1 - x) * 0.6, t = ((ff % BP) + BP) % BP;
    let v = 0;
    if (t < 1.5) v = -14; else if (t < 3) v = 9; else if (t > 8 && t < 12) v = -3 * Math.sin((t - 8) / 4 * Math.PI);
    pts.push(y + v);
  }
  for (let i = 1; i < pts.length; i++) {
    const a = Math.min(pts[i - 1], pts[i]), b = Math.max(pts[i - 1], pts[i]);
    for (let yy = Math.floor(a); yy <= Math.ceil(b); yy++) { put(x0 + i, yy, col); addPx(x0 + i, yy - 1, col, 0.25); addPx(x0 + i, yy + 1, col, 0.25); }
  }
  glow(x1 - 1, pts[pts.length - 1], 8, col, 0.8);
};

export const fist = (cx: number, cy: number, s: number) => {
  push(cx, cy, 0.1, s, s);
  const skin: Mat = { base: hex("#f7c49a"), lite: hex("#ffe6c8"), dark: hex("#c9765e"), puff: 14 };
  paint(-30, 20, 30, 90, rbox(0, 50, 18, 32, 10), { base: hex("#17a58f"), lite: hex("#62e8c0"), dark: hex("#0c4a6e"), puff: 12 });
  paint(-36, -40, 36, 36, rbox(0, -2, 32, 34, 14), skin);
  for (let i = 0; i < 4; i++) paint(-34, -44, 34, 0, circle(-22 + i * 14.5, -26, 8.5), { ...skin, puff: 8 });
  paint(-44, -20, -8, 20, capsule(-28, 10, -12, -10, 9), skin);
  for (let i = 0; i < 3; i++) rect(-15 + i * 14.5, -24, 1, 14, hex("#c9765e"));
  pop();
};
