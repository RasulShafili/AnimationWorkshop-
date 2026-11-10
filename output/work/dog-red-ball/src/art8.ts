import { W, H, RGB, Mat, hex, mix, sat, lerp, hash, noise, put, rect, glow, paint, push, pop, circle, ell, rbox, capsule, blend, union, toWorld } from "./gfx";
import { arc, Label, body, headArt, Suit } from "./art";
import { tri } from "./art7";

const flat = (c: string, a = 1): Mat => ({ base: hex(c), flat: true, line: null, rim: 0, alpha: a });
export const GROUND = 392;

// ---------------- sunny park ----------------
export const park = (f: number) => {
  for (let y = 0; y < 300; y++) { const c = mix(hex("#4a9ae8"), hex("#bfe6ff"), Math.pow(y / 300, 1.3)); for (let x = 0; x < W; x++) put(x, y, c); }
  glow(222, 64, 70, hex("#fff6c0"), 0.5); paint(206, 48, 238, 80, circle(222, 64, 13), { base: hex("#fff6c0"), flat: true, line: null, rim: 0 });
  for (let i = 0; i < 4; i++) {           // drifting clouds
    const cx = ((i * 97 + f * 0.15) % 340) - 35, cy = 150 + (i % 2) * 40 + i * 6;
    paint(cx - 40, cy - 20, cx + 40, cy + 14, blend(6, ell(cx, cy, 26, 9), circle(cx - 10, cy - 6, 10), circle(cx + 8, cy - 9, 12)), { base: hex("#ffffff"), lite: hex("#ffffff"), dark: hex("#c8dcf0"), puff: 8, rim: 0 });
  }
  // distant tree line + far hills
  for (let x = 0; x < W; x++) { const h = 16 + noise(x * 0.03, 1) * 14; for (let y = 300 - h; y < 300; y++) put(x, y, mix(hex("#6aa86a"), hex("#4a8a5a"), (y - 300 + h) / h)); }
  for (let i = 0; i < 9; i++) { const tx = i * 32 + 8, ty = 296 - hash(i, 2) * 12, r = 14 + hash(i, 3) * 8;
    paint(tx - r - 2, ty - r * 2, tx + r + 2, ty + 4, blend(5, circle(tx, ty - r, r), circle(tx - r * 0.6, ty - r * 0.6, r * 0.7), circle(tx + r * 0.6, ty - r * 0.5, r * 0.7)), { base: hex("#3a8a4a"), lite: hex("#7ac86a"), dark: hex("#1a5a3a"), puff: 10 }); }
  // mowed lawn with stripes
  for (let y = 300; y < H; y++) { const z = (y - 300) / (H - 300); for (let x = 0; x < W; x++) {
    const u = (x - 135) / (0.4 + z * 1.4), stripe = Math.floor((u + 400) / 26) % 2;
    put(x, y, mix(stripe ? hex("#5ab84a") : hex("#4aa83e"), hex("#2a7a2a"), 0.15 - z * 0.15 + noise(x * 0.2, y * 0.3) * 0.08));
  } }
  // path, bench, flowers in three colours (they make the dog-vision difference obvious)
  for (let y = 318; y < 336; y++) for (let x = 0; x < W; x++) put(x, y, mix(hex("#e8d0a0"), hex("#c8a878"), noise(x * 0.3, y * 0.5) * 0.6));
  paint(14, 286, 74, 322, union(rbox(44, 306, 28, 3, 1), rbox(44, 296, 28, 3, 1), rbox(22, 314, 2, 8, 1), rbox(66, 314, 2, 8, 1)), { base: hex("#a85a2a"), lite: hex("#e09a5a"), dark: hex("#5a2a14"), puff: 3 });
  const FL: [number, number, string][] = [[100, 352, "#ff3a3a"], [118, 360, "#ffd84a"], [206, 350, "#3a7aff"], [226, 362, "#ff3a3a"], [244, 348, "#ffd84a"], [30, 360, "#3a7aff"], [62, 372, "#ff3a3a"], [150, 376, "#ff8a3a"], [254, 380, "#3a7aff"]];
  FL.forEach(([x, y, c], i) => {
    for (let k = 0; k < 8; k++) put(x, y + k, hex("#2a7a2a"));
    const sw = Math.sin(f * 0.06 + i) * 0.8;
    for (let p = 0; p < 5; p++) { const a = p / 5 * Math.PI * 2; paint(x + sw - 6, y - 6, x + sw + 6, y + 4, circle(x + sw + Math.cos(a) * 2.6, y - 1 + Math.sin(a) * 2.6, 2.2), { base: hex(c), puff: 2, rim: 0 }); }
    put(x + sw, y - 1, hex("#fff6a0"));
  });
};

// red fire hydrant (another red thing that "vanishes")
export const hydrant = (x: number, by: number) => {
  paint(x - 12, by - 36, x + 12, by + 2, union(rbox(x, by - 14, 7, 14, 2), circle(x, by - 28, 7.5), rbox(x, by - 1, 9, 2, 1), rbox(x, by - 18, 11, 2.5, 1)), { base: hex("#e8302a"), lite: hex("#ff8a7a"), dark: hex("#7a1010"), puff: 6 });
};

export const ball = (x: number, y: number, r: number, c: string, spin = 0) => {
  paint(x - r - 2, y - r - 2, x + r + 2, y + r + 2, circle(x, y, r), {
    base: hex(c), lite: mix(hex(c), hex("#ffffff"), 0.55), dark: mix(hex(c), hex("#000000"), 0.5), puff: r,
    tex: (px, py, d) => (d < -1 && Math.abs(Math.sin((px - x) * 0.5 + spin) * r * 0.6 - (py - y)) < 1 ? mix(hex(c), hex("#ffffff"), 0.35) : null),
  });
};
export const shadowBlob = (x: number, y: number, w: number) => { for (let j = -2; j <= 2; j++) for (let i = -w; i <= w; i++) if ((i * i) / (w * w) + (j * j) / 4 <= 1) put(x + i, y + j, hex("#1a4a1a"), 0.35); };

// ---------------- the dog (golden retriever, facing right) ----------------
export type DogPose = { run: number; phase: number; headDown: number; wag: number; mouthBall?: string; happy: number; look?: number };
const FUR: Mat = { base: hex("#e8a85a"), lite: hex("#ffe0a8"), dark: hex("#9a5a2a"), puff: 12 };
const FURD: Mat = { base: hex("#c88a42"), lite: hex("#e8b878"), dark: hex("#7a4a1a"), puff: 8 };
export const dog = (cx: number, by: number, s: number, P: DogPose, f: number) => {
  push(cx, by, 0, s, s);
  const st = P.run * 6, ph = P.phase;
  const leg = (x: number, a: number, m: Mat) => { const fx = x + Math.sin(a) * (6 + P.run * 10), fy = -2 + Math.min(0, Math.cos(a)) * 4 * P.run; paint(x - 10, -40, x + 18, 3, capsule(x, -30, fx, fy, 5, 4), m); paint(fx - 6, fy - 4, fx + 7, fy + 3, ell(fx + 2, fy, 5, 3), m); };
  // far legs (darker)
  leg(18 + st, ph + Math.PI, FURD); leg(-22 - st, ph, FURD);
  // tail
  const wag = Math.sin(f * (0.5 + P.happy * 0.4)) * 10 * P.wag;
  paint(-64, -76, -24, -30, union(capsule(-30, -42, -44, -56 + wag * 0.3, 5, 4), capsule(-44, -56 + wag * 0.3, -54 + wag * 0.4, -66 + wag, 4, 3)), { ...FUR, tex: (x, y) => (y > -60 && hash(Math.floor(x), Math.floor(y)) > 0.8 ? hex("#ffe0a8") : null) });
  // body
  paint(-48, -62, 50, -18, blend(8, ell(0, -40, 32 + st, 15), ell(26 + st, -42, 16, 17), ell(-24 - st, -40, 15, 16)), {
    ...FUR, tex: (x, y, d) => (d < -2 && y > -32 ? hex("#ffe8c0") : null),
  });
  // near legs
  leg(24 + st, ph, FUR); leg(-18 - st, ph + Math.PI, FUR);
  // head (drops to sniff the grass)
  const hd = P.headDown, hx = 44 + st + hd * 6, hy = -62 + hd * 38;
  push(hx, hy, hd * 0.55, 1, 1);
  paint(-14, -18, 30, 16, blend(5, circle(0, 0, 13), ell(14, 4, 12, 7.5)), { ...FUR, puff: 10, tex: (x, y) => (x > 8 && y > 4 ? hex("#ffe8c0") : null) });
  paint(20, -2, 30, 6, circle(25, 2, 3.4), { base: hex("#2a1a14"), lite: hex("#6a5a5a"), puff: 2, rim: 0 });
  // eye: wide when looking, closed-happy when happy
  if (P.happy > 0.6) paint(0, -8, 10, 0, arc(5, -2, 3.5, -2.8, -0.35, 0.9), flat("#2a1a14"));
  else { paint(1, -9, 10, 0, circle(5, -4, 2.8), flat("#2a1a14")); put(4, -6, hex("#ffffff")); }
  // floppy ear
  paint(-12, -14, 4, 16, ell(-4, 2 + Math.sin(f * 0.2) * P.run, 5.5, 11), FURD);
  // mouth / tongue / ball in mouth
  if (P.mouthBall) { const [bx, by2] = [26, 10]; paint(bx - 8, by2 - 8, bx + 8, by2 + 8, circle(bx, by2, 6.5), { base: hex(P.mouthBall), lite: mix(hex(P.mouthBall), hex("#ffffff"), 0.5), dark: mix(hex(P.mouthBall), hex("#000000"), 0.5), puff: 6 }); }
  else if (P.happy > 0.3) paint(12, 6, 24, 20, capsule(18, 9, 19, 15 + Math.sin(f * 0.6) * 1.5, 3, 3.5), { base: hex("#ff6a8a"), lite: hex("#ffb0c0"), puff: 3, rim: 0 });
  pop();
  // sniff puffs
  if (hd > 0.6) for (let i = 0; i < 3; i++) { const u = ((f * 0.08 + i / 3) % 1); const [px, py] = toWorld(hx + 32 + u * 10, hy + 6 - u * 8); put(px, py, hex("#ffffff"), 0.6 * (1 - u)); }
  pop();
};

// ---------------- the owner (channel mascot in a park jacket) ----------------
const JACKET: Suit = { pj: hex("#3a6ab8"), pjLite: hex("#7aa8f0"), pjDark: hex("#1a2a5a"), stripe: null, shoe: hex("#f2f2f2") };
export const owner = (cx: number, feet: number, armR: number, face: "smile" | "grin" | "o") => {
  for (let j = -6; j <= 6; j++) for (let i = -44; i <= 44; i++) if ((i * i) / 1936 + (j * j) / 36 <= 1) put(cx + i, feet + j, hex("#1a4a1a"), 0.35);
  push(cx, feet, 0, 0.82, 0.82);
  const b = body({ armL: 0.25, armR }, JACKET);
  headArt(0, -146, { eye: "open", mouth: face, lookX: 0.6 }, "#3a2418");
  if (b.raisedR) b.backArm(b.rx, b.ry, 1);
  pop();
};

// ---------------- eye mosaics: 3 cone types vs 2 ----------------
export const coneDisc = (cx: number, cy: number, r: number, colors: string[], f: number, L: Label[], label: string, labelC: string) => {
  paint(cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4, circle(cx, cy, r + 2), { base: hex("#2a1a2a"), lite: hex("#4a3a4a"), puff: 6 });
  for (let y = -r; y <= r; y += 6) for (let x = -r; x <= r; x += 6) {
    const ox = x + (Math.round(y / 6) % 2 ? 3 : 0); if (Math.hypot(ox, y) > r - 3) continue;
    const k = Math.floor(hash(Math.floor(ox + 100), Math.floor(y + 100)) * colors.length), tw = 0.75 + 0.25 * Math.sin(f * 0.2 + ox * 0.3 + y * 0.2);
    paint(cx + ox - 4, cy + y - 4, cx + ox + 4, cy + y + 4, circle(cx + ox, cy + y, 2.6), { base: mix(hex(colors[k]), hex("#ffffff"), 0.3 * tw), flat: true, line: null, rim: 0 });
  }
  L.push({ s: label, x: Math.round(cx - label.length * 4.5), y: cy + r + 10, c: labelC, size: 24 });
};
