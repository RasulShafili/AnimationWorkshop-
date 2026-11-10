// Pixel "shader" engine: everything is shaded in float on a 270x480 art canvas,
// then ordered-dithered. Every frame is a pure function of the frame number.
import fontData from "./font.json";

export const W = 270, H = 480;
export type RGB = [number, number, number];
export type SDF = (x: number, y: number) => number;

export const clamp = (v: number, a: number, b: number) => (v < a ? a : v > b ? b : v);
export const sat = (v: number) => clamp(v, 0, 1);
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const sstep = (a: number, b: number, x: number) => {
  const t = sat((x - a) / (b - a));
  return t * t * (3 - 2 * t);
};
export const easeOut = (t: number) => 1 - Math.pow(1 - sat(t), 3);
export const easeIn = (t: number) => Math.pow(sat(t), 3);
export const easeInOut = (t: number) => { t = sat(t); return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
export const backOut = (t: number) => { t = sat(t); const c = 1.9; return 1 + (c + 1) * Math.pow(t - 1, 3) + c * Math.pow(t - 1, 2); };

const hexCache = new Map<string, RGB>();
export const hex = (s: string): RGB => {
  let c = hexCache.get(s);
  if (!c) {
    const n = parseInt(s.slice(1), 16);
    c = [(n >> 16 & 255) / 255, (n >> 8 & 255) / 255, (n & 255) / 255];
    hexCache.set(s, c);
  }
  return c;
};
export const mix = (a: RGB, b: RGB, t: number): RGB => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];
export const mul = (a: RGB, b: RGB): RGB => [a[0] * b[0], a[1] * b[1], a[2] * b[2]];
export const scl = (a: RGB, k: number): RGB => [a[0] * k, a[1] * k, a[2] * k];

// deterministic hash + value noise
export const hash = (x: number, y = 0): number => {
  let h = (Math.imul(x | 0, 374761393) + Math.imul(y | 0, 668265263)) | 0;
  h = Math.imul(h ^ (h >>> 13), 1274126177);
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
};
export const noise = (x: number, y: number): number => {
  const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi;
  const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
  return lerp(lerp(hash(xi, yi), hash(xi + 1, yi), u), lerp(hash(xi, yi + 1), hash(xi + 1, yi + 1), u), v);
};
export const fbm = (x: number, y: number) => noise(x, y) * 0.55 + noise(x * 2.1, y * 2.1) * 0.3 + noise(x * 4.3, y * 4.3) * 0.15;

// ---- frame buffers ----
export const makeFB = () => new Float32Array(W * H * 3);
let T: Float32Array = makeFB();
export const target = (fb: Float32Array) => { T = fb; };

export const put = (x: number, y: number, c: RGB, a = 1) => {
  if (x < 0 || y < 0 || x >= W || y >= H) return;
  const i = ((y | 0) * W + (x | 0)) * 3;
  T[i] += (c[0] - T[i]) * a; T[i + 1] += (c[1] - T[i + 1]) * a; T[i + 2] += (c[2] - T[i + 2]) * a;
};
export const addPx = (x: number, y: number, c: RGB, a: number) => {
  if (x < 0 || y < 0 || x >= W || y >= H) return;
  const i = ((y | 0) * W + (x | 0)) * 3;
  T[i] += c[0] * a; T[i + 1] += c[1] * a; T[i + 2] += c[2] * a;
};
export const rect = (x: number, y: number, w: number, h: number, c: RGB, a = 1) => {
  const x0 = Math.max(0, Math.round(x)), y0 = Math.max(0, Math.round(y));
  const x1 = Math.min(W, Math.round(x + w)), y1 = Math.min(H, Math.round(y + h));
  for (let j = y0; j < y1; j++) for (let i = x0; i < x1; i++) put(i, j, c, a);
};
export const vgrad = (y0: number, y1: number, stops: RGB[]) => {
  for (let y = Math.max(0, y0 | 0); y < Math.min(H, y1); y++) {
    const t = ((y - y0) / (y1 - y0)) * (stops.length - 1);
    const k = Math.min(stops.length - 2, Math.floor(t));
    const c = mix(stops[k], stops[k + 1], t - k);
    for (let x = 0; x < W; x++) put(x, y, c);
  }
};
export const glow = (cx: number, cy: number, r: number, c: RGB, a: number, sy = 1) => {
  const x0 = Math.floor(cx - r), x1 = Math.ceil(cx + r), y0 = Math.floor(cy - r * sy), y1 = Math.ceil(cy + r * sy);
  for (let y = Math.max(0, y0); y < Math.min(H, y1); y++) for (let x = Math.max(0, x0); x < Math.min(W, x1); x++) {
    const dx = (x - cx) / r, dy = (y - cy) / (r * sy), d = 1 - Math.sqrt(dx * dx + dy * dy);
    if (d > 0) addPx(x, y, c, a * d * d);
  }
};
export const darken = (y0: number, y1: number, c: RGB, a0: number, a1: number) => {
  for (let y = Math.max(0, y0 | 0); y < Math.min(H, y1); y++) {
    const a = lerp(a0, a1, (y - y0) / (y1 - y0));
    for (let x = 0; x < W; x++) put(x, y, c, a);
  }
};

// ---- SDF library ----
export const circle = (cx: number, cy: number, r: number): SDF => (x, y) => Math.hypot(x - cx, y - cy) - r;
export const ell = (cx: number, cy: number, rx: number, ry: number): SDF => (x, y) => {
  const px = (x - cx) / rx, py = (y - cy) / ry;
  return (Math.hypot(px, py) - 1) * Math.min(rx, ry);
};
export const rbox = (cx: number, cy: number, hw: number, hh: number, r: number): SDF => (x, y) => {
  const qx = Math.abs(x - cx) - hw + r, qy = Math.abs(y - cy) - hh + r;
  return Math.hypot(Math.max(qx, 0), Math.max(qy, 0)) + Math.min(Math.max(qx, qy), 0) - r;
};
export const capsule = (ax: number, ay: number, bx: number, by: number, r: number, r2 = r): SDF => (x, y) => {
  const pax = x - ax, pay = y - ay, bax = bx - ax, bay = by - ay;
  const h = sat((pax * bax + pay * bay) / (bax * bax + bay * bay || 1));
  return Math.hypot(pax - bax * h, pay - bay * h) - lerp(r, r2, h);
};
export const smin = (a: number, b: number, k: number) => {
  const h = sat(0.5 + (0.5 * (b - a)) / k);
  return lerp(b, a, h) - k * h * (1 - h);
};
export const union = (...s: SDF[]): SDF => (x, y) => { let d = 1e9; for (const f of s) d = Math.min(d, f(x, y)); return d; };
export const blend = (k: number, ...s: SDF[]): SDF => (x, y) => { let d = s[0](x, y); for (let i = 1; i < s.length; i++) d = smin(d, s[i](x, y), k); return d; };
export const minus = (a: SDF, b: SDF): SDF => (x, y) => Math.max(a(x, y), -b(x, y));

// ---- transforms (local -> world) ----
type Xf = { a: number; b: number; c: number; d: number; e: number; f: number };
let xf: Xf = { a: 1, b: 0, c: 0, d: 1, e: 0, f: 0 };
const stack: Xf[] = [];
export const push = (tx: number, ty: number, rot = 0, sx = 1, sy = 1) => {
  stack.push(xf);
  const co = Math.cos(rot), si = Math.sin(rot);
  const m = { a: co * sx, b: si * sx, c: -si * sy, d: co * sy, e: tx, f: ty };
  xf = { a: xf.a * m.a + xf.c * m.b, b: xf.b * m.a + xf.d * m.b, c: xf.a * m.c + xf.c * m.d, d: xf.b * m.c + xf.d * m.d,
    e: xf.a * m.e + xf.c * m.f + xf.e, f: xf.b * m.e + xf.d * m.f + xf.f };
};
export const pop = () => { xf = stack.pop()!; };
export const toWorld = (x: number, y: number): [number, number] => [xf.a * x + xf.c * y + xf.e, xf.b * x + xf.d * y + xf.f];

// ---- scene lighting ----
export const light = {
  dir: [-0.5, -0.62, 0.6] as [number, number, number],
  rimDir: [0.8, -0.45] as [number, number],
  rim: hex("#ffc36b") as RGB,
  rimAmt: 0.85,
  tint: [1, 1, 1] as RGB,
};

export type Mat = {
  base: RGB; lite?: RGB; dark?: RGB;
  line?: RGB | null; puff?: number; rim?: number; alpha?: number;
  tex?: (lx: number, ly: number, d: number, lam: number) => RGB | null;
  flat?: boolean;
};
export const defaultDark = (c: RGB): RGB => [c[0] * 0.48 + 0.03, c[1] * 0.42 + 0.01, c[2] * 0.58 + 0.08];
export const defaultLite = (c: RGB): RGB => [Math.min(1, c[0] * 1.14 + 0.1), Math.min(1, c[1] * 1.12 + 0.08), Math.min(1, c[2] * 1.08 + 0.05)];

// Fill an SDF with dome-shaded volume, outline and rim light.
export const paint = (bx0: number, by0: number, bx1: number, by1: number, sdf: SDF, m: Mat) => {
  const det = xf.a * xf.d - xf.b * xf.c;
  const ia = xf.d / det, ib = -xf.b / det, ic = -xf.c / det, id = xf.a / det;
  const lx = (X: number, Y: number) => ia * (X - xf.e) + ic * (Y - xf.f);
  const ly = (X: number, Y: number) => ib * (X - xf.e) + id * (Y - xf.f);
  const cs = [toWorld(bx0, by0), toWorld(bx1, by0), toWorld(bx0, by1), toWorld(bx1, by1)];
  const x0 = Math.max(0, Math.floor(Math.min(...cs.map(c => c[0]))) - 1), x1 = Math.min(W - 1, Math.ceil(Math.max(...cs.map(c => c[0]))) + 1);
  const y0 = Math.max(0, Math.floor(Math.min(...cs.map(c => c[1]))) - 1), y1 = Math.min(H - 1, Math.ceil(Math.max(...cs.map(c => c[1]))) + 1);
  const dark = m.dark ?? defaultDark(m.base), lite = m.lite ?? defaultLite(m.base);
  const puff = m.puff ?? 12, alpha = m.alpha ?? 1, rimK = (m.rim ?? 1) * light.rimAmt;
  const line = m.line === undefined ? hex("#1a1038") : m.line;
  const L = light.dir, R = light.rimDir;
  for (let Y = y0; Y <= y1; Y++) for (let X = x0; X <= x1; X++) {
    const px = X + 0.5, py = Y + 0.5, ux = lx(px, py), uy = ly(px, py);
    const d = sdf(ux, uy);
    if (d > 0) continue;
    let c: RGB;
    if (line && d > -1) { c = mul(line, light.tint); put(X, Y, c, alpha); continue; }
    const gx = sdf(lx(px + 1, py), ly(px + 1, py)) - sdf(lx(px - 1, py), ly(px - 1, py));
    const gy = sdf(lx(px, py + 1), ly(px, py + 1)) - sdf(lx(px, py - 1), ly(px, py - 1));
    const gl = Math.hypot(gx, gy) || 1;
    const k = 1 - sat(-d / puff), nx = (gx / gl) * k, ny = (gy / gl) * k, nz = Math.sqrt(Math.max(0, 1 - k * k));
    const lam = sat(nx * L[0] + ny * L[1] + nz * L[2]);
    if (m.flat) c = m.base;
    else c = lam < 0.55 ? mix(dark, m.base, lam / 0.55) : mix(m.base, lite, (lam - 0.55) / 0.45);
    if (m.tex) { const t = m.tex(ux, uy, d, lam); if (t) c = t; }
    c = mul(c, light.tint);
    if (rimK > 0 && d > -3.2) {
      const r = sat((gx / gl) * R[0] + (gy / gl) * R[1]);
      if (r > 0.35) c = mix(c, light.rim, rimK * sat((r - 0.35) * 2.4));
    }
    put(X, Y, c, alpha);
  }
};

// ---- output: ordered dither ----
const B8 = [0, 32, 8, 40, 2, 34, 10, 42, 48, 16, 56, 24, 50, 18, 58, 26, 12, 44, 4, 36, 14, 46, 6, 38, 60, 28, 52, 20, 62, 30, 54, 22,
  3, 35, 11, 43, 1, 33, 9, 41, 51, 19, 59, 27, 49, 17, 57, 25, 15, 47, 7, 39, 13, 45, 5, 37, 63, 31, 55, 23, 61, 29, 53, 21];
export const bayer = (x: number, y: number) => (B8[(y & 7) * 8 + (x & 7)] + 0.5) / 64;

export const quantize = (src: Float32Array, out: Uint8ClampedArray, levels = 11, strength = 0.85) => {
  const q = levels - 1;
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const i = (y * W + x) * 3, o = (y * W + x) * 4, b = (bayer(x, y) - 0.5) * strength;
    for (let k = 0; k < 3; k++) {
      const v = Math.round(sat(src[i + k]) * q + b) / q;
      out[o + k] = sat(v) * 255;
    }
    out[o + 3] = 255;
  }
};

// ---- text (drawn after dithering so it stays razor sharp) ----
type Glyphs = { h: number; g: Record<string, { w: number; p: number[][] }> };
const FONT = fontData as unknown as Record<string, Glyphs>;
const px = (o: Uint8ClampedArray, x: number, y: number, c: RGB) => {
  if (x < 0 || y < 0 || x >= W || y >= H) return;
  const i = (y * W + x) * 4; o[i] = c[0] * 255; o[i + 1] = c[1] * 255; o[i + 2] = c[2] * 255;
};
const ADV: Record<number, number> = { 16: 6, 24: 9, 32: 13 };
const CELL: Record<number, number> = { 16: 5, 24: 8, 32: 11 };
export const textWidth = (s: string, size = 24) => s.length * ADV[size] - (ADV[size] - CELL[size]);
const OUT = hex("#120a2e");
export const glyphRun = (o: Uint8ClampedArray, s: string, x: number, y: number, c: RGB, size = 16, shadow = true) => {
  const f = FONT[size], adv = ADV[size], cellW = CELL[size];
  const plot = (fn: (X: number, Y: number) => void) => {
    let cx = x;
    for (const ch of s) {
      const g = f.g[ch];
      if (g) { const off = Math.floor((cellW - g.w) / 2); for (const p of g.p) fn(cx + off + p[0], y + p[1]); }
      cx += adv;
    }
  };
  if (shadow) plot((X, Y) => { // pixel outline + drop shadow
    for (let dy = -1; dy <= 2; dy++) for (let dx = -1; dx <= 1; dx++) px(o, X + dx, Y + dy, OUT);
  });
  plot((X, Y) => px(o, X, Y, c));
};

export type Seg = { t: string; c?: string };
export type Line = { segs: Seg[]; big?: boolean };
// Centered text block with typewriter reveal; `chars` = characters visible.
export const textBlock = (o: Uint8ClampedArray, lines: Line[], topY: number, chars: number, cx = 135) => {
  let y = topY, n = 0;
  for (const l of lines) {
    const size = l.big ? 32 : 24, adv = ADV[size];
    const full = l.segs.map(s => s.t).join("");
    let x = Math.round(cx - textWidth(full, size) / 2);
    for (const s of l.segs) {
      const vis = Math.max(0, Math.min(s.t.length, Math.floor(chars - n)));
      if (vis > 0) glyphRun(o, s.t.slice(0, vis), x, y, hex(s.c ?? "#ffffff"), size);
      n += s.t.length; x += s.t.length * adv;
    }
    y += l.big ? 26 : 19;
  }
};
