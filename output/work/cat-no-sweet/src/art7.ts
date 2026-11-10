import { W, H, RGB, SDF, Mat, hex, mix, sat, lerp, hash, noise, put, addPx, rect, glow, paint, push, pop, circle, ell, rbox, capsule, blend, union, minus, toWorld } from "./gfx";
import { arc, Label } from "./art";

const flat = (c: string, a = 1): Mat => ({ base: hex(c), flat: true, line: null, rim: 0, alpha: a });
export const tri = (ax: number, ay: number, bx: number, by: number, cx: number, cy: number): SDF => (x, y) => {
  const e0x = bx - ax, e0y = by - ay, e1x = cx - bx, e1y = cy - by, e2x = ax - cx, e2y = ay - cy;
  const v0x = x - ax, v0y = y - ay, v1x = x - bx, v1y = y - by, v2x = x - cx, v2y = y - cy;
  const c = (v: number) => Math.max(0, Math.min(1, v));
  const k0 = c((v0x * e0x + v0y * e0y) / (e0x * e0x + e0y * e0y)), k1 = c((v1x * e1x + v1y * e1y) / (e1x * e1x + e1y * e1y)), k2 = c((v2x * e2x + v2y * e2y) / (e2x * e2x + e2y * e2y));
  const p0x = v0x - e0x * k0, p0y = v0y - e0y * k0, p1x = v1x - e1x * k1, p1y = v1y - e1y * k1, p2x = v2x - e2x * k2, p2y = v2y - e2y * k2;
  const s = Math.sign(e0x * e2y - e0y * e2x);
  const d0 = [p0x * p0x + p0y * p0y, s * (v0x * e0y - v0y * e0x)], d1 = [p1x * p1x + p1y * p1y, s * (v1x * e1y - v1y * e1x)], d2 = [p2x * p2x + p2y * p2y, s * (v2x * e2y - v2y * e2x)];
  const dd = Math.min(d0[0], d1[0], d2[0]), sg = Math.min(d0[1], d1[1], d2[1]);
  return -Math.sqrt(dd) * Math.sign(sg);
};
const line = (x0: number, y0: number, x1: number, y1: number, c: RGB, a = 1) => {
  const n = Math.ceil(Math.hypot(x1 - x0, y1 - y0));
  for (let i = 0; i <= n; i++) put(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n, c, a);
};

// ---------------- the kitchen at night ----------------
export const COUNTER = 384;
export const kitchen = (f: number, L: Label[], lamp = 1) => {
  // upper wall: warm plaster with a soft lamp pool
  for (let y = 0; y < 250; y++) for (let x = 0; x < W; x++) {
    const n = noise(x * 0.08, y * 0.08) * 0.05;
    put(x, y, mix(hex("#5a3a4a"), hex("#f2c9a0"), sat(1 - Math.hypot((x - 80) / 260, (y - 160) / 220)) * lamp + n));
  }
  // window: night sky, moon, stars, a rooftop
  const wx0 = 158, wx1 = 252, wy0 = 150, wy1 = 236;
  for (let y = wy0; y < wy1; y++) for (let x = wx0; x < wx1; x++) put(x, y, mix(hex("#1a2a6a"), hex("#3a4a9a"), (y - wy0) / (wy1 - wy0)));
  for (let i = 0; i < 14; i++) { const sx = wx0 + 4 + hash(i, 1) * (wx1 - wx0 - 8), sy = wy0 + 3 + hash(i, 2) * 50; put(sx, sy, hex("#ffffff"), (f + i * 9) % 50 < 4 ? 0.3 : 0.9); }
  paint(wx0 + 50, wy0 + 8, wx0 + 76, wy0 + 34, minus(circle(wx0 + 63, wy0 + 21, 11), circle(wx0 + 69, wy0 + 17, 9)), { base: hex("#fff4c0"), flat: true, line: null, rim: 0 });
  glow(wx0 + 63, wy0 + 21, 30, hex("#fff4c0"), 0.25);
  for (let x = wx0; x < wx1; x++) { const h = 14 + Math.floor(hash(Math.floor(x / 12), 3) * 16); for (let y = wy1 - h; y < wy1; y++) put(x, y, hex("#141a3a")); if (hash(Math.floor(x / 4), Math.floor((wy1 - h + 6) / 5)) > 0.7) put(x, wy1 - h + 6, hex("#ffd27a")); }
  rect(wx0 - 5, wy0 - 5, wx1 - wx0 + 10, 5, hex("#fff6ea")); rect(wx0 - 5, wy1, wx1 - wx0 + 10, 6, hex("#fff6ea")); rect(wx0 - 5, wy0, 5, wy1 - wy0, hex("#fff6ea")); rect(wx1, wy0, 5, wy1 - wy0, hex("#fff6ea"));
  rect((wx0 + wx1) / 2 - 1, wy0, 3, wy1 - wy0, hex("#fff6ea")); rect(wx0, (wy0 + wy1) / 2 - 1, wx1 - wx0, 3, hex("#fff6ea"));
  rect(wx0 - 8, wy1 + 6, wx1 - wx0 + 16, 4, hex("#e8d8c4"));
  // hanging pot plant in the window
  paint(wx1 - 30, wy1 - 2, wx1 - 6, wy1 + 8, rbox(wx1 - 18, wy1 + 2, 10, 5, 2), { base: hex("#d86a4a"), puff: 3 });
  for (let k = 0; k < 6; k++) paint(wx1 - 34, wy1 - 26, wx1 - 2, wy1, capsule(wx1 - 18, wy1 - 2, wx1 - 26 + k * 3.2, wy1 - 18 - (k % 2) * 6, 2.2, 1), { base: hex(k % 2 ? "#4aa04a" : "#6ac05a"), puff: 2, rim: 0 });
  // backsplash tiles
  for (let y = 250; y < COUNTER; y++) for (let x = 0; x < W; x++) {
    const gx = (x % 14), gy = ((y - 250) % 14);
    const grout = gx === 0 || gy === 0;
    const base = mix(hex("#7ac0c0"), hex("#a8e0d8"), sat(1 - Math.hypot((x - 80) / 280, (y - 300) / 200)) * lamp);
    put(x, y, grout ? mix(base, hex("#2a4a5a"), 0.35) : mix(base, hex("#ffffff"), (gx === 1 || gy === 1) ? 0.2 : 0));
  }
  // counter top + cabinets
  for (let y = COUNTER; y < COUNTER + 10; y++) for (let x = 0; x < W; x++) put(x, y, mix(hex("#c8875a"), hex("#8a4a2a"), (y - COUNTER) / 10 + noise(x * 0.3, y) * 0.15));
  for (let x = 0; x < W; x++) put(x, COUNTER, hex("#f0b88a"));
  for (let y = COUNTER + 10; y < H; y++) for (let x = 0; x < W; x++) put(x, y, hex("#3a5a7a"));
  for (const cx of [0, 90, 180]) { rect(cx + 6, COUNTER + 18, 78, 80, hex("#4a6a8a")); rect(cx + 6, COUNTER + 18, 78, 2, hex("#6a8aaa")); rect(cx + 70, COUNTER + 40, 3, 16, hex("#e8c87a")); }
  glow(80, 140, 120, hex("#ffcf8a"), 0.18 * lamp);
};

// ---------------- props ----------------
export const cake = (cx: number, by: number, bite = 0) => {
  paint(cx - 40, by - 8, cx + 40, by + 4, ell(cx, by - 2, 38, 6), { base: hex("#f4f4f8"), lite: hex("#ffffff"), dark: hex("#a8a8c0"), puff: 4 });
  const body = rbox(cx, by - 26, 30, 20, 4);
  paint(cx - 34, by - 50, cx + 34, by - 4, body, {
    base: hex("#fff0e0"), lite: hex("#ffffff"), dark: hex("#d8b8a0"), puff: 8,
    tex: (x, y, d) => (d < -2 && Math.abs(y - (by - 22)) < 2.5 ? hex("#ff7ab0") : d < -2 && Math.abs(y - (by - 34)) < 1.5 ? hex("#ffb8d0") : null),
  });
  for (let i = 0; i < 6; i++) { const x = cx - 26 + i * 10.4, h = 4 + hash(i, 4) * 7; paint(x - 4, by - 48, x + 4, by - 44 + h, capsule(x, by - 45, x, by - 44 + h, 3), { base: hex("#ffffff"), puff: 2 }); }
  for (let i = 0; i < 3; i++) {
    const x = cx - 14 + i * 14, y = by - 52;
    paint(x - 7, y - 8, x + 7, y + 6, blend(2, circle(x, y, 5.5), circle(x, y + 2, 4.5)), { base: hex("#e8283a"), lite: hex("#ff8a8a"), dark: hex("#8a1020"), puff: 4, tex: (px, py) => ((Math.floor(px) + Math.floor(py) * 2) % 5 === 0 ? hex("#ffe14e") : null) });
    paint(x - 4, y - 9, x + 4, y - 4, tri(x - 4, y - 5, x + 4, y - 5, x, y - 9), { base: hex("#4aa04a"), puff: 1, rim: 0 });
  }
};

export const fishPlate = (cx: number, by: number, f: number, eaten = 0) => {
  paint(cx - 38, by - 8, cx + 38, by + 4, ell(cx, by - 2, 36, 6), { base: hex("#f4f4f8"), lite: hex("#ffffff"), dark: hex("#a8a8c0"), puff: 4 });
  if (eaten >= 1) return;
  const wig = Math.sin(f * 0.3) * 1.5;
  push(cx, by - 12, 0, 1 - eaten * 0.5, 1);
  paint(-32, -14, 30, 12, union(ell(-2, 0, 22, 9), tri(18, 0, 32, -10 + wig, 32, 10 + wig)), {
    base: hex("#8ab0d0"), lite: hex("#e0f0ff"), dark: hex("#3a5a8a"), puff: 7,
    tex: (x, y, d) => (d < -2 && y > 2 ? hex("#e8e0f0") : d < -2 && (Math.floor(x / 4) + Math.floor(y / 3)) % 3 === 0 ? hex("#a8c8e8") : null),
  });
  paint(-22, -5, -14, 3, circle(-18, -2, 3), { base: hex("#1a1a2a"), flat: true, rim: 0, line: null });
  put(-19, -3, hex("#ffffff"));
  pop();
  for (let i = 0; i < 3; i++) { const t = ((f * 0.03 + i / 3) % 1); put(cx - 10 + i * 10 + Math.sin(t * 6) * 2, by - 26 - t * 22, hex("#ffffff"), 0.4 * (1 - t)); }
};

export const iceCream = (cx: number, by: number, licked: number) => {
  paint(cx - 22, by - 10, cx + 22, by + 2, ell(cx, by - 4, 20, 6), { base: hex("#7ac0e8"), lite: hex("#c8ecff"), dark: hex("#3a6aa8"), puff: 4 });
  paint(cx - 20, by - 18, cx + 20, by - 2, minus(ell(cx, by - 8, 19, 9), rbox(cx, by - 22, 22, 9, 0)), { base: hex("#7ac0e8"), lite: hex("#c8ecff"), dark: hex("#3a6aa8"), puff: 5 });
  const s = 1 - licked * 0.35;
  [["#fff0d8", -8], ["#ff9ac0", 8], ["#8a4a2a", 0]].forEach(([c, dx], i) => {
    const x = cx + (dx as number), y = by - 18 - (i === 2 ? 12 : 0);
    paint(x - 12, y - 12, x + 12, y + 10, circle(x, y, 10 * s), { base: hex(c as string), lite: hex("#ffffff"), puff: 7, tex: (px, py, d) => (d > -2.5 && py > y + 3 ? mix(hex(c as string), hex("#ffffff"), 0.2) : null) });
  });
};

// ---------------- the cat ----------------
export type CatPose = { lean: number; tail: number; eyes: "open" | "squint" | "wide" | "closed" | "wink"; tongue: number; lick: number; headTilt: number; mouth: "smile" | "o" | "flat" | "bleh"; ear: number; duck?: number };
const FUR = hex("#f0a050"), FURL = hex("#ffd8a0"), FURD = hex("#a8502a"), STRIPE = hex("#c86a2a"), CREAM = hex("#fff2dc");
const furMat = (stripes = true): Mat => ({
  base: FUR, lite: FURL, dark: FURD, puff: 16,
  tex: stripes ? (x, y, d) => { if (d < -2 && Math.sin(x * 0.42 + Math.sin(y * 0.1) * 2) > 0.62 && y < -40) return STRIPE; return null; } : undefined,
});
export const cat = (cx: number, by: number, s: number, P: CatPose, f: number) => {
  push(cx, by, 0, s, s);
  const sway = Math.sin(f * 0.08) * 6 * P.tail;
  // tail behind
  paint(-80, -100, -20, 0, union(capsule(-30, -10, -52, -22, 7), capsule(-52, -22, -62 + sway * 0.5, -52, 6.5), capsule(-62 + sway * 0.5, -52, -56 + sway, -82, 6)), { ...furMat(false), tex: (x, y) => (y < -62 && Math.floor((y + 200) / 8) % 2 === 0 ? STRIPE : null) });
  // body + haunch + chest
  const body = blend(10, ell(-6, -42, 38, 40), ell(-22, -22, 28, 22), ell(12 + P.lean * 4 + (P.duck ?? 0) * 10, -62 + (P.duck ?? 0) * 18, 24, 34));
  paint(-60, -110, 50, 4, body, { ...furMat(), tex: (x, y, d) => (ell(14 + P.lean * 4, -60, 13, 24)(x, y) < 0 && d < -2 ? CREAM : (d < -2 && Math.sin(x * 0.36 + y * 0.05) > 0.7 && x < 0 ? STRIPE : null)) });
  // front paws
  for (const px of [4, 22]) paint(px - 10, -30, px + 12, 3, capsule(px + P.lean * 3, -26, px + 2 + P.lean * 4, -3, 6, 7), { base: CREAM, lite: hex("#ffffff"), dark: hex("#d8b890"), puff: 6 });
  // head (leans toward the cake / sniffs)
  const dk = P.duck ?? 0, hx = 20 + P.lean * 16 + dk * 22, hy = -106 + P.lean * 10 + dk * 52;
  push(hx, hy, P.headTilt, 1, 1);
  const ear = (sgn: number) => { const ex = sgn * 18; return tri(ex - 13, -16, ex + 13 * (sgn > 0 ? 1 : 0.4) - (sgn > 0 ? 0 : 0), -18, ex + sgn * 6, -46 - P.ear * 4); };
  paint(-36, -52, 36, -10, union(ear(-1), ear(1)), { ...furMat(false), tex: (x, y) => (Math.abs(x) > 8 && y < -22 && Math.abs(x) < 26 && y > -40 && Math.abs((Math.abs(x) - 17)) < 5 - (y + 40) * -0.1 ? hex("#ff9ab0") : null) });
  const head = blend(6, ell(0, -4, 32, 28), ell(0, 8, 36, 20));
  paint(-40, -36, 40, 30, head, { ...furMat(), puff: 18, tex: (x, y, d) => (d < -2 && y < -14 && Math.abs(x) < 10 && Math.sin(x * 0.9) > 0.3 ? STRIPE : (ell(0, 14, 16, 12)(x, y) < 0 ? CREAM : null)) });
  // eyes
  for (const sx of [-13, 13]) {
    const ex = sx, ey = -2;
    if (P.eyes === "closed" || (P.eyes === "wink" && sx > 0) || (f + 13) % 90 < 3) { paint(ex - 8, ey - 4, ex + 8, ey + 6, arc(ex, ey - 2, 6, 0.4, 2.7, 1.1), flat("#3a1a10")); continue; }
    if (P.eyes === "squint") { paint(ex - 8, ey - 4, ex + 8, ey + 4, capsule(ex - 6, ey + (sx < 0 ? 2 : -1), ex + 6, ey + (sx < 0 ? -1 : 2), 1.3), flat("#3a1a10")); continue; }
    const big = P.eyes === "wide" ? 1.25 : 1;
    paint(ex - 9, ey - 10, ex + 9, ey + 10, ell(ex, ey, 7 * big, 8 * big), { base: hex("#9ad84a"), lite: hex("#e8ff9a"), dark: hex("#4a8a2a"), puff: 4, line: hex("#2a1a10") });
    const pw = P.eyes === "wide" ? 4.5 : 1.8;
    paint(ex - 6, ey - 8, ex + 6, ey + 8, ell(ex + P.lean * 1.5, ey, pw, 6.5 * big), flat("#1a0a10"));
    put(ex - 3, ey - 4, hex("#ffffff")); put(ex - 2, ey - 4, hex("#ffffff")); put(ex - 3, ey - 3, hex("#ffffff"));
    if (P.eyes === "wide") { put(ex + 2, ey + 3, hex("#ffffff")); }
  }
  // nose, mouth, tongue
  paint(-5, 6, 5, 12, tri(-4, 7, 4, 7, 0, 11), { base: hex("#ff8aa8"), puff: 2, rim: 0 });
  if (P.mouth === "o") paint(-5, 12, 5, 22, ell(0, 16, 3.5, 4), flat("#5a1a2a"));
  else paint(-9, 10, 9, 20, union(arc(-4, 12, 4, 0.2, 2.9, 0.9), arc(4, 12, 4, 0.2, 2.9, 0.9)), flat("#5a1a2a"));
  if (P.tongue > 0.02) paint(-6, 12, 6, 30, capsule(0, 15, 1, 15 + 12 * P.tongue, 4, 4.5), { base: hex("#ff6a8a"), lite: hex("#ffb0c0"), dark: hex("#c03a5a"), puff: 3, tex: (x) => (Math.abs(x) < 0.6 ? hex("#c03a5a") : null) });
  if (P.lick > 0.02) paint(-6, -2, 8, 22, capsule(0, 14, 4, 14 - 12 * P.lick, 4, 4.5), { base: hex("#ff6a8a"), lite: hex("#ffb0c0"), dark: hex("#c03a5a"), puff: 3 });
  // whiskers
  const wc = hex("#fff6e8");
  for (const sg of [-1, 1]) for (let k = 0; k < 3; k++) { const [x0, y0] = toWorld(sg * 14, 8 + k * 3), [x1, y1] = toWorld(sg * (40 + Math.sin(f * 0.1 + k) * 1.5), 2 + k * 6); line(x0, y0, x1, y1, wc, 0.85); }
  pop();
  pop();
};

// ---------------- inside the tongue ----------------
export const tongueBg = (f: number) => {
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const n = noise(x * 0.05, y * 0.05 + f * 0.003), cx = x % 22 - 11 + (Math.floor(y / 20) % 2) * 11, cy = y % 20 - 10, pap = Math.hypot(cx, cy) < 5.5;
    let c = mix(hex("#c84a6a"), hex("#ff8aa8"), 0.4 + 0.3 * n);
    if (pap) c = mix(c, hex("#ffc0d0"), 0.4 - Math.hypot(cx, cy) / 16);
    put(x, y, mix(c, hex("#5a1030"), sat(Math.hypot((x - 135) / 240, (y - 300) / 300) - 0.3)));
  }
};
/** a taste receptor "socket" on the cell membrane; broken = cracked and grey */
export const socket = (cx: number, cy: number, broken: boolean, glowAmt: number, L: Label[], label: string, color: string) => {
  paint(cx - 40, cy - 6, cx + 40, cy + 60, rbox(cx, cy + 30, 36, 26, 10), { base: hex("#ffb8c8"), lite: hex("#ffe0e8"), dark: hex("#c86a8a"), puff: 10 });
  const cup = minus(rbox(cx, cy, 22, 16, 6), rbox(cx, cy - 8, 13, 13, 4));
  paint(cx - 26, cy - 20, cx + 26, cy + 20, cup, {
    base: broken ? hex("#8a8a98") : mix(hex(color), hex("#ffffff"), glowAmt * 0.4), lite: broken ? hex("#c8c8d0") : hex("#ffffff"), dark: broken ? hex("#4a4a58") : mix(hex(color), hex("#000000"), 0.4), puff: 6,
    tex: broken ? (x, y) => (Math.abs((x - cx) * 0.8 + Math.sin(y * 0.8) * 2 - (y - cy) * 0.5) < 0.8 && y > cy - 4 ? hex("#2a2a38") : null) : undefined,
  });
  if (glowAmt > 0) glow(cx, cy - 4, 40, hex(color), 0.5 * glowAmt);
  L.push({ s: label, x: Math.round(cx - label.length * 4.5), y: cy + 30, c: broken ? "#ff4a6a" : color, size: 24 });
  if (broken) L.push({ s: "X", x: cx - 4, y: cy - 12, c: "#ff4a6a", size: 24 });
};
export const sugarCube = (x: number, y: number, rot: number) => {
  push(x, y, rot, 1, 1);
  paint(-12, -12, 12, 12, rbox(0, 0, 9, 9, 1.5), { base: hex("#ffffff"), lite: hex("#ffffff"), dark: hex("#c8d0e8"), puff: 4, tex: (px, py) => (hash(Math.floor(px + 50), Math.floor(py + 50)) > 0.85 ? hex("#e0e8ff") : null) });
  pop();
  for (let i = 0; i < 4; i++) { const a = i * 1.57 + rot * 2; put(x + Math.cos(a) * 15, y + Math.sin(a) * 15, hex("#ffffff"), 0.8); }
};
export const umami = (x: number, y: number, rot: number) => {
  push(x, y, rot, 1, 1);
  paint(-16, -16, 16, 16, blend(3, circle(-6, -4, 6), circle(6, -5, 5.5), circle(0, 6, 6.5), capsule(-6, -4, 6, -5, 2), capsule(0, 6, 6, -5, 2)), { base: hex("#ffb347"), lite: hex("#fff0a0"), dark: hex("#c8601a"), puff: 5 });
  pop();
};
export const hearts = (x: number, y: number, t: number) => {
  for (let i = 0; i < 3; i++) {
    const u = (t + i / 3) % 1, hx = x + Math.sin(u * 6 + i) * 8 + (i - 1) * 10, hy = y - u * 40;
    paint(hx - 6, hy - 6, hx + 6, hy + 6, union(circle(hx - 2.5, hy - 1.5, 3), circle(hx + 2.5, hy - 1.5, 3), tri(hx - 5.4, hy - 0.5, hx + 5.4, hy - 0.5, hx, hy + 5)), { base: hex("#ff5a8a"), flat: true, line: null, rim: 0, alpha: 1 - u });
  }
};
