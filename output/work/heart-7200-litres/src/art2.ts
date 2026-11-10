import { W, H, RGB, SDF, Mat, hex, mix, sat, clamp, lerp, sstep, hash, noise, fbm, put, addPx, rect, glow, paint, push, pop,
  circle, ell, rbox, capsule, union, minus, light, easeOut } from "./gfx";
import { heroSil, Pose, headArt, Face, sparkle, Label, arc } from "./art";

// photon-count colour map: black -> violet -> red -> amber -> cream
const HEAT = ["#05030f", "#2a0a5e", "#8a1a8a", "#ff4a3a", "#ffb23a", "#fff6c0"].map(hex);
export const heat = (v: number): RGB => {
  v = sat(v) * (HEAT.length - 1);
  const i = Math.min(HEAT.length - 2, Math.floor(v));
  return mix(HEAT[i], HEAT[i + 1], v - i);
};

// soft light hugging the hero's silhouette
export const aura = (cx: number, feet: number, sy: number, pose: Pose, col: RGB, a: number, r = 22) => {
  const s = heroSil(pose);
  for (let y = Math.max(0, Math.floor(feet - 200 * sy - r)); y < Math.min(H, feet + r); y++)
    for (let x = Math.max(0, Math.floor(cx - 80 - r)); x < Math.min(W, cx + 80 + r); x++) {
      const d = s(x + 0.5 - cx, (y + 0.5 - feet) / sy);
      if (d > r) continue;
      const t = d < 0 ? 0.3 : 1 - d / r;
      addPx(x, y, col, a * t * t);
    }
};

// little photons drifting up and away
export const photons = (cx: number, cy: number, w: number, h: number, f: number, n: number, col: RGB, a = 1) => {
  for (let i = 0; i < n; i++) {
    const ph = (f * (0.006 + hash(i, 21) * 0.008) + hash(i, 22)) % 1;
    const x = cx + (hash(i, 23) - 0.5) * w + Math.sin(f * 0.05 + i * 1.7) * 5, y = cy - ph * h;
    const al = Math.sin(Math.PI * ph) * a;
    glow(x, y, 7, col, 0.35 * al);
    sparkle(x, y, i % 3 === 0 ? 2 : 1, mix(col, hex("#ffffff"), 0.6), al);
  }
};

// ---------- the eye ----------
export const eyeChar = (cx: number, cy: number, r: number, open: number, lookX: number, lookY: number, pupil: number, f: number) => {
  paint(cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3, circle(cx, cy, r), {
    base: hex("#f4f0ff"), lite: hex("#ffffff"), dark: hex("#9a8ad0"), puff: r, rim: 0.6,
    tex: (x, y, d) => {
      if (d > -9 && d < -2) {
        const a = Math.atan2(y - cy, x - cx), v = Math.sin(a * 7 + Math.sin(d * 0.9) * 1.5);
        if (Math.abs(v) < 0.07) return hex("#ff8aa8");
      }
      return null;
    },
  });
  const ix = cx + lookX * r * 0.28, iy = cy + lookY * r * 0.28, ir = r * 0.47;
  paint(ix - ir - 2, iy - ir - 2, ix + ir + 2, iy + ir + 2, circle(ix, iy, ir), {
    base: hex("#25b8d8"), lite: hex("#8af4ff"), dark: hex("#0a4a8a"), puff: ir * 0.8, rim: 0,
    tex: (x, y, d) => {
      const a = Math.atan2(y - iy, x - ix), rr = Math.hypot(x - ix, y - iy) / ir;
      if (Math.sin(a * 22) > 0.55 && rr > 0.45) return mix(hex("#1a7ab0"), hex("#5ce1e6"), rr);
      if (rr > 0.86) return hex("#0a2a6a");
      return null;
    },
  });
  const pr = ir * 0.48 * pupil;
  paint(ix - pr - 2, iy - pr - 2, ix + pr + 2, iy + pr + 2, circle(ix, iy, pr), { base: hex("#08061a"), flat: true, line: null, rim: 0 });
  paint(ix - ir, iy - ir, ix, iy, circle(ix - ir * 0.32, iy - ir * 0.36, ir * 0.2), { base: hex("#ffffff"), flat: true, line: null, rim: 0 });
  put(ix + ir * 0.3, iy + ir * 0.25, hex("#ffffff")); put(ix + ir * 0.3 + 1, iy + ir * 0.25, hex("#ffffff"));
  // lids squint down from top and up from bottom
  const lid: Mat = { base: hex("#b46aa8"), lite: hex("#e8a0d0"), dark: hex("#5a2a7a"), puff: 10, rim: 0.4 };
  const top = cy - r + (1 - open) * r * 1.05, bot = cy + r - (1 - open) * r * 0.8;
  paint(cx - r - 4, cy - r - 4, cx + r + 4, top + 3, (x, y) => Math.max(circle(cx, cy, r + 2)(x, y), y - top - Math.sin((x - cx) / r * 1.5) * 0), lid);
  paint(cx - r - 4, bot - 3, cx + r + 4, cy + r + 4, (x, y) => Math.max(circle(cx, cy, r + 2)(x, y), bot - y), lid);
  rect(cx - Math.sqrt(Math.max(0, r * r - (top - cy) ** 2)), Math.round(top), 2 * Math.sqrt(Math.max(0, r * r - (top - cy) ** 2)), 2, hex("#1a1038"));
  for (let i = 0; i < 6; i++) { // lashes
    const lx = cx - r * 0.7 + i * r * 0.28, ly = top;
    if (Math.abs(lx - cx) < Math.sqrt(Math.max(0, r * r - (ly - cy) ** 2)))
      paint(lx - 4, ly - 9, lx + 4, ly + 1, capsule(lx, ly, lx + (i - 2.5) * 1.2, ly - 6, 1), { base: hex("#1a1038"), flat: true, line: null, rim: 0 });
  }
  // brows
  const br = 3 + (1 - open) * 5;
  for (const s of [-1, 1]) paint(cx + s * r * 0.55 - 20, top - 26, cx + s * r * 0.55 + 20, top - 4,
    capsule(cx + s * r * 0.2, top - 10 - br * 0.3, cx + s * r * 0.85, top - 14 + br * 0.4, 3), { base: hex("#4a2a6a"), puff: 3, rim: 0 });
};

// vertical light-level gauge: brighter things higher up
export const gauge = (x: number, top: number, bot: number, f: number, labels: Label[]) => {
  for (let y = top; y < bot; y++) {
    const t = (y - top) / (bot - top), c = mix(hex("#fff3a0"), hex("#0a0820"), Math.pow(t, 0.7));
    for (let i = 0; i < 9; i++) put(x + i, y, c);
  }
  rect(x - 1, top - 1, 11, 1, hex("#c9a860")); rect(x - 1, bot, 11, 1, hex("#c9a860"));
  rect(x - 1, top, 1, bot - top, hex("#c9a860")); rect(x + 9, top, 1, bot - top, hex("#c9a860"));
  const mark = (y: number, s: string, c: string, dashed = false) => {
    for (let i = 0; i < (dashed ? 150 : 14); i++) if (!dashed || i % 4 < 2) put(x + 10 + i, y, hex(c));
    labels.push({ s, x: x + 14, y: y - 12, c });
  };
  mark(top + 18, "CANDLE", "#ffd86b");
  mark(top + 92, "EYE LIMIT", "#5ce1e6", true);
  const yy = bot - 14, bl = 0.5 + 0.5 * Math.sin(f * 0.3);
  glow(x + 4, yy, 10, hex("#55efc4"), 0.6 * bl);
  mark(yy, "YOU", "#55efc4");
};

// ---------- photon camera ----------
// brightness of the person the camera sees: face hottest, cheeks hotter still
export const bodyField = (cx: number, feet: number, pose: Pose) => {
  const s = heroSil(pose), hx = cx, hy = feet - 146;
  return (x: number, y: number) => {
    const d = s(x - cx, y - feet);
    if (d > 3) return 0;
    let v = 0.32 + 0.12 * fbm(x * 0.1, y * 0.1);
    const fd = Math.hypot((x - hx) / 34, (y - hy) / 32);
    if (fd < 1) v += 0.45 * (1 - fd * fd);
    for (const sx of [-1, 1]) v += 0.35 * Math.exp(-(((x - hx - sx * 20) ** 2) + ((y - hy - 10) ** 2)) / 70);
    return v * (d > 0 ? 1 - d / 3 : 1);
  };
};

export const viewfinder = (f: number, count: number, labels: Label[]) => {
  const c = hex("#e8f4ff"), x0 = 20, x1 = 250, y0 = 146, y1 = 420, L = 18;
  for (const [x, y, sx, sy] of [[x0, y0, 1, 1], [x1, y0, -1, 1], [x0, y1, 1, -1], [x1, y1, -1, -1]] as const) {
    rect(sx > 0 ? x : x - L, y, L, 2, c); rect(sx > 0 ? x : x - 1, sy > 0 ? y : y - L, 2, L, c);
  }
  if (Math.floor(f / 15) % 2 === 0) { glow(32, 160, 8, hex("#ff3a3a"), 0.8); rect(29, 157, 6, 6, hex("#ff4a4a")); }
  labels.push({ s: "REC", x: 40, y: 153, c: "#ff6a6a" });
  labels.push({ s: "1 PHOTON CAM", x: 168, y: 153, c: "#a8c8ff", plain: true });
  labels.push({ s: "PHOTONS " + String(count).padStart(6, "0"), x: 30, y: 400, c: "#ffe600" });
  // crosshair
  rect(131, 282, 9, 1, c, 0.6); rect(135, 278, 1, 9, c, 0.6);
};

// ---------- the cell ----------
export const cellBg = (f: number, warm = 0) => {
  const a = mix(hex("#0b5a7a"), hex("#6a2a1a"), warm), b = mix(hex("#04122e"), hex("#1a0820"), warm);
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const r = Math.hypot((x - 135) / 200, (y - 300) / 260);
    const n = fbm(x * 0.02 + f * 0.003, y * 0.02 - f * 0.002);
    put(x, y, mix(mix(a, b, sat(r * 1.3)), mix(a, hex("#5ae0d0"), 0.4), sat((n - 0.55) * 2) * 0.5));
  }
  for (let i = 0; i < 16; i++) { // drifting vesicles
    const x = (hash(i, 31) * 300 + f * (0.1 + hash(i, 32) * 0.2)) % 300 - 15, y = hash(i, 33) * H, r = 3 + hash(i, 34) * 6;
    paint(x - r - 2, y - r - 2, x + r + 2, y + r + 2, circle(x, y, r), { base: mix(a, hex("#8af0e0"), 0.4), line: null, puff: r, rim: 0, alpha: 0.5 });
  }
};

export const bean = (cx: number, cy: number, len: number, wid: number, rot: number, f: number, glowA: number) => {
  push(cx, cy, rot);
  paint(-len - wid - 2, -wid - 2, len + wid + 2, wid + 2, capsule(-len, 0, len, 0, wid), {
    base: hex("#ff8a3a"), lite: hex("#ffd08a"), dark: hex("#a8303a"), puff: wid * 0.9,
    tex: (x, y, d) => {
      if (d < -2.5) {
        const fold = Math.abs(((x + 400) % 9) - 4.5 + Math.sin(y * 0.6) * 1.2);
        if (fold < 1.1 && Math.abs(y) < wid - 3) return hex("#e05a3a");
      }
      return null;
    },
  });
  pop();
  if (glowA > 0) glow(cx, cy, len * 2.4, hex("#ffb84a"), glowA);
};

export const cellChar = (cx: number, cy: number, r: number, f: number, labels: Label[]) => {
  glow(cx, cy, r * 1.6, hex("#5affd8"), 0.25);
  paint(cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2, circle(cx, cy, r - 4), { base: hex("#7ae8d8"), flat: true, line: null, rim: 0, alpha: 0.28 });
  paint(cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3, minus(circle(cx, cy, r), circle(cx, cy, r - 6)), {
    base: hex("#3ad0b8"), lite: hex("#b8fff0"), dark: hex("#0a5a6a"), puff: 4, rim: 0.7,
  });
  // mitochondria orbiting, each one pulsing with light
  for (let i = 0; i < 5; i++) {
    const a = i * 1.2566 + f * 0.008, rr = r * (0.6 + 0.08 * Math.sin(i * 2.1));
    const p = 0.5 + 0.5 * Math.sin(f * 0.25 + i * 1.9);
    bean(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr * 0.92, 13, 7.5, a + 1.3, f, 0.12 + 0.18 * p);
    if (p > 0.92) sparkle(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr * 0.92 - 12, 2, hex("#fff6c0"), 1);
  }
  // nucleus with a face
  const nx = cx - 6, ny = cy + 4;
  paint(nx - 38, ny - 34, nx + 38, ny + 34, ell(nx, ny, 34, 30), { base: hex("#8a5ae8"), lite: hex("#c8a8ff"), dark: hex("#3a1a8a"), puff: 26 });
  const dk = hex("#1a1038"), blink = (f + 20) % 90 < 4;
  for (const s of [-1, 1]) {
    const ex = nx + s * 12, ey = ny - 3;
    if (blink) { paint(ex - 7, ey - 5, ex + 7, ey + 5, arc(ex, ey - 3, 5, 0.4, 2.75, 1), { base: dk, flat: true, line: null, rim: 0 }); continue; }
    paint(ex - 7, ey - 9, ex + 7, ey + 9, ell(ex, ey, 5.5, 7), { base: hex("#ffffff"), flat: true, rim: 0 });
    paint(ex - 5, ey - 5, ex + 5, ey + 5, circle(ex + 1, ey + 1, 3.6), { base: hex("#2a1450"), flat: true, line: null, rim: 0 });
    put(ex, ey - 1, hex("#ffffff"));
  }
  paint(nx - 8, ny + 6, nx + 8, ny + 16, arc(nx, ny + 6, 5.5, 0.45, 2.7, 1), { base: dk, flat: true, line: null, rim: 0 });
  for (const s of [-1, 1]) for (let j = -2; j <= 2; j++) for (let i = -4; i <= 4; i++) put(nx + s * 21 + i, ny + 8 + j, hex("#ff7fb8"), 0.25);
};

// ---------- inside a mitochondrion ----------
export const radical = (x: number, y: number, f: number, mad: boolean) => {
  const s: SDF = (px, py) => { const a = Math.atan2(py - y, px - x); return Math.hypot(px - x, py - y) - (10 + 3.5 * Math.max(0, Math.sin(a * 8 + f * 0.2))); };
  glow(x, y, 22, hex("#ff3a6a"), 0.3);
  paint(x - 16, y - 16, x + 16, y + 16, s, { base: hex("#ff3a5a"), lite: hex("#ff9aa8"), dark: hex("#7a0a3a"), puff: 9 });
  const dk = hex("#1a1038");
  for (const sd of [-1, 1]) {
    paint(x + sd * 4 - 4, y - 4, x + sd * 4 + 4, y + 4, circle(x + sd * 4, y, 2.6), { base: hex("#ffffff"), flat: true, line: dk, rim: 0 });
    put(x + sd * 4, y, dk);
    paint(x + sd * 4 - 5, y - 9, x + sd * 4 + 5, y - 3, capsule(x + sd * 1.5, y - (mad ? 4 : 6), x + sd * 7, y - (mad ? 7 : 6), 0.9), { base: dk, flat: true, line: null, rim: 0 });
  }
  paint(x - 4, y + 2, x + 4, y + 7, mad ? capsule(x - 3, y + 5, x + 3, y + 5, 0.9) : arc(x, y + 1, 3, 0.4, 2.7, 0.9), { base: dk, flat: true, line: null, rim: 0 });
};

export const fatChain = (x: number, y: number, f: number, hitT: number) => {
  for (let i = 0; i < 5; i++) {
    const bx = x - 16 + i * 8, by = y + Math.sin(f * 0.12 + i * 0.9) * 2;
    const hot = hitT >= 0 && hitT < 10 ? 1 - hitT / 10 : 0;
    paint(bx - 6, by - 6, bx + 6, by + 6, circle(bx, by, 4.6), { base: mix(hex("#ffd84e"), hex("#ffffff"), hot), lite: hex("#fff6c0"), dark: hex("#c0702a"), puff: 4 });
  }
};

export const mitoBig = (cx: number, cy: number, f: number) => {
  glow(cx, cy, 190, hex("#ff8a3a"), 0.25);
  paint(cx - 130, cy - 70, cx + 130, cy + 70, capsule(cx - 72, cy, cx + 72, cy, 62), {
    base: hex("#ff7a3a"), lite: hex("#ffc08a"), dark: hex("#8a203a"), puff: 30,
    tex: (x, y, d, lam) => {
      if (d > -7) return null;
      // matrix + cristae folds
      const fold = Math.abs(((x - cx + 400) % 30) - 15 + Math.sin((y - cy) * 0.09 + x * 0.02) * 6);
      if (d < -11 && Math.abs(y - cy) < 46 && fold < 3.2) return mix(hex("#c8402a"), hex("#ff8a4a"), lam);
      if (d < -7 && d > -10) return hex("#d84a3a");
      return mix(hex("#ffb06a"), hex("#ff8a4a"), 1 - lam) as RGB;
    },
  });
};

// ---------- clock ----------
export const clock = (cx: number, cy: number, r: number, hours: number) => {
  paint(cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6, circle(cx, cy, r + 4), { base: hex("#c9974e"), lite: hex("#ffd890"), dark: hex("#6a3a2a"), puff: 6 });
  paint(cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2, circle(cx, cy, r), { base: hex("#fff6e0"), lite: hex("#ffffff"), dark: hex("#c8b8d0"), puff: r, rim: 0 });
  for (let i = 0; i < 12; i++) {
    const a = (i / 12) * Math.PI * 2, big = i % 3 === 0;
    const x0 = cx + Math.sin(a) * (r - (big ? 10 : 6)), y0 = cy - Math.cos(a) * (r - (big ? 10 : 6));
    const x1 = cx + Math.sin(a) * (r - 3), y1 = cy - Math.cos(a) * (r - 3);
    paint(Math.min(x0, x1) - 3, Math.min(y0, y1) - 3, Math.max(x0, x1) + 3, Math.max(y0, y1) + 3, capsule(x0, y0, x1, y1, big ? 1.6 : 0.8), { base: hex("#3a2a5a"), flat: true, line: null, rim: 0 });
  }
  const hand = (a: number, l: number, w: number, c: string) => {
    const x1 = cx + Math.sin(a) * l, y1 = cy - Math.cos(a) * l;
    paint(Math.min(cx, x1) - w - 2, Math.min(cy, y1) - w - 2, Math.max(cx, x1) + w + 2, Math.max(cy, y1) + w + 2, capsule(cx, cy, x1, y1, w, w * 0.6), { base: hex(c), flat: true, line: null, rim: 0 });
  };
  hand(((hours % 12) / 12) * Math.PI * 2, r * 0.5, 2.6, "#2a1a4a");
  hand((hours % 1) * Math.PI * 2, r * 0.78, 1.6, "#2a1a4a");
  paint(cx - 4, cy - 4, cx + 4, cy + 4, circle(cx, cy, 2.6), { base: hex("#ff4a6a"), flat: true, line: null, rim: 0 });
};

// ---------- fireflies ----------
export const firefly = (x: number, y: number, f: number, i: number) => {
  const on = 0.55 + 0.45 * Math.sin(f * 0.21 + i * 2.3);
  glow(x, y, 16, hex("#d8ff6a"), 0.55 * on);
  glow(x, y, 5, hex("#ffffc0"), 0.9 * on);
  const flap = Math.sin(f * 1.3 + i) > 0 ? 1 : 0;
  put(x - 2, y - 2 - flap, hex("#e8f0ff"), 0.8); put(x + 2, y - 2 - flap, hex("#e8f0ff"), 0.8);
  put(x, y, hex("#fffff0")); put(x + 1, y, hex("#2a2a3a"));
};
