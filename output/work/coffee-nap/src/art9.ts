import { W, H, RGB, Mat, hex, mix, sat, lerp, hash, noise, put, rect, glow, paint, push, pop, circle, ell, rbox, capsule, blend, union, minus, toWorld, light } from "./gfx";
import { arc, Label, headArt, Face, heroSil } from "./art";

const flat = (c: string, a = 1): Mat => ({ base: hex(c), flat: true, line: null, rim: 0, alpha: a });
export const DESK = 340;          // y of the desk top
export const SEAT = DESK + 70;    // local y = 0 of the sitter

// ---------------- rainy afternoon at a home desk (sun = 0 rain, 1 sunshine) ----------------
export const room = (f: number, sun: number) => {
  // teal wall with soft vertical wallpaper stripes
  for (let y = 0; y < DESK; y++) for (let x = 0; x < W; x++) {
    const st = Math.floor((x + 3) / 18) % 2 ? 0.04 : 0;
    put(x, y, mix(mix(hex("#24434f"), hex("#36606a"), y / DESK), hex("#4a7a7a"), st));
  }
  // window
  const wx0 = 30, wx1 = 240, wy0 = 140, wy1 = 262;
  for (let y = wy0; y < wy1; y++) {
    const rainSky = mix(hex("#5a7088"), hex("#9aaab8"), (y - wy0) / (wy1 - wy0));
    const sunSky = mix(hex("#3a8ae0"), hex("#bfe8ff"), (y - wy0) / (wy1 - wy0));
    const c = mix(rainSky, sunSky, sun);
    for (let x = wx0; x < wx1; x++) put(x, y, c);
  }
  // far roofs
  for (let x = wx0; x < wx1; x++) {
    const h = 18 + Math.floor(hash(Math.floor(x / 22), 4) * 22);
    for (let y = wy1 - h; y < wy1; y++) put(x, y, mix(mix(hex("#3a4a5a"), hex("#4a6a8a"), sun), hex("#2a3a4a"), (y - wy1 + h) / h * 0.4));
    if (x % 22 > 6 && x % 22 < 11 && (wy1 - h + 6) < wy1 - 4) for (let y = wy1 - h + 6; y < wy1 - h + 10; y++) put(x, y, mix(hex("#ffd27a"), hex("#cfe8ff"), sun), 0.8 * (1 - sun));
  }
  if (sun > 0) { glow(200, 170, 50, hex("#fff2b0"), 0.6 * sun); paint(186, 156, 214, 184, circle(200, 170, 11), { ...flat("#fff6c8"), alpha: sun }); }
  // clouds
  for (let i = 0; i < 3; i++) {
    const cx = ((i * 83 + f * 0.25) % 260) + 10, cy = 156 + (i % 2) * 14;
    paint(cx - 34, cy - 16, cx + 34, cy + 12, blend(6, ell(cx, cy, 24, 8), circle(cx - 9, cy - 5, 9), circle(cx + 8, cy - 7, 10)),
      { base: mix(hex("#7a8a9a"), hex("#ffffff"), sun), lite: mix(hex("#9aaaba"), hex("#ffffff"), sun), dark: mix(hex("#5a6a7a"), hex("#c8dcf0"), sun), puff: 8, rim: 0, line: null });
  }
  // rain streaks
  const rain = 1 - sun;
  if (rain > 0) for (let i = 0; i < 70; i++) {
    const x0 = wx0 + hash(i, 1) * (wx1 - wx0), sp = 5 + hash(i, 2) * 3, y = wy0 + ((hash(i, 3) * 200 + f * sp) % (wy1 - wy0));
    for (let k = 0; k < 5; k++) put(x0 - k * 0.4, y - k, hex("#d8e8f8"), 0.5 * rain * (1 - k / 5));
  }
  // drops running down the glass
  for (let i = 0; i < 8; i++) {
    const x = wx0 + 10 + hash(i, 7) * (wx1 - wx0 - 20), y = wy0 + ((hash(i, 8) * 120 + f * (0.6 + hash(i, 9))) % (wy1 - wy0 - 6));
    put(x, y, hex("#ffffff"), 0.7 * rain); put(x, y + 1, hex("#b8d0e8"), 0.7 * rain);
  }
  // frame + mullions
  const wood: Mat = { base: hex("#e8e0d0"), lite: hex("#ffffff"), dark: hex("#8a8a8a"), puff: 3 };
  paint(wx0 - 8, wy0 - 8, wx1 + 8, wy1 + 12, minus(rbox(135, (wy0 + wy1) / 2 + 2, (wx1 - wx0) / 2 + 6, (wy1 - wy0) / 2 + 8, 2), rbox(135, (wy0 + wy1) / 2, (wx1 - wx0) / 2, (wy1 - wy0) / 2, 0)), wood);
  paint(131, wy0, 139, wy1, rbox(135, (wy0 + wy1) / 2, 2.5, (wy1 - wy0) / 2, 0), wood);
  paint(wx0, 196, wx1, 206, rbox(135, 201, (wx1 - wx0) / 2, 2.5, 0), wood);
  // sunbeam on the wall when it clears up
  if (sun > 0) for (let y = wy1 + 12; y < DESK; y++) for (let x = 0; x < W; x++) {
    const u = x - (y - wy1) * 0.4; if (u > 60 && u < 230) put(x, y, hex("#fff0b0"), 0.12 * sun);
  }
  // hanging plant at the top left
  for (let y = 0; y < 34; y++) put(18, y, hex("#2a2a2a"));
  paint(4, 30, 34, 54, union(rbox(18, 42, 12, 9, 4)), { base: hex("#d86a3a"), lite: hex("#ffa86a"), dark: hex("#7a2a1a"), puff: 6 });
  for (let i = 0; i < 6; i++) { const a = -2.6 + i * 0.5, lx = 18 + Math.cos(a) * 14 + Math.sin(f * 0.05 + i) * 1.2, ly = 36 + Math.sin(a) * 8 + i * 6;
    paint(lx - 6, ly - 6, lx + 6, ly + 6, ell(lx, ly, 4.5, 3), { base: hex("#3a9a4a"), lite: hex("#7ad86a"), dark: hex("#1a5a2a"), puff: 3 }); }
};

// desk front + top (drawn over the sitter's lower body)
export const desk = () => {
  paint(-4, DESK - 4, W + 4, DESK + 12, rbox(135, DESK + 4, 150, 7, 2), {
    base: hex("#c8864a"), lite: hex("#f0b878"), dark: hex("#7a4a2a"), puff: 4,
    tex: (x, y) => (Math.sin(x * 0.12 + noise(x * 0.05, y * 0.4) * 4) > 0.9 ? hex("#b0703a") : null),
  });
  for (let y = DESK + 11; y < H; y++) for (let x = 0; x < W; x++) {
    const n = noise(x * 0.06, y * 0.5);
    let c = mix(hex("#8a5230"), hex("#5a321e"), (y - DESK) / (H - DESK) * 0.7 + n * 0.15);
    if (Math.abs(x - 135) < 70 && (y === DESK + 40 || y === DESK + 41)) c = hex("#3a2014");
    put(x, y, c);
  }
  paint(126, DESK + 22, 144, DESK + 32, rbox(135, DESK + 27, 7, 2.5, 1.5), { base: hex("#e0c070"), lite: hex("#fff0b0"), dark: hex("#8a6a2a"), puff: 2 });
  // lamp on the left with a warm glow
  paint(30, DESK - 12, 60, DESK + 2, ell(45, DESK - 2, 13, 4), { base: hex("#3a3a4a"), lite: hex("#6a6a7a"), puff: 4 });
  paint(36, DESK - 64, 56, DESK, union(capsule(45, DESK - 4, 40, DESK - 40, 2), capsule(40, DESK - 40, 52, DESK - 60, 2)), { base: hex("#3a3a4a"), lite: hex("#6a6a7a"), puff: 2 });
  paint(36, DESK - 76, 76, DESK - 48, (x, y) => Math.max(circle(56, DESK - 52, 15)(x, y), DESK - 60 - y), { base: hex("#f2c24a"), lite: hex("#fff0a0"), dark: hex("#a86a1a"), puff: 6 });
  glow(56, DESK - 40, 46, hex("#ffd27a"), 0.35);
  // notebook
  paint(64, DESK - 4, 116, DESK + 4, rbox(90, DESK, 24, 2.5, 1), { base: hex("#e85a6a"), lite: hex("#ff9aa0"), dark: hex("#8a1a3a"), puff: 2 });
};

// ---------------- the sitter: channel mascot in a mustard hoodie ----------------
const HOOD: Mat = { base: hex("#e8a83a"), lite: hex("#ffd87a"), dark: hex("#8a4a2a"), puff: 14 };
const SKIN: Mat = { base: hex("#f7c49a"), lite: hex("#ffe6c8"), dark: hex("#c9765e"), puff: 7 };
export type Sit = { face: Face; tilt: number; lift: number; hl: [number, number]; hr: [number, number]; mug?: "r" | null; mugTilt?: number; steam?: number };
const ik = (sx: number, sy: number, hx: number, hy: number, l1: number, l2: number, bend: number): [number, number, number, number] => {
  let dx = hx - sx, dy = hy - sy, d = Math.hypot(dx, dy);
  const mx = l1 + l2 - 0.5; if (d > mx) { hx = sx + dx / d * mx; hy = sy + dy / d * mx; dx = hx - sx; dy = hy - sy; d = mx; }
  const a = Math.acos(Math.max(-1, Math.min(1, (l1 * l1 + d * d - l2 * l2) / (2 * l1 * Math.max(d, 1e-3))))), b = Math.atan2(dy, dx) + bend * a;
  return [sx + Math.cos(b) * l1, sy + Math.sin(b) * l1, hx, hy];
};
export const sitterBody = (cx: number, P: Sit) => {
  push(cx, SEAT - P.lift, 0, 1, 1);
  paint(-30, -118, 30, -40, rbox(0, -80, 27, 34, 15), { ...HOOD, puff: 22, tex: (x, y) => (Math.abs(Math.abs(x) - 5) < 0.8 && y > -110 && y < -94 ? hex("#fff0d0") : null) });
  paint(-20, -124, 20, -106, ell(0, -114, 18, 7), { ...HOOD, base: hex("#c8862a"), puff: 6 });   // hood folded behind the neck
  push(0, -116, P.tilt, 1, 1);
  headArt(0, -30, P.face, "#5a3020");
  pop();
  pop();
};
export const sitterArms = (cx: number, P: Sit, f: number) => {
  push(cx, SEAT - P.lift, 0, 1, 1);
  const arm = (s: number, h: [number, number]) => {
    const [ex, ey, hx, hy] = ik(s * 25, -100, h[0], h[1] + P.lift, 22, 22, s > 0 ? 1 : -1);
    const x0 = Math.min(s * 25, ex, hx) - 10, x1 = Math.max(s * 25, ex, hx) + 10, y0 = Math.min(-100, ey, hy) - 10, y1 = Math.max(-100, ey, hy) + 10;
    paint(x0, y0, x1, y1, blend(3, capsule(s * 25, -100, ex, ey, 8, 7), capsule(ex, ey, hx, hy, 7, 6)), { ...HOOD, puff: 8 });
    paint(hx - 8, hy - 8, hx + 8, hy + 8, circle(hx, hy, 6.5), SKIN);
    return [hx, hy];
  };
  arm(-1, P.hl);
  const [rx, ry] = arm(1, P.hr);
  if (P.mug === "r") { const [X, Y] = toWorld(rx - 2, ry - 2); pop(); mug(X, Y, P.mugTilt ?? 0, P.steam ?? 1, f); return; }
  pop();
};

// coffee mug centred on (x, y); tilt rotates it towards the mouth
export const mug = (x: number, y: number, tilt: number, steam: number, f: number) => {
  push(x, y, tilt, 1, 1);
  paint(4, -8, 18, 8, minus(circle(9, 0, 6.5), circle(9, 0, 3.2)), { base: hex("#2ab0a0"), lite: hex("#7af0d8"), dark: hex("#0a5a5a"), puff: 3 });
  paint(-12, -14, 10, 13, rbox(-1, 0, 9, 11, 2.5), { base: hex("#2ab0a0"), lite: hex("#7af0d8"), dark: hex("#0a5a5a"), puff: 8, tex: (px, py) => (py > 2 && py < 5 ? hex("#ffffff") : null) });
  paint(-11, -14, 9, -8, ell(-1, -10.5, 8, 2), { base: hex("#5a2a14"), lite: hex("#8a4a24"), flat: true, line: null, rim: 0 });
  pop();
  if (steam > 0) for (let k = 0; k < 3; k++) for (let i = 0; i < 16; i++) {
    const u = ((i / 16 + f * 0.02 + k * 0.33) % 1), sx = x - 5 + k * 5 + Math.sin(u * 7 + f * 0.1 + k) * 2.5, sy = y - 14 - u * 26;
    put(sx, sy, hex("#ffffff"), 0.45 * steam * Math.sin(Math.PI * u));
  }
};

// twin-bell alarm clock sitting on the desk; ring = 0..1 shake
export const alarm = (x: number, f: number, ring: number, L: Label[]) => {
  const sh = ring > 0 ? Math.sin(f * 2.3) * 2 * ring : 0, y = DESK - 15, rot = ring > 0 ? Math.sin(f * 1.7) * 0.12 * ring : 0;
  push(x + sh, y, rot, 1, 1);
  const red: Mat = { base: hex("#e8403a"), lite: hex("#ff9a8a"), dark: hex("#7a1414"), puff: 8 };
  for (const s of [-1, 1]) paint(s * 9 - 7, -20, s * 9 + 7, -6, (px, py) => Math.max(circle(s * 9, -10, 6)(px, py), py + 10), red);
  paint(-6, -18, 6, -10, capsule(-4, -14, 4, -14, 1.2), { base: hex("#3a3a4a"), puff: 1 });
  for (const s of [-1, 1]) paint(s * 8 - 4, 6, s * 8 + 4, 16, capsule(s * 6, 9, s * 9, 14, 1.6), { base: hex("#3a3a4a"), puff: 1 });
  paint(-15, -15, 15, 15, circle(0, 0, 12.5), red);
  paint(-12, -12, 12, 12, circle(0, 0, 9.5), { base: hex("#fff8e8"), lite: hex("#ffffff"), dark: hex("#c8c0b0"), puff: 6, rim: 0 });
  paint(-3, -9, 3, 3, capsule(0, 0, 0, -7, 0.9), flat("#2a2a3a"));
  paint(-3, -3, 9, 3, capsule(0, 0, 6, 0, 0.9), flat("#2a2a3a"));
  pop();
  if (ring > 0) {
    for (const s of [-1, 1]) for (let k = 0; k < 2; k++) {
      const r = 18 + k * 6 + ((f * 0.5) % 6);
      for (let a = -0.6; a <= 0.6; a += 0.06) put(x + s * Math.cos(a) * r, y - 6 + Math.sin(a) * r, hex("#ffe14e"), 0.9 * ring);
    }
    L.push({ s: "RING!", x: x - 32, y: y - 46 + Math.round(Math.sin(f * 0.8) * 2), c: "#ffe14e", size: 16 });
  }
};

// energy battery overlay
export const battery = (x: number, y: number, lvl: number, a: number, L: Label[]) => {
  if (a <= 0) return;
  paint(x - 14, y - 34, x + 14, y + 34, minus(rbox(x, y + 2, 12, 30, 3), rbox(x, y + 2, 9, 27, 1)), { base: hex("#f2f2f2"), lite: hex("#ffffff"), dark: hex("#8a8a9a"), puff: 3, alpha: a });
  paint(x - 6, y - 34, x + 6, y - 26, rbox(x, y - 30, 5, 3, 1), { base: hex("#f2f2f2"), puff: 2, alpha: a });
  const c = lvl < 0.34 ? hex("#ff4a4a") : lvl < 0.67 ? hex("#ffd84a") : hex("#55efc4"), n = Math.max(1, Math.round(lvl * 5));
  for (let i = 0; i < n; i++) rect(x - 7, y + 24 - i * 10.5, 14, 8, c, a);
  if (a > 0.5) L.push({ s: "ENERGY", x: x - 17, y: y + 38, c: lvl > 0.67 ? "#55efc4" : "#ff6a6a", size: 16 });
};

// ---------------- inside view: caffeine on its way to the brain ----------------
export const PATH: [number, number][] = [[142, 392], [150, 360], [146, 336], [140, 318], [137, 300]];
export const along = (u: number): [number, number] => {
  const seg = PATH.length - 1, t = Math.min(seg - 1e-6, Math.max(0, u * seg)), k = Math.floor(t), r = t - k;
  return [lerp(PATH[k][0], PATH[k + 1][0], r), lerp(PATH[k][1], PATH[k + 1][1], r)];
};
export const inside = (f: number, kick: number) => {
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const v = Math.hypot((x - 135) / 200, (y - 300) / 260), g = (x % 15 === 0 || y % 15 === 0) ? 0.05 : 0;
    put(x, y, mix(mix(hex("#4a2a1e"), hex("#1a0c08"), sat(v)), hex("#c8864a"), g));
  }
  // silhouette, sepia "scan" style
  push(135, 474, 0, 1.25, 1.25);
  paint(-72, -192, 72, 4, heroSil({ armL: 0.3, armR: 0.3 }), { base: hex("#6a3a22"), lite: hex("#8a5232"), dark: hex("#3a1e12"), line: hex("#ffd8a0"), puff: 20, rim: 0 });
  pop();
  // vessel from the stomach to the brain
  for (let i = 0; i <= 120; i++) { const [px, py] = along(i / 120); put(px, py, hex("#ff7a5a"), 0.8); put(px + 1, py, hex("#c8402a"), 0.8); }
  // stomach with coffee
  paint(122, 372, 166, 408, blend(6, ell(144, 390, 15, 11), circle(134, 384, 8)), { base: hex("#ff9a8a"), lite: hex("#ffd0c0"), dark: hex("#a84a4a"), puff: 8,
    tex: (x, y) => (y > 390 + Math.sin(x * 0.4 + f * 0.2) ? hex("#6a3a1a") : null) });
  // brain
  const bc = mix(hex("#ff9ab8"), hex("#ffe08a"), kick);
  paint(106, 270, 168, 312, blend(5, ell(137, 290, 25, 17), circle(124, 286, 11), circle(150, 286, 11)), { base: bc, lite: mix(bc, hex("#ffffff"), 0.5), dark: mix(bc, hex("#5a1a3a"), 0.6), puff: 10,
    tex: (x, y, d) => (d < -2 && Math.abs(Math.sin((x - 137) * 0.35 + Math.cos((y - 290) * 0.4) * 2)) < 0.12 ? mix(bc, hex("#8a2a5a"), 0.5) : null) });
  if (kick > 0) glow(137, 290, 60, hex("#ffe14e"), 0.6 * kick);
};
export const caffeine = (x: number, y: number, r: number, a = 1) => {
  paint(x - r - 2, y - r - 2, x + r + 2, y + r + 2, circle(x, y, r), { base: hex("#ffd84a"), lite: hex("#fff6c0"), dark: hex("#c87a1a"), puff: r, alpha: a, line: hex("#4a2a0a") });
};

// ---------------- the synapse: adenosine leaves, caffeine moves in ----------------
export const MEM = 334;
export const RX = [48, 104, 166, 222];
export const synapse = (f: number, lit: number) => {
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const n = noise(x * 0.03 + f * 0.004, y * 0.03);
    put(x, y, mix(mix(hex("#2a1048"), hex("#5a1e5a"), n * 0.8), hex("#ffb84a"), lit * 0.18 * sat(1 - Math.abs(y - MEM) / 160)));
  }
  // floating background vesicles
  for (let i = 0; i < 14; i++) {
    const x = (hash(i, 1) * 300 + f * (0.2 + hash(i, 2) * 0.3)) % 290 - 10, y = 160 + hash(i, 3) * 140 + Math.sin(f * 0.05 + i) * 4, r = 2 + hash(i, 4) * 3;
    paint(x - r - 1, y - r - 1, x + r + 1, y + r + 1, circle(x, y, r), { base: hex("#7a4a9a"), lite: hex("#b88ad8"), puff: r, rim: 0, line: null, alpha: 0.6 });
  }
  // membrane of the next nerve cell
  const top = (x: number) => MEM + Math.sin(x * 0.05 + f * 0.04) * 3;
  for (let x = 0; x < W; x++) { const t = top(x); for (let y = Math.floor(t); y < H; y++) {
    const d = y - t; put(x, y, d < 2 ? hex("#ffd0f0") : d < 10 ? mix(hex("#e88ad0"), hex("#b85aa8"), d / 10) : mix(hex("#8a3a8a"), hex("#4a1a5a"), sat((d - 10) / 120)));
  } }
  for (const x of RX) {
    const t = top(x), gl = lit;
    paint(x - 14, t - 26, x + 14, t + 4, union(capsule(x, t + 2, x, t - 8, 3.5), capsule(x, t - 8, x - 9, t - 20, 3), capsule(x, t - 8, x + 9, t - 20, 3)),
      { base: mix(hex("#5ce1e6"), hex("#ffe14e"), gl), lite: hex("#ffffff"), dark: mix(hex("#1a6a8a"), hex("#a86a1a"), gl), puff: 4 });
    if (gl > 0) glow(x, t - 14, 26, hex("#ffe14e"), 0.5 * gl);
  }
};
export const RECV = (x: number, f: number) => MEM + Math.sin(x * 0.05 + f * 0.04) * 3 - 22;
export const blob = (x: number, y: number, kind: "aden" | "caf", f: number, a = 1) => {
  const aden = kind === "aden", r = 9;
  paint(x - r - 2, y - r - 2, x + r + 2, y + r + 2, aden ? blend(3, circle(x, y, r), circle(x - 6, y - 5, 4)) : circle(x, y, r),
    aden ? { base: hex("#9a6ae8"), lite: hex("#d0b0ff"), dark: hex("#4a2a8a"), puff: 8, alpha: a } : { base: hex("#ffd84a"), lite: hex("#fff6c0"), dark: hex("#c87a1a"), puff: 8, alpha: a });
  const ink: Mat = { ...flat("#1a1038"), alpha: a };
  if (aden) { for (const s of [-1, 1]) paint(x + s * 4 - 4, y - 4, x + s * 4 + 4, y + 2, arc(x + s * 4, y - 3, 2.6, 0.4, 2.7, 0.7), ink); }
  else { for (const s of [-1, 1]) { paint(x + s * 4 - 3, y - 5, x + s * 4 + 3, y + 1, circle(x + s * 4, y - 2, 2.2), ink); put(x + s * 4 - 1, y - 3, hex("#ffffff"), a); }
    paint(x - 4, y + 1, x + 4, y + 6, arc(x, y + 1, 3, 0.4, 2.7, 0.8), ink); }
};
