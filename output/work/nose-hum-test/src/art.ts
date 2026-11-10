import {
  W, H, RGB, SDF, Mat, hex, mix, mul, scl, sat, clamp, lerp, sstep, hash, noise, fbm, put, addPx, rect, glow, paint, push, pop,
  circle, ell, rbox, capsule, blend, union, minus, light, toWorld, easeOut,
} from "./gfx";

export type Label = { s: string; x: number; y: number; c: string; size?: number; plain?: boolean };

// ---------- time of day ----------
type Key = { t: number; sky: RGB[]; tint: RGB; rim: RGB; lamp: number };
const K: Key[] = [
  { t: 0.0, sky: [hex("#3b3f9e"), hex("#e86f8a"), hex("#ffc26e")], tint: [1.04, 0.92, 0.9], rim: hex("#ffd27a"), lamp: 0.15 },
  { t: 0.25, sky: [hex("#2a6fe0"), hex("#67b9f2"), hex("#c9efff")], tint: [1.12, 1.1, 1.08], rim: hex("#fff0c0"), lamp: 0 },
  { t: 0.5, sky: [hex("#2a1a6e"), hex("#c23f83"), hex("#ff9440")], tint: [1.0, 0.8, 0.84], rim: hex("#ffa24e"), lamp: 0.75 },
  { t: 0.75, sky: [hex("#060a2c"), hex("#101a5e"), hex("#2c3192")], tint: [0.62, 0.66, 1.0], rim: hex("#8fb4ff"), lamp: 0.0 },
  { t: 1.0, sky: [hex("#3b3f9e"), hex("#e86f8a"), hex("#ffc26e")], tint: [1.04, 0.92, 0.9], rim: hex("#ffd27a"), lamp: 0.15 },
];
export const tod = (t: number): Key => {
  t = ((t % 1) + 1) % 1;
  let i = 0; while (i < K.length - 2 && t > K[i + 1].t) i++;
  const a = K[i], b = K[i + 1], u = (t - a.t) / (b.t - a.t);
  return { t, sky: a.sky.map((c, k) => mix(c, b.sky[k], u)), tint: mix(a.tint, b.tint, u), rim: mix(a.rim, b.rim, u), lamp: lerp(a.lamp, b.lamp, u) };
};

const star4 = (x: number, y: number, r: number, c: RGB, a = 1) => {
  x = Math.round(x); y = Math.round(y);
  for (let i = -r; i <= r; i++) { put(x + i, y, c, a); put(x, y + i, c, a); }
  if (r >= 3) { put(x - 1, y - 1, c, a * 0.7); put(x + 1, y - 1, c, a * 0.7); put(x - 1, y + 1, c, a * 0.7); put(x + 1, y + 1, c, a * 0.7); }
};
export const sparkle = star4;

// ---------- window ----------
const WX0 = 14, WX1 = 100, WY0 = 142, WY1 = 262;
const drawWindow = (k: Key, f: number) => {
  const tt = k.t, night = sstep(0.56, 0.68, tt) * (1 - sstep(0.9, 0.99, tt));
  for (let y = WY0; y < WY1; y++) {
    const u = (y - WY0) / (WY1 - WY0) * 2, i = Math.min(1, Math.floor(u));
    const c = mix(k.sky[i], k.sky[i + 1], u - i);
    for (let x = WX0; x < WX1; x++) put(x, y, c);
  }
  // stars
  if (night > 0.02) for (let i = 0; i < 70; i++) {
    const x = WX0 + hash(i, 3) * (WX1 - WX0), y = WY0 + hash(i, 7) * 85;
    const tw = 0.5 + 0.5 * Math.sin(f * 0.15 + i * 2.1);
    put(x, y, hex("#ffffff"), night * (0.4 + 0.6 * tw));
  }
  // sun / moon arc
  const sunP = tt < 0.6 ? tt / 0.6 : -1;
  if (sunP >= 0) {
    const sx = lerp(WX0 + 6, WX1 - 6, sunP), sy = WY1 - 34 - Math.sin(sunP * Math.PI) * 76;
    glow(sx, sy, 46, hex("#ffcf7a"), 0.55);
    paint(sx - 14, sy - 14, sx + 14, sy + 14, circle(sx, sy, 11), { base: hex("#ffe27a"), lite: hex("#fff8d6"), line: null, flat: true, rim: 0 });
  }
  if (night > 0.02) {
    const mx = 62, my = 186;
    glow(mx, my, 44, hex("#a9c6ff"), 0.4 * night);
    paint(mx - 18, my - 18, mx + 18, my + 18, circle(mx, my, 15), {
      base: hex("#f5e8a8"), lite: hex("#fffbe0"), dark: hex("#c9b46a"), line: null, puff: 15, rim: 0, alpha: night,
      tex: (x, y) => { const n = noise(x * 0.28, y * 0.28); return n > 0.62 ? hex("#d8c67e") : null; },
    });
  }
  // clouds
  for (let i = 0; i < 3; i++) {
    const cx = WX0 + ((i * 41 + f * (0.22 + i * 0.08)) % 118) - 16, cy = WY0 + 30 + i * 24;
    const blob = union(ell(cx, cy, 16, 6), ell(cx + 10, cy - 4, 10, 7), ell(cx - 11, cy + 1, 9, 5));
    const s: SDF = (x, y) => Math.max(blob(x, y), WX0 - x, x - WX1);
    const cc = mix(hex("#ffffff"), k.sky[1], 0.25 + night * 0.6);
    paint(cx - 22, cy - 13, cx + 22, cy + 9, s, { base: cc, lite: hex("#ffffff"), dark: mix(k.sky[0], cc, 0.55), line: null, puff: 6, rim: 0, alpha: 0.9 - night * 0.5 });
  }
  // skyline
  for (let x = WX0; x < WX1; x++) {
    const b = Math.floor((x - WX0) / 11), h = 14 + hash(b, 2) * 26;
    for (let y = Math.round(WY1 - h); y < WY1; y++) {
      const wlit = (x % 4 === 1) && (y % 5 === 2) && hash(b * 31 + (x >> 2), y) > 0.45 - 0.2 * (1 - sat(k.lamp + night));
      const c = mix(hex("#1b1450"), k.sky[0], 0.18);
      put(x, y, wlit && (night > 0.1 || k.lamp > 0.3) ? hex("#ffd86b") : c);
    }
  }
  // frame + muntins
  const wood: Mat = { base: hex("#a86a3c"), lite: hex("#e9b676"), dark: hex("#5e3226"), puff: 3 };
  paint(WX0 - 7, WY0 - 7, WX1 + 7, WY1 + 7, minus(rbox(57, 202, 50, 67, 2), rbox(57, 202, 43, 60, 1)), wood);
  paint(52, WY0, 62, WY1, rbox(57, 202, 2.5, 60, 1), wood);
  paint(WX0, 192, WX1, 208, rbox(57, 200, 43, 2.5, 1), wood);
  paint(WX0 - 12, WY1 + 4, WX1 + 12, WY1 + 16, rbox(57, WY1 + 10, 56, 5, 2), { ...wood, base: hex("#c98a50") });
};

const curtain = (x0: number, x1: number, f: number, tint: RGB) => {
  for (let y = 124; y < 288; y++) {
    const sway = Math.sin(y * 0.03 + f * 0.03) * 1.2;
    for (let x = x0; x < x1; x++) {
      const v = Math.sin((x + sway) * 0.95) * 0.5 + 0.5;
      const c = mix(hex("#2d1f86"), hex("#6a4be0"), v * v);
      put(x, y, mul(c, tint));
    }
    put(x1, y, mul(hex("#170f4a"), tint));
  }
};

// ---------- room ----------
export const room = (k: Key, f: number, labels: Label[]) => {
  light.tint = k.tint; light.rim = k.rim; light.rimAmt = 0.8;
  const night = sstep(0.56, 0.68, k.t) * (1 - sstep(0.9, 0.99, k.t));
  const wallT = hex("#1f1a6b"), wallB = hex("#4f33a8");
  for (let y = 0; y < 340; y++) for (let x = 0; x < W; x++) {
    let c = mix(wallT, wallB, Math.pow(y / 340, 1.3));
    const st = (x % 30) < 15 ? 1.05 : 0.97;
    c = scl(c, st);
    if ((x % 30) === 14 && (y % 30) < 15 && (y % 6) === 0) c = scl(c, 1.25);
    put(x, y, mul(c, k.tint));
  }
  // light spilling from the window
  glow(57, 200, 210, mix(k.sky[2], k.sky[1], 0.5), 0.34 * (1 - night * 0.6));
  // picture rail
  rect(0, 64, W, 3, mul(hex("#c9974e"), k.tint));
  rect(0, 67, W, 1, mul(hex("#120a3a"), k.tint));
  for (let y = 0; y < 64; y++) for (let x = 0; x < W; x++) put(x, y, mul(hex("#191459"), k.tint), 0.75);
  // wainscot
  rect(0, 276, W, 2, mul(hex("#c9974e"), k.tint), 0.9);
  for (let y = 278; y < 340; y++) for (let x = 0; x < W; x++) put(x, y, mul(hex("#2a1c78"), k.tint), 0.55);
  for (let i = 0; i < 6; i++) {
    const x = 10 + i * 46;
    rect(x, 288, 36, 1, mul(hex("#7a5ad8"), k.tint), 0.5); rect(x, 330, 36, 1, mul(hex("#100a40"), k.tint), 0.5);
    rect(x, 288, 1, 42, mul(hex("#7a5ad8"), k.tint), 0.5); rect(x + 36, 288, 1, 43, mul(hex("#100a40"), k.tint), 0.5);
  }
  // floor
  const sunX = lerp(-30, 210, sat(k.t / 0.55));
  for (let y = 340; y < H; y++) {
    const p = (y - 340) / 140, row = Math.floor(Math.sqrt(p) * 11), rp = Math.sqrt(p) * 11 - row, sc = 1 + p * 1.4;
    for (let x = 0; x < W; x++) {
      const u = (x - 135) / sc + 400, seg = Math.floor((u + hash(row, 9) * 60) / 62);
      const v = hash(seg, row);
      let c = mix(hex("#7a4a30"), hex("#b37a4a"), v);
      c = scl(c, 0.86 + 0.28 * noise(u * 0.09, row * 7 + rp * 2));
      if (rp < 0.09 || ((u + hash(row, 9) * 60) % 62) < 1.2) c = hex("#3a1f2a");
      c = scl(c, lerp(1.08, 0.62, p));
      c = mul(c, k.tint);
      // window light patch on the floor
      const skew = sunX + p * 90, xx = x - skew;
      if (night < 0.5 && xx > 0 && xx < 78 + p * 40 && p < 0.8 && Math.abs(xx - (39 + p * 20)) > 2) {
        c = mix(c, mix(k.sky[2], hex("#fff2c6"), 0.5), 0.32 * (1 - p));
      }
      if (night > 0.5 && x > 40 + p * 60 && x < 120 + p * 90 && p < 0.7) c = mix(c, hex("#7f9dff"), 0.14 * (1 - p));
      put(x, y, c);
    }
  }
  rect(0, 334, W, 8, mul(hex("#d9c6a8"), k.tint));
  rect(0, 334, W, 1, mul(hex("#fff0d8"), k.tint));
  rect(0, 342, W, 2, mul(hex("#2a1538"), k.tint));

  // sign on the picture rail (channel watermark)
  paint(72, 40, 198, 62, rbox(135, 51, 62, 10, 2), { base: hex("#3a2a7a"), lite: hex("#4d3a9a"), line: hex("#c9974e"), puff: 3, rim: 0 });
  labels.push({ s: "LEARN WITH 8-BIT", x: 88, y: 46, c: "#c9a860" });

  drawWindow(k, f);
  rect(0, 122, 118, 3, mul(hex("#c9974e"), k.tint));
  curtain(0, 16, f, k.tint);
  curtain(98, 112, f + 30, k.tint);

  // floor lamp
  const on = k.lamp;
  paint(240, 240, 256, 345, rbox(248, 292, 1.5, 54, 1), { base: hex("#c9974e"), puff: 2 });
  paint(232, 338, 264, 350, ell(248, 345, 14, 4), { base: hex("#9a6a3a"), puff: 4 });
  paint(222, 200, 274, 246, (x, y) => Math.max(Math.abs(x - 248) - (14 + (y - 205) * 0.34), Math.abs(y - 224) - 19), {
    base: mix(hex("#a87a3a"), hex("#ffd46e"), 0.25 + on * 0.75), lite: mix(hex("#c9974e"), hex("#fff2c0"), on), dark: hex("#a0542a"), puff: 12, rim: 0,
    tex: (x, y) => (Math.floor(x / 5) % 2 === 0 ? null : mix(hex("#8a5a2a"), hex("#ffbf55"), on)),
  });
  if (on > 0.02) { glow(248, 250, 150, hex("#ffa548"), 0.5 * on); glow(248, 225, 60, hex("#fff0b0"), 0.45 * on); }

  // potted plant
  const pl = (dx: number, h: number, ang: number, i: number) => {
    const sw = Math.sin(f * 0.04 + i) * 2, tx = 208 + dx + Math.sin(ang) * h + sw, ty = 322 - Math.cos(ang) * h;
    paint(Math.min(208 + dx, tx) - 8, ty - 8, Math.max(208 + dx, tx) + 8, 330, capsule(208 + dx, 326, tx, ty, 2, 6), {
      base: hex("#2fae7a"), lite: hex("#8ae8a0"), dark: hex("#0f5a60"), puff: 4,
    });
  };
  pl(-3, 34, -0.5, 1); pl(3, 40, 0.42, 2); pl(0, 46, 0.02, 3);
  paint(192, 322, 224, 352, (x, y) => Math.max(Math.abs(x - 208) - (14 - (y - 325) * 0.14), Math.abs(y - 338) - 13), { base: hex("#d8643e"), lite: hex("#ff9a60"), dark: hex("#7a2a3e"), puff: 9 });
};

export const rug = (cx: number, cy: number, k: Key) => {
  paint(cx - 112, cy - 30, cx + 112, cy + 30, ell(cx, cy, 106, 25), {
    base: hex("#7a2360"), lite: hex("#a53a78"), dark: hex("#4a1650"), line: hex("#2a0f3a"), puff: 30, rim: 0,
    tex: (x, y) => {
      const r = Math.hypot((x - cx) / 106, (y - cy) / 25);
      if (r > 0.86 && r < 0.92) return hex("#e8b44e");
      if (r > 0.6 && r < 0.64) return hex("#e8b44e");
      if (r > 0.64 && r < 0.84 && (Math.floor((Math.atan2((y - cy) * 4, x - cx) + 7) * 9) % 2 === 0) && Math.abs(r - 0.74) < 0.03) return hex("#ff8fa8");
      return null;
    },
  });
};

// ---------- hero ----------
export type Face = { eye: "open" | "half" | "closed" | "wide" | "wink"; mouth: "smile" | "flat" | "o" | "grin" | "sleep"; lookX?: number; lookY?: number; blink?: boolean };
export type Pose = { armL: number; armR: number }; // angle from straight down, radians, positive = outwards

const armEnd = (sx: number, ang: number, side: number): [number, number] => [sx + side * Math.sin(ang) * 46, -102 + Math.cos(ang) * 46];

const SKIN: Mat = { base: hex("#f7c49a"), lite: hex("#ffe6c8"), dark: hex("#c9765e"), puff: 12 };

export const arc = (cx: number, cy: number, r: number, a0: number, a1: number, th: number): SDF => (x, y) => {
  const a = Math.atan2(y - cy, x - cx);
  const aa = clamp(a, a0, a1);
  return Math.hypot(x - (cx + Math.cos(aa) * r), y - (cy + Math.sin(aa) * r)) - th;
};

export const headArt = (cx: number, cy: number, face: Face, hairC = "#e0702e") => {
  const hair: Mat = { base: hex(hairC), lite: hex("#ffb04e"), dark: hex("#7a2a3a"), puff: 14 };
  paint(cx - 40, cy - 12, cx - 26, cy + 12, circle(cx - 33, cy + 3, 6), SKIN);
  paint(cx + 26, cy - 12, cx + 40, cy + 12, circle(cx + 33, cy + 3, 6), SKIN);
  paint(cx - 36, cy - 34, cx + 36, cy + 34, ell(cx, cy, 33, 31), { ...SKIN, puff: 26 });
  // cheeks: dithered blush
  for (const s of [-1, 1]) for (let j = -5; j <= 5; j++) for (let i = -8; i <= 8; i++) {
    if ((i * i) / 64 + (j * j) / 25 > 1) continue;
    const [X, Y] = toWorld(cx + s * 21 + i, cy + 11 + j);
    put(Math.floor(X), Math.floor(Y), mul(hex("#ff7f8f"), light.tint), 0.22);
  }
  // eyes
  const dark = hex("#1a1038");
  for (const s of [-1, 1]) {
    const ex = cx + s * 13, ey = cy + 1;
    const shut = face.eye === "closed" || face.blink || (face.eye === "wink" && s > 0);
    if (shut) {
      const up = face.eye === "wink" ? arc(ex, ey + 4, 7, -2.8, -0.35, 1) : arc(ex, ey - 4, 7, 0.35, 2.8, 1);
      paint(ex - 10, ey - 8, ex + 10, ey + 8, up, { base: dark, flat: true, line: null, rim: 0 });
      continue;
    }
    const big = face.eye === "wide" ? 1.18 : 1;
    const rx = 7.5 * big, ry = 8.8 * big;
    paint(ex - 11, ey - 12, ex + 11, ey + 12, ell(ex, ey, rx, ry), { base: hex("#ffffff"), flat: true, rim: 0 });
    const lx = ex + (face.lookX ?? 0) * 2.4, ly = ey + (face.lookY ?? 0) * 2.4;
    const pr = face.eye === "wide" ? 3.6 : 5.2;
    paint(lx - 7, ly - 7, lx + 7, ly + 7, circle(lx, ly, pr), { base: hex("#3a1f5e"), flat: true, line: null, rim: 0 });
    paint(lx - 3, ly - 5, lx + 1, ly - 1, circle(lx - 1.6, ly - 2.4, 1.7), { base: hex("#ffffff"), flat: true, line: null, rim: 0 });
    if (face.eye === "half") {
      paint(ex - 10, ey - 11, ex + 10, ey, (x, y) => Math.max(ell(ex, ey, rx + 1.2, ry + 1.2)(x, y), y - (ey - 1)), { base: hex("#e7a57e"), flat: true, line: null, rim: 0 });
      paint(ex - 10, ey - 3, ex + 10, ey + 1, rbox(ex, ey - 1, rx, 0.8, 0.4), { base: dark, flat: true, line: null, rim: 0 });
    }
  }
  // mouth
  const mm: Mat = { base: hex("#7a2a3a"), flat: true, line: null, rim: 0 };
  const my = cy + 16;
  if (face.mouth === "smile") paint(cx - 9, my - 5, cx + 9, my + 7, arc(cx, my - 4, 6.5, 0.45, 2.7, 1), mm);
  if (face.mouth === "flat") paint(cx - 7, my, cx + 7, my + 4, capsule(cx - 4, my + 2, cx + 4, my + 2, 1), mm);
  if (face.mouth === "o") paint(cx - 6, my - 4, cx + 6, my + 8, ell(cx, my + 2, 4, 5), { ...mm, line: hex("#1a1038") });
  if (face.mouth === "sleep") paint(cx - 5, my - 2, cx + 5, my + 6, arc(cx, my, 3, 0.3, 2.8, 0.8), mm);
  if (face.mouth === "grin") {
    paint(cx - 12, my - 5, cx + 12, my + 10, (x, y) => Math.max(circle(cx, my - 3, 11)(x, y), my - 1 - y), {
      base: hex("#8a2a4a"), flat: true, tex: (x, y) => (y < my + 2 ? hex("#ffffff") : y > my + 5 ? hex("#ff7f8f") : null), rim: 0,
    });
  }
  // hair: cap with a zig-zag fringe + cowlick
  const fringe = (x: number) => cy - 13 + Math.abs(((x - cx + 60) % 13) - 6.5) * 1.3;
  const cap: SDF = (x, y) => Math.max(ell(cx, cy - 3, 35, 33)(x, y), y - fringe(x));
  const tuft = blend(4, cap, capsule(cx + 3, cy - 30, cx - 3, cy - 44, 7, 1.5), capsule(cx + 9, cy - 30, cx + 16, cy - 41, 6, 1.2));
  paint(cx - 40, cy - 50, cx + 40, cy + 2, tuft, {
    ...hair, tex: (x, y) => (Math.sin((x - cx) * 0.55 + (y - cy) * 0.12) > 0.82 ? hex("#ffa24e") : null),
  });
};

export type Suit = { pj: RGB; pjLite: RGB; pjDark: RGB; stripe: RGB | null; shoe: RGB };
const PJ: Suit = { pj: hex("#17a58f"), pjLite: hex("#62e8c0"), pjDark: hex("#0c4a6e"), stripe: hex("#0f7f86"), shoe: hex("#ffc94e") };
export const SPACE: Suit = { pj: hex("#e9ecf6"), pjLite: hex("#ffffff"), pjDark: hex("#6a78b8"), stripe: null, shoe: hex("#ff7a4e") };

export const heroSil = (pose: Pose): SDF => {
  const [lx, ly] = armEnd(-27, pose.armL, -1), [rx, ry] = armEnd(27, pose.armR, 1);
  return union(
    capsule(-13, -52, -14, -10, 11, 9), capsule(13, -52, 14, -10, 11, 9), rbox(-16, -6, 14, 6, 5), rbox(16, -6, 14, 6, 5),
    rbox(0, -80, 27, 34, 15), capsule(-27, -102, lx, ly, 8, 7), capsule(27, -102, rx, ry, 8, 7), ell(0, -146, 34, 32),
  );
};

export const body = (pose: Pose, suit: Suit = PJ) => {
  const m: Mat = {
    base: suit.pj, lite: suit.pjLite, dark: suit.pjDark, puff: 14,
    tex: suit.stripe ? (x, y) => (Math.floor((x + 400) / 8) % 2 === 0 ? mix(suit.stripe!, suit.pj, 0.35) : null) : undefined,
  };
  paint(-34, -6 - 8, 34, 2, union(rbox(-16, -6, 14, 6, 5), rbox(16, -6, 14, 6, 5)), { base: suit.shoe, lite: hex("#fff0a8"), dark: hex("#c9574e"), puff: 6 });
  paint(-28, -66, -2, -8, capsule(-13, -52, -14, -11, 11, 9), m);
  paint(2, -66, 28, -8, capsule(13, -52, 14, -11, 11, 9), m);
  const [lx, ly] = armEnd(-27, pose.armL, -1), [rx, ry] = armEnd(27, pose.armR, 1);
  const armM: Mat = { ...m, puff: 8 };
  const backArm = (ax: number, ay: number, s: number) => {
    const sx = s * 27;
    paint(Math.min(sx, ax) - 11, Math.min(-102, ay) - 11, Math.max(sx, ax) + 11, Math.max(-102, ay) + 11, capsule(sx, -102, ax, ay, 8, 7), armM);
    paint(ax - 9, ay - 9, ax + 9, ay + 9, circle(ax, ay, 7), { ...SKIN, puff: 7 });
  };
  const raised = (a: number) => a > 1.4 || a < -0.3; // raised or crossing the chest: draw in front
  if (!raised(pose.armL)) backArm(lx, ly, -1);
  if (!raised(pose.armR)) backArm(rx, ry, 1);
  paint(-30, -116, 30, -44, rbox(0, -80, 27, 34, 15), { ...m, puff: 22 });
  // collar + pocket with a star
  if (suit.stripe) {
    paint(-14, -116, 14, -100, (x, y) => Math.max(Math.abs(x) + (y + 114) * -0.9 - 4, Math.abs(y + 108) - 6), { base: hex("#d9fff0"), puff: 3, rim: 0 });
    paint(4, -92, 22, -74, rbox(13, -83, 8, 8, 2), { base: suit.pjLite, lite: hex("#c8fff0"), dark: suit.pj, puff: 3, rim: 0 });
    const [px, py] = toWorld(13, -83);
    star4(px, py, 3, hex("#ffe14e"));
  } else {
    paint(-16, -96, 16, -70, rbox(0, -84, 14, 10, 3), { base: hex("#3a4a8a"), lite: hex("#5a6ab8"), dark: hex("#1a2a5a"), puff: 4, rim: 0 });
    for (let i = 0; i < 3; i++) { const [px, py] = toWorld(-7 + i * 7, -84); put(px, py, hex(["#ff5a5a", "#ffe14e", "#5ce1e6"][i])); put(px + 1, py, hex(["#ff5a5a", "#ffe14e", "#5ce1e6"][i])); put(px, py + 1, hex(["#ff5a5a", "#ffe14e", "#5ce1e6"][i])); put(px + 1, py + 1, hex(["#ff5a5a", "#ffe14e", "#5ce1e6"][i])); }
  }
  return { raisedL: raised(pose.armL), raisedR: raised(pose.armR), lx, ly, rx, ry, backArm };
};

export const hero = (cx: number, feet: number, sy: number, pose: Pose, face: Face, tilt = 0) => {
  // contact shadow
  for (let j = -7; j <= 7; j++) for (let i = -56; i <= 56; i++) {
    if ((i * i) / 3136 + (j * j) / 49 > 1) continue;
    put(cx + i, feet + j, hex("#1a0a3a"), 0.5);
  }
  push(cx, feet, tilt, 1, sy);
  const b = body(pose);
  headArt(0, -146, face);
  if (b.raisedL) b.backArm(b.lx, b.ly, -1);
  if (b.raisedR) b.backArm(b.rx, b.ry, 1);
  pop();
};

// ---------- x-ray ----------
export const xrayHero = (cx: number, feet: number, sy: number, pose: Pose, f: number) => {
  push(cx, feet, 0, 1, sy);
  const cy = hex("#7df6ff"), blue = hex("#0a2a72");
  paint(-70, -190, 70, 4, heroSil(pose), { base: blue, lite: hex("#14489a"), dark: hex("#061a50"), line: cy, puff: 20, rim: 0 });
  const bone: Mat = { base: hex("#d8fbff"), lite: hex("#ffffff"), dark: hex("#5ab8e0"), line: hex("#0a2a72"), puff: 5, rim: 0 };
  // skull
  paint(-30, -176, 30, -120, blend(5, ell(0, -152, 25, 22), rbox(0, -130, 13, 9, 4)), { ...bone, puff: 16 });
  for (const s of [-1, 1]) paint(s * 11 - 8, -152, s * 11 + 8, -134, ell(s * 11, -144, 6.5, 7), { base: hex("#0a2a72"), flat: true, line: null, rim: 0 });
  paint(-3, -136, 3, -128, ell(0, -132, 2, 3), { base: hex("#0a2a72"), flat: true, line: null, rim: 0 });
  // ribs
  for (let i = 0; i < 4; i++) {
    const y = -103 + i * 9;
    paint(-26, y - 7, 26, y + 8, arc(0, y - 6, 21 - i, 0.3, 2.84, 1.3), { ...bone, line: null, flat: true, base: hex("#a8ecff") });
  }
  // pelvis + legs + arms
  paint(-26, -66, 26, -40, blend(4, ell(-11, -54, 13, 10), ell(11, -54, 13, 10)), { ...bone, puff: 8 });
  for (const s of [-1, 1]) paint(s * 13 - 7, -48, s * 13 + 7, -10, capsule(s * 13, -46, s * 14, -12, 2.6), bone);
  const [lx, ly] = armEnd(-27, pose.armL, -1), [rx, ry] = armEnd(27, pose.armR, 1);
  paint(Math.min(-27, lx) - 6, -110, -20, ly + 6, capsule(-27, -102, lx, ly, 2.4), bone);
  paint(20, -110, Math.max(27, rx) + 6, ry + 6, capsule(27, -102, rx, ry, 2.4), bone);
  // spine: the star of the show
  const n = 9;
  for (let i = 0; i < n; i++) {
    const y = -118 + i * 7.4;
    paint(-8, y - 4, 8, y + 4, rbox(0, y, 6, 2.4, 1), { ...bone, base: hex("#fff6c8"), lite: hex("#ffffff"), dark: hex("#e0b060") });
    if (i < n - 1) {
      const pulse = 0.55 + 0.45 * Math.sin(f * 0.35 - i * 0.8);
      paint(-7, y + 2, 7, y + 6, rbox(0, y + 3.7, 5, 1.2, 1), { base: hex("#ff5fa8"), flat: true, line: null, rim: 0 });
      const [X, Y] = toWorld(0, y + 3.7);
      glow(X, Y, 11, hex("#ff5fa8"), 0.4 * pulse);
    }
  }
  pop();
};

// ---------- ruler + tag ----------
export const ruler = (x: number, top: number, bottom: number, k: Key) => {
  paint(x - 11, top - 3, x + 11, bottom + 3, rbox(x, (top + bottom) / 2, 9, (bottom - top) / 2, 2), {
    base: hex("#e4bf7c"), lite: hex("#ffe9b8"), dark: hex("#9a6236"), puff: 6,
    tex: (lx, ly, d, lam) => (Math.sin(lx * 0.8 + noise(lx * 0.2, ly * 0.04) * 6) > 0.86 ? hex("#c99a5c") : null),
  });
  for (let y = bottom - 4, i = 0; y > top + 2; y -= 5, i++) {
    const big = i % 5 === 0;
    rect(x - 8, y, big ? 9 : 5, 1, mul(hex("#4a2a2a"), k.tint));
  }
};

// ---------- spine macro ----------
const BONE: Mat = { base: hex("#f1dcae"), lite: hex("#fff8e0"), dark: hex("#a9673f"), puff: 30 };
export const vertebra = (cx: number, cy: number) => {
  const hw = 60, hh = 36;
  const wings = union(capsule(cx - hw - 16, cy + 4, cx - hw + 8, cy, 7, 12), capsule(cx + hw + 16, cy + 4, cx + hw - 8, cy, 7, 12));
  paint(cx - hw - 28, cy - 18, cx + hw + 28, cy + 18, wings, { ...BONE, base: hex("#d2a878"), lite: hex("#f0d2a0"), dark: hex("#6e3a4e"), puff: 9 });
  const s: SDF = (x, y) => {
    // superellipse: soft dome without the mitred creases a box SDF gives
    const dy = (y - cy) / hh, w = hw - 7 * (1 - dy * dy * dy * dy);
    const a = Math.abs(x - cx) / w, b = Math.abs(y - cy) / hh;
    return (Math.pow(a ** 5 + b ** 5, 0.2) - 1) * hh;
  };
  paint(cx - hw - 2, cy - hh - 2, cx + hw + 2, cy + hh + 2, s, {
    ...BONE,
    tex: (x, y, d, lam) => {
      // raised end plates + a few tiny pores, like the real thing
      const e = Math.abs(y - cy);
      if (e > hh - 8 && e < hh - 6 && d < -3) return mix(hex("#c08a5c"), hex("#e8c690"), lam);
      const gx = Math.floor(x / 7), gy = Math.floor((y - cy + 80) / 6);
      if (d < -9 && e < hh - 11 && hash(gx, gy) > 0.86 && Math.floor(x) % 7 === 3 && Math.floor(y - cy + 80) % 6 === 2) return mix(hex("#b07a50"), hex("#d8ae78"), lam);
      return null;
    },
  });
};

export type DiscFace = "happy" | "pain" | "tired" | "sleep" | "awake" | "blink";
export const disc = (cx: number, cy: number, h: number, water: number, face: DiscFace, f: number, dim = 0) => {
  const hw = 74 + (56 - h) * 0.55, hh = h / 2;
  const s = rbox(cx, cy, hw, hh, hh * 0.92);
  paint(cx - hw - 2, cy - hh - 2, cx + hw + 2, cy + hh + 2, s, {
    base: hex("#f4688a"), lite: hex("#ffb6bc"), dark: hex("#7a2078"), puff: Math.max(6, hh * 0.9),
    tex: (x, y, d, lam) => {
      const band = Math.sin(d * 1.15);
      if (band > 0.72 && d < -2) return mix(hex("#c23a86"), hex("#ff8fa8"), lam);
      return null;
    },
  });
  if (dim > 0) { paint(cx - hw - 2, cy - hh - 2, cx + hw + 2, cy + hh + 2, s, { base: hex("#1a1050"), flat: true, line: null, rim: 0, alpha: dim }); return; }
  // nucleus: translucent jelly with sloshing water
  const nw = hw * 0.74, nh = Math.max(5, hh * 0.72);
  const ns = rbox(cx, cy, nw, nh, nh * 0.95);
  const top = cy + nh - (nh * 2) * water;
  paint(cx - nw - 2, cy - nh - 2, cx + nw + 2, cy + nh + 2, ns, {
    base: hex("#ffc9d4"), line: hex("#b0307e"), puff: 8, rim: 0,
    tex: (x, y) => {
      const wv = top + Math.sin(x * 0.11 + f * 0.22) * 1.8 + Math.sin(x * 0.05 - f * 0.13) * 1.4;
      if (y < wv) return mix(hex("#ffd8e0"), hex("#ffb0c8"), sat((y - cy + nh) / (nh * 2)));
      if (y < wv + 1.4) return hex("#d8fbff");
      return mix(hex("#3cc4ff"), hex("#1c58d8"), sat((y - wv) / (nh * 1.4)));
    },
  });
  for (let i = 0; i < 7; i++) { // bubbles
    const bx = cx + (hash(i, 5) - 0.5) * nw * 1.7, ph = (f * (0.012 + hash(i, 8) * 0.012) + hash(i, 6)) % 1;
    const by = cy + nh - 2 - ph * Math.max(0, nh * 2 * water - 4);
    if (water > 0.12) put(bx, by, hex("#c8f4ff"), 0.9);
  }
  // face
  const ey = cy - Math.min(2, hh * 0.08), gap = 27, ry = clamp(hh * 0.36, 3.5, 9.5), dk = hex("#1a1038");
  const flat: Mat = { base: dk, flat: true, line: null, rim: 0 };
  for (const sd of [-1, 1]) {
    const ex = cx + sd * gap;
    if (face === "sleep" || face === "blink") {
      paint(ex - 9, ey - 6, ex + 9, ey + 6, arc(ex, ey - 3, 6, 0.4, 2.75, 1), flat);
    } else if (face === "pain") {
      paint(ex - 8, ey - 6, ex + 8, ey + 6, union(capsule(ex - sd * 5, ey - 4, ex + sd * 5, ey, 1), capsule(ex - sd * 5, ey + 4, ex + sd * 5, ey, 1)), flat);
    } else {
      paint(ex - 9, ey - ry - 2, ex + 9, ey + ry + 2, ell(ex, ey, 7, ry), { base: hex("#ffffff"), flat: true, rim: 0 });
      paint(ex - 6, ey - 6, ex + 6, ey + 6, circle(ex + 1, ey + (face === "tired" ? 1 : 0), Math.min(4.4, ry * 0.62)), { ...flat, base: hex("#2a1450") });
      put(ex - 1, ey - 2, hex("#ffffff")); put(ex, ey - 2, hex("#ffffff")); put(ex - 1, ey - 1, hex("#ffffff"));
      if (face === "tired") paint(ex - 8, ey - ry - 1, ex + 8, ey, rbox(ex, ey - ry * 0.65, 7.5, ry * 0.45, 1), { base: hex("#d24a86"), flat: true, line: null, rim: 0 });
    }
  }
  const my = ey + clamp(hh * 0.42, 3, 8);
  if (face === "happy" || face === "awake") paint(cx - 9, my - 5, cx + 9, my + 7, arc(cx, my - 4, 6.5, 0.45, 2.7, 1), flat);
  if (face === "pain") paint(cx - 9, my - 3, cx + 9, my + 3, (x, y) => Math.abs(y - my - Math.sin(x * 1.1) * 1.2) - 0.9 + Math.max(0, Math.abs(x - cx) - 7) * 9, flat);
  if (face === "tired") paint(cx - 6, my - 2, cx + 6, my + 3, capsule(cx - 4, my + 1, cx + 4, my + 1, 0.9), flat);
  if (face === "sleep" || face === "blink") paint(cx - 5, my - 3, cx + 5, my + 4, ell(cx, my + 1, 2.5, 2.5), { ...flat, base: hex("#7a2a4a") });
};

export const droplet = (x: number, y: number, vx: number, vy: number, r: number) => {
  const l = Math.hypot(vx, vy) || 1, tx = x - (vx / l) * r * 2.1, ty = y - (vy / l) * r * 2.1;
  paint(Math.min(x, tx) - r - 2, Math.min(y, ty) - r - 2, Math.max(x, tx) + r + 2, Math.max(y, ty) + r + 2, capsule(x, y, tx, ty, r, 0.6), {
    base: hex("#3cc4ff"), lite: hex("#e0fbff"), dark: hex("#1c48c8"), line: hex("#0f1f7a"), puff: r + 1, rim: 0,
  });
};

// ---------- falling loads ----------
export const books = (cx: number, by: number) => {
  const cols = ["#e8483e", "#ffc94e", "#2fb8a8"], ws = [46, 40, 44];
  for (let i = 0; i < 3; i++) {
    const y = by - 5 - i * 9.4, x = cx + (i === 1 ? 5 : -2);
    paint(x - ws[i] - 2, y - 7, x + ws[i] + 2, y + 7, rbox(x, y, ws[i], 4.8, 1.5), {
      base: hex(cols[i]), puff: 4, tex: (lx) => (lx > x + ws[i] - 7 ? hex("#fff0d8") : Math.abs(lx - x + 26) < 2 ? hex("#fff0d8") : null),
    });
  }
};
export const backpack = (cx: number, by: number) => {
  paint(cx - 44, by - 34, cx + 44, by + 1, rbox(cx, by - 16, 41, 16, 11), { base: hex("#5a5ae8"), lite: hex("#9aa0ff"), dark: hex("#26208a"), puff: 16 });
  for (const sd of [-1, 1]) paint(cx + sd * 27 - 5, by - 33, cx + sd * 27 + 5, by - 1, rbox(cx + sd * 27, by - 17, 3, 15, 2), { base: hex("#26208a"), lite: hex("#4a48c8"), puff: 3, rim: 0 });
  paint(cx - 12, by - 40, cx + 12, by - 28, arc(cx, by - 31, 8, -3.1, -0.04, 1.6), { base: hex("#26208a"), lite: hex("#4a48c8"), puff: 2, rim: 0 });
  paint(cx - 28, by - 22, cx + 28, by, rbox(cx, by - 10, 19, 7, 4), { base: hex("#ffa23e"), lite: hex("#ffd08a"), dark: hex("#c0503e"), puff: 7 });
  rect(cx - 12, by - 11, 24, 1, hex("#7a2a3a"));
};
export const ironBlock = (cx: number, by: number, labels: Label[]) => {
  paint(cx - 60, by - 30, cx + 60, by + 1, rbox(cx, by - 14, 58, 14, 5), { base: hex("#4e5a8a"), lite: hex("#a8b8e0"), dark: hex("#1e1e50"), puff: 10 });
  labels.push({ s: "GRAVITY", x: Math.round(cx - 20), y: Math.round(by - 21), c: "#ffe600" });
};

// ---------- macro backdrop ----------
export const tissue = (night: number, f: number, cy: number) => {
  const top = mix(hex("#2a1566"), hex("#070b30"), night), mid = mix(hex("#6a1f8e"), hex("#16207a"), night), hot = mix(hex("#e0408a"), hex("#3a5ae0"), night);
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const dx = (x - 135) / 170, dy = (y - cy) / 215, r = Math.hypot(dx, dy), a = Math.atan2(dy, dx);
    const wv = Math.sin(r * 26 + Math.sin(a * 3 + f * 0.02) * 1.5 - f * 0.05);
    const c = mix(mix(hot, mid, sat(r * 1.5)), top, sat(r * 1.1 - 0.25));
    put(x, y, scl(c, 1 + (wv > 0.55 ? 0.2 : 0)));
  }
};

// ---------- bed ----------
export const bedScene = (k: Key, f: number, l: number, grow: number, labels: Label[], spine = true) => {
  rug(135, 420, k);
  const breathe = Math.sin(f * 0.1) * 1.4;
  const wood: Mat = { base: hex("#9a5a34"), lite: hex("#dc9a5c"), dark: hex("#4a2430"), puff: 6 };
  for (const x of [34, 240]) paint(x - 6, 372, x + 6, 412, rbox(x, 392, 4, 20, 2), wood);
  paint(16, 248, 44, 392, rbox(30, 320, 12, 72, 8), { ...wood, puff: 12 });
  paint(236, 306, 262, 392, rbox(249, 349, 9, 43, 6), { ...wood, puff: 10 });
  paint(28, 346, 244, 396, rbox(136, 372, 106, 18, 8), { base: hex("#f2e6d8"), lite: hex("#ffffff"), dark: hex("#8a7ab0"), puff: 12 });
  labels.push({ s: "LEARN WITH 8-BIT", x: 88, y: 368, c: "#a596c8", plain: true });
  paint(40, 300, 112, 358, ell(76, 332, 34, 21), { base: hex("#f6f0ff"), lite: hex("#ffffff"), dark: hex("#8f86c8"), puff: 18 });
  push(79, 312, -Math.PI / 2 - 0.08, 0.8, 0.8);
  headArt(0, 0, { eye: "closed", mouth: "sleep" });
  pop();
  // feet slowly poke out as the spine lengthens
  const fx = 226 + grow;
  for (const dy of [-4, 8]) paint(fx - 10, 336 + dy - 9, fx + 12, 336 + dy + 9, ell(fx + 2, 336 + dy, 8, 7), { base: hex("#f7c49a"), lite: hex("#ffe6c8"), dark: hex("#c9765e"), puff: 7 });
  const quilt = blend(10, rbox(165, 340, 64, 20 + breathe * 0.4, 16), ell(146, 330, 44, 24 + breathe));
  paint(92, 296, 236, 366, quilt, {
    base: hex("#c43f88"), lite: hex("#ff86b0"), dark: hex("#4a1a86"), puff: 24,
    tex: (x, y, d, lam) => {
      const a = (Math.floor((x + y) / 14) + Math.floor((x - y + 400) / 14)) % 2 === 0;
      const seam = ((x + y) % 14 < 1) || ((x - y + 400) % 14 < 1);
      if (seam) return mix(hex("#7a2a8e"), hex("#e860a0"), lam);
      return a ? mix(hex("#3a2aa8"), hex("#a23fd0"), lam) : null;
    },
  });
  paint(92, 322, 118, 366, rbox(104, 344, 9, 20, 6), { base: hex("#fff0e0"), dark: hex("#a08ac8"), puff: 7 });
  // glowing spine under the quilt: discs breathe apart as it lengthens
  const n = spine ? 8 : 0;
  for (let i = 0; i < n; i++) {
    const x = 122 + i * (11.5 + grow * 0.14), y = 338, p = 0.5 + 0.5 * Math.sin(f * 0.14 - i * 0.7);
    glow(x, y, 14, hex("#6fd8ff"), 0.3 + 0.2 * p);
    paint(x - 5, y - 7, x + 5, y + 7, rbox(x, y, 2.2, 5.5, 1.5), { base: hex("#c8f6ff"), flat: true, line: hex("#2a4ad8"), rim: 0, alpha: 0.95 });
  }
};

// ---------- space ----------
export const space = (f: number, l: number) => {
  light.tint = [1, 1, 1]; light.rim = hex("#8fd8ff"); light.rimAmt = 0.9; light.dir = [0.45, -0.6, 0.62]; light.rimDir = [-0.75, 0.55];
  for (let y = 0; y < H; y++) {
    const c = mix(hex("#05062a"), hex("#1a1a6e"), Math.pow(y / H, 2));
    for (let x = 0; x < W; x++) {
      const n = fbm(x * 0.012 + 3, y * 0.012 + l * 0.0015);
      put(x, y, mix(c, hex("#6a2aa8"), sat((n - 0.5) * 1.8) * 0.6));
    }
  }
  for (let i = 0; i < 170; i++) {
    const x = hash(i, 1) * W, y = hash(i, 2) * H, tw = 0.45 + 0.55 * Math.sin(f * 0.17 + i);
    put(x, y, hex(i % 5 === 0 ? "#ffe6b0" : "#ffffff"), tw);
    if (i % 23 === 0) star4(x, y, 2, hex("#ffffff"), 0.8 * tw);
  }
  // Earth
  const ex = 92, ey = 690, er = 332, rot = f * 0.0016;
  glow(ex, ey, er + 74, hex("#4fb6ff"), 0.0);
  for (let y = 300; y < H; y++) for (let x = 0; x < W; x++) {
    const dx = x - ex, dy = y - ey, r = Math.hypot(dx, dy);
    if (r > er + 22) continue;
    if (r > er) { addPx(x, y, hex("#5cc8ff"), Math.pow(1 - (r - er) / 22, 2) * 0.85); continue; }
    const nz = Math.sqrt(Math.max(0, 1 - (r / er) ** 2));
    // azimuthal mapping: isotropic continents, no pole, no seam
    const X = dx / er, Y = dy / er, rr = Math.max(1e-4, Math.hypot(X, Y)), ang = Math.asin(Math.min(1, rr)) / rr;
    const u = X * ang * 3.4 + rot * 9, v = Y * ang * 3.4;
    const land = fbm(u * 2.2 + 8, v * 2.2), cloud = fbm(u * 4.5 + 3 - rot * 12, v * 7 + 2);
    let c = land > 0.52 ? mix(hex("#2fa86e"), hex("#d8c078"), sat((land - 0.52) * 5)) : mix(hex("#0c3fb8"), hex("#1f8fe8"), land * 1.4);
    if (cloud > 0.56) c = mix(c, hex("#ffffff"), sat((cloud - 0.56) * 7));
    const lit = sat((dx * 0.55 - dy * 0.75) / er + 0.92);
    c = scl(c, 0.3 + lit * 0.85);
    c = mix(c, hex("#7fd8ff"), Math.pow(1 - nz, 3) * 0.9);
    put(x, y, c);
  }
  // sun on the limb
  glow(252, 300, 150, hex("#ffd9a0"), 0.5); glow(252, 300, 44, hex("#ffffff"), 0.95);
  for (let i = -44; i <= 44; i++) { put(252 + i, 300, hex("#fff2d0"), 0.7 * (1 - Math.abs(i) / 44)); put(252, 300 + i, hex("#fff2d0"), 0.7 * (1 - Math.abs(i) / 44)); }
};

export const astronaut = (cx: number, cy: number, rot: number, sy: number, f: number) => {
  push(cx, cy, rot, 0.86, 0.86 * sy);
  push(0, 90);
  paint(-40, -128, 40, -44, rbox(0, -84, 36, 38, 10), { base: hex("#8a96c8"), lite: hex("#c8d4f0"), dark: hex("#3a3a7a"), puff: 10 });
  const pose: Pose = { armL: 1.05 + Math.sin(f * 0.05) * 0.14, armR: 1.2 - Math.sin(f * 0.05) * 0.14 };
  const b = body(pose, SPACE);
  paint(-30, -124, 30, -108, rbox(0, -116, 25, 6, 3), { base: hex("#ffb14e"), lite: hex("#ffe0a0"), dark: hex("#c0503e"), puff: 4 });
  headArt(0, -146, { eye: "wide", mouth: "grin", lookX: 0.5, lookY: -0.4 });
  paint(-46, -192, 46, -100, circle(0, -146, 42), {
    base: hex("#9fe6ff"), flat: true, alpha: 0.2, line: hex("#e8f4ff"), rim: 0,
  });
  paint(-34, -182, -6, -156, arc(0, -146, 37, -2.6, -2.05, 1.4), { base: hex("#ffffff"), flat: true, line: null, rim: 0, alpha: 0.8 });
  pop(); pop();
};
