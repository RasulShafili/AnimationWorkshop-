import { W, H, RGB, SDF, Mat, hex, mix, sat, clamp, lerp, sstep, hash, noise, fbm, put, addPx, rect, glow, paint, push, pop,
  circle, ell, rbox, capsule, blend, union, minus, light, toWorld } from "./gfx";
import { arc, sparkle, Label } from "./art";

// a little tree: the classic optics test object
export const tree = (cx: number, by: number, s: number, alpha = 1) => {
  push(cx, by, 0, s, s);
  paint(-6, -34, 6, 2, rbox(0, -16, 3.5, 17, 1.5), { base: hex("#9a5a34"), lite: hex("#dc9a5c"), dark: hex("#4a2430"), puff: 3, alpha });
  paint(-24, -66, 24, -22, union(circle(0, -48, 16), circle(-11, -38, 11), circle(11, -38, 11)), { base: hex("#2fae5a"), lite: hex("#9ae88a"), dark: hex("#0f5a50"), puff: 12, alpha });
  paint(-10, -62, 10, -44, circle(5, -50, 3), { base: hex("#ff4a5a"), puff: 2, alpha, rim: 0 });
  pop();
};

const line = (x0: number, y0: number, x1: number, y1: number, c: RGB, a = 1, upto = 1) => {
  const n = Math.ceil(Math.hypot(x1 - x0, y1 - y0) * upto);
  const L = Math.hypot(x1 - x0, y1 - y0) || 1;
  for (let i = 0; i <= n; i++) {
    const t = i / L, x = x0 + (x1 - x0) * t, y = y0 + (y1 - y0) * t;
    put(x, y, c, a); addPx(x, y - 1, c, 0.25 * a); addPx(x, y + 1, c, 0.25 * a);
  }
};

// side view of the eye with light rays crossing in the lens
export const eyeSection = (cx: number, cy: number, r: number, rays: number, f: number) => {
  glow(cx, cy, r * 2, hex("#3a6aff"), 0.15);
  paint(cx + r - 8, cy - 10, cx + r + 40, cy + 14, capsule(cx + r - 4, cy + 2, cx + r + 40, cy + 6, 7, 5), { base: hex("#ffd84e"), lite: hex("#fff2a0"), dark: hex("#c0702a"), puff: 5 });
  paint(cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3, circle(cx, cy, r), {
    base: hex("#f4f0ff"), lite: hex("#ffffff"), dark: hex("#8a7ac8"), puff: 20,
    tex: (x, y, d) => {
      const a = Math.atan2(y - cy, x - cx);
      if (d > -9 && d < -3 && Math.abs(a) < 1.25) return hex("#ff6a8a"); // retina lining the back
      if (d < -9) return mix(hex("#d8e8ff"), hex("#a8c0f0"), sat(-d / r)); // vitreous
      return null;
    },
  });
  paint(cx - r - 14, cy - 30, cx - r + 12, cy + 30, (x, y) => Math.max(ell(cx - r + 2, cy, 12, 28)(x, y), cx - r - 2 - x + 0 * y), { base: hex("#c8f0ff"), lite: hex("#ffffff"), dark: hex("#6aa8d8"), puff: 6, alpha: 0.7 });
  paint(cx - r + 4, cy - 26, cx - r + 34, cy + 26, ell(cx - r + 18, cy, 10, 22), { base: hex("#8ae8ff"), lite: hex("#e8ffff"), dark: hex("#2a8ab8"), puff: 10, alpha: 0.9 });
  // iris edges
  rect(cx - r + 6, cy - 30, 4, 8, hex("#2a8a6a")); rect(cx - r + 6, cy + 22, 4, 8, hex("#2a8a6a"));
  return { lensX: cx - r + 18, lensY: cy, retinaX: cx + r - 7 };
};

export const rays = (ox: number, top: number, bot: number, lx: number, ly: number, rx: number, ry: number, h: number, upto: number) => {
  const c1 = hex("#ffe600"), c2 = hex("#5ce1e6");
  // top of the object lands at the bottom of the retina and vice versa
  const k1 = sat(upto * 2), k2 = sat(upto * 2 - 1);
  line(ox, top, lx, ly, c1, 0.95, k1); line(ox, bot, lx, ly, c2, 0.95, k1);
  if (k2 > 0) { line(lx, ly, rx, ry + h / 2, c1, 0.95, k2); line(lx, ly, rx, ry - h / 2, c2, 0.95, k2); }
};

// ---------- the brain ----------
export const brainChar = (cx: number, cy: number, s: number, face: "happy" | "wink" | "focus" | "dizzy", f: number) => {
  push(cx, cy, 0, s, s);
  paint(-12, 30, 12, 72, capsule(0, 34, 6, 66, 9, 6), { base: hex("#f0a0b8"), lite: hex("#ffd0dc"), dark: hex("#a0406a"), puff: 7 });
  const shape = blend(10, ell(0, 0, 62, 44), ell(-26, 20, 30, 22), ell(28, 22, 28, 20), ell(0, -24, 46, 26));
  paint(-66, -54, 66, 48, shape, {
    base: hex("#ff8ab0"), lite: hex("#ffd0e0"), dark: hex("#a0306a"), puff: 28,
    tex: (x, y, d, lam) => {
      if (d > -3) return null;
      const g = Math.sin(x * 0.26 + Math.sin(y * 0.23) * 2.6) * Math.cos(y * 0.21 + Math.sin(x * 0.17) * 2.2);
      if (Math.abs(g) < 0.11) return mix(hex("#c0407a"), hex("#ff9ac0"), lam * 0.5);
      if (Math.abs(x) < 1.2 && y < 6) return hex("#c0407a");
      return null;
    },
  });
  const dk = hex("#1a1038"), flat: Mat = { base: dk, flat: true, line: null, rim: 0 };
  for (const sd of [-1, 1]) {
    const ex = sd * 17, ey = 12;
    if (face === "dizzy") { paint(ex - 7, ey - 7, ex + 7, ey + 7, union(capsule(ex - 4, ey - 4, ex + 4, ey + 4, 1.1), capsule(ex - 4, ey + 4, ex + 4, ey - 4, 1.1)), flat); continue; }
    if ((face === "wink" && sd > 0) || (f + 21) % 93 < 4) { paint(ex - 8, ey - 6, ex + 8, ey + 6, arc(ex, ey - 3, 5.5, 0.4, 2.75, 1.1), flat); continue; }
    paint(ex - 8, ey - 10, ex + 8, ey + 10, ell(ex, ey, 6.5, 8), { base: hex("#ffffff"), flat: true, rim: 0 });
    const lx = face === "focus" ? 0 : Math.sin(f * 0.05) * 1.5;
    paint(ex - 6, ey - 6, ex + 6, ey + 6, circle(ex + lx, ey + 1, 4), { ...flat, base: hex("#2a1450") });
    paint(ex - 3, ey - 4, ex + 1, ey, circle(ex + lx - 1, ey - 1.5, 1.5), { ...flat, base: hex("#ffffff") });
  }
  if (face === "dizzy") paint(-8, 22, 8, 32, (x, y) => Math.abs(y - 27 - Math.sin(x * 1.1) * 1.4) - 0.9 + Math.max(0, Math.abs(x) - 6) * 9, flat);
  else paint(-9, 20, 9, 32, arc(0, 22, 6.5, 0.45, 2.7, 1.1), flat);
  pop();
};

// picture frame showing a little landscape, rotatable
export const picture = (cx: number, cy: number, rot: number, s: number) => {
  push(cx, cy, rot, s, s);
  paint(-40, -32, 40, 32, rbox(0, 0, 38, 30, 3), {
    base: hex("#e8b44e"), lite: hex("#fff0a0"), dark: hex("#8a5a2a"), puff: 4,
    tex: (x, y, d) => {
      if (d < -5) {
        if (y > 12) return hex("#3ac86a");
        return mix(hex("#7ad0ff"), hex("#c8f0ff"), (y + 30) / 42);
      }
      return null;
    },
  });
  paint(14, -24, 30, -8, circle(22, -16, 6), { base: hex("#ffe14e"), flat: true, line: null, rim: 0 });
  pop();
  push(cx, cy, rot, s, s); tree(-12, 22, 0.42); pop();
};

// tube goggles (Stratton's inverting lenses)
export const goggles = (cx: number, cy: number) => {
  paint(cx - 40, cy - 6, cx + 40, cy + 6, rbox(cx, cy, 38, 2.5, 1), { base: hex("#2a2a3a"), puff: 2, rim: 0 });
  for (const s of [-1, 1]) {
    paint(cx + s * 13 - 12, cy - 12, cx + s * 13 + 12, cy + 12, circle(cx + s * 13, cy, 10), { base: hex("#4a4a6a"), lite: hex("#9a9ac8"), dark: hex("#1a1a2a"), puff: 6 });
    paint(cx + s * 13 - 8, cy - 8, cx + s * 13 + 8, cy + 8, circle(cx + s * 13, cy, 6.5), { base: hex("#5ce1e6"), lite: hex("#e0ffff"), dark: hex("#1a5a8a"), puff: 6, rim: 0 });
    put(cx + s * 13 - 3, cy - 3, hex("#ffffff")); put(cx + s * 13 - 2, cy - 3, hex("#ffffff"));
  }
};

export const calendar = (x: number, y: number, day: number, labels: Label[]) => {
  paint(x - 2, y - 2, x + 50, y + 50, rbox(x + 24, y + 24, 24, 24, 4), { base: hex("#fff6e0"), lite: hex("#ffffff"), dark: hex("#b8a8c8"), puff: 6 });
  rect(x + 2, y + 2, 44, 12, hex("#ff4a6a"));
  labels.push({ s: "DAY", x: x + 14, y: y + 1, c: "#ffffff", plain: true });
  labels.push({ s: String(day), x: x + (day > 9 ? 11 : 18), y: y + 19, c: "#2a1450", size: 32, plain: true });
};
