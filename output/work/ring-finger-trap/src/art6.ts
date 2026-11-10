import { W, H, RGB, Mat, hex, mix, sat, lerp, hash, noise, put, addPx, rect, glow, paint, push, pop, circle, ell, rbox, capsule, blend, union, light } from "./gfx";
import { arc, Label } from "./art";

const flat = (c: string, a = 1): Mat => ({ base: hex(c), flat: true, line: null, rim: 0, alpha: a });

// ---------- top-down desk: walnut planks, lamp pool, notebook, pencil, mug ----------
export const desk = (f: number, lamp = 1) => {
  for (let y = 0; y < H; y++) {
    const plank = Math.floor(y / 64), seam = y % 64 === 0;
    for (let x = 0; x < W; x++) {
      const g = noise(x * 0.012 + plank * 7.3, y * 0.18) * 0.6 + noise(x * 0.05 + plank * 3, y * 0.6) * 0.4;
      let c = mix(hex("#3a1c10"), hex("#8a4a24"), 0.25 + 0.6 * g);
      if (seam) c = hex("#1e0c06");
      const pool = sat(1 - Math.hypot((x - 120) / 230, (y - 290) / 260));
      put(x, y, mix(mix(c, hex("#0e0604"), 0.45), c, 0.35 + 0.65 * pool * lamp));
    }
  }
  glow(110, 270, 200, hex("#ffcf7a"), 0.22 * lamp, 1.1);
  // notebook bottom-left, slightly rotated
  push(46, 430, -0.22, 1, 1);
  paint(-48, -40, 48, 40, rbox(0, 0, 44, 34, 3), {
    base: hex("#f2ead8"), lite: hex("#ffffff"), dark: hex("#a89878"), puff: 4,
    tex: (x, y, d) => (d < -3 && (Math.floor(y + 40) % 7 === 0) ? hex("#9ab8d8") : d < -3 && x < -30 && x > -32 ? hex("#e87a7a") : null),
  });
  pop();
  // pencil
  push(236, 420, -1.0, 1, 1);
  paint(-40, -6, 40, 6, rbox(0, 0, 34, 3.2, 1), { base: hex("#ffc83a"), lite: hex("#fff0a0"), dark: hex("#a06a1a"), puff: 2 });
  paint(33, -5, 44, 5, (x, y) => Math.max(Math.abs(y) - (44 - x) * 0.32, 33 - x), { base: hex("#e8c8a0"), flat: true, rim: 0 });
  paint(-42, -5, -32, 5, rbox(-37, 0, 4, 3.2, 1), { base: hex("#ff8aa0"), puff: 2 });
  pop();
  // coffee mug top-right with a little steam
  paint(204, 140, 270, 206, circle(236, 172, 26), { base: hex("#e8f0ff"), lite: hex("#ffffff"), dark: hex("#8a9ac8"), puff: 8 });
  paint(212, 148, 260, 196, circle(236, 172, 19), { base: hex("#5a2e14"), lite: hex("#8a4a24"), dark: hex("#2a1206"), puff: 10, line: null, rim: 0 });
  paint(256, 160, 274, 186, arc(262, 172, 8, -1.4, 1.4, 2.6), { base: hex("#e8f0ff"), puff: 3 });
  for (let i = 0; i < 3; i++) { const t = ((f * 0.6 + i * 14) % 42) / 42; put(230 + i * 5 + Math.sin(t * 6 + i) * 3, 168 - t * 40, hex("#ffffff"), 0.35 * (1 - t)); }
};

// ---------- the hand, seen from above (back of the right hand, thumb on the left) ----------
const FING = [{ x: -25, len: 50, r: 7.4 }, { x: -8.5, len: 58, r: 7.9 }, { x: 8.5, len: 54, r: 7.7 }, { x: 24.5, len: 41, r: 6.5 }];
const BASE = -30;
export type HandState = { lift: number[]; fold: number; strain: number; air?: number };
export const tipOf = (cx: number, cy: number, s: number, i: number, st: HandState): [number, number] => {
  const F = FING[i], len = i === 1 ? F.len * (1 - 0.72 * st.fold) : F.len;
  return [cx + F.x * s, cy + (BASE - len) * s];
};

const SKIN = { base: hex("#f2b48a"), lite: hex("#ffe0c4"), dark: hex("#b8644e") };
const fingerMat = (lift: number, strain: number, folded: number, r: number, tipY: number, x0: number): Mat => ({
  base: mix(mix(SKIN.base, hex("#ff6a6a"), strain * 0.45), hex("#c8805e"), folded * 0.5),
  lite: mix(SKIN.lite, hex("#ffffff"), lift * 0.3), dark: SKIN.dark, puff: r + 2,
  tex: (x, y, d) => {
    if (folded < 0.5 && ell(x0, tipY + r * 0.9, r * 0.58, r * 0.85)(x, y) < 0) return mix(hex("#ffd8d0"), hex("#ffffff"), 0.3 + 0.3 * sat(-d / r)); // nail
    for (const k of [0.36, 0.66]) if (folded < 0.5 && Math.abs(y - (BASE - (BASE - tipY) * k)) < 0.6 && d < -2) return hex("#c87a62"); // knuckle creases
    return null;
  },
});

export const hand = (cx: number, cy: number, s: number, st: HandState, f: number) => {
  push(cx, cy, 0, s, s);
  const thumbLift = st.lift[0], air = st.air ?? 0;
  // shadow of the whole hand on the desk, plus deeper offsets for lifted fingers
  const shadow = (dx: number, dy: number, a: number, sdf: (x: number, y: number) => number) =>
    paint(-90, -120, 90, 170, (x, y) => sdf(x - dx - air * 16, y - dy - air * 20), { base: hex("#120604"), flat: true, line: null, rim: 0, alpha: a * (1 - air * 0.5) });
  shadow(4, 5, 0.38, union(rbox(0, 0, 33, 34, 14), rbox(0, 70, 30, 46, 8)));
  FING.forEach((F, i) => {
    const li = st.lift[i + 1], len = i === 1 ? F.len * (1 - 0.72 * st.fold) : F.len;
    shadow(4 + li * 9, 5 + li * 11, 0.38 - li * 0.12, capsule(F.x, BASE, F.x, BASE - len, F.r));
  });
  shadow(4 + thumbLift * 9, 5 + thumbLift * 11, 0.38 - thumbLift * 0.12, capsule(-27, 12, -50, -16, 8));
  // sleeve + wrist
  paint(-44, 60, 44, 140, rbox(0, 104, 38, 36, 7), {
    base: hex("#2f5aa8"), lite: hex("#6a94e0"), dark: hex("#14285a"), puff: 10,
    tex: (x, y) => (Math.abs(y - 76) < 0.7 ? hex("#ffc84e") : (Math.floor(x * 0.7 + y * 0.7) % 5 === 0 ? hex("#284c94") : null)),
  });
  paint(-34, 20, 34, 72, rbox(0, 46, 27, 26, 10), { ...SKIN, puff: 14 });
  // back of the hand with knuckle bumps
  paint(-38, -42, 38, 40, rbox(0, 0, 33, 34, 14), {
    ...SKIN, puff: 18,
    tex: (x, y) => {
      for (const F of FING) if (Math.hypot(x - F.x, y + 27) < 5) return SKIN.lite;
      if (Math.abs(x + 4 - y * 0.15) < 0.6 && y > -10 && y < 26) return hex("#e09a78"); // a vein
      return null;
    },
  });
  // thumb
  const tl = 1 + thumbLift * 0.16;
  paint(-64, -30, -14, 26, capsule(-27, 12, -50 - thumbLift * 2, -16 - thumbLift * 3, 8 * tl, 7.5 * tl), fingerMat(thumbLift, 0, 0, 8, -100, -999));
  paint(-60, -26, -40, -6, ell(-48 - thumbLift * 2, -14 - thumbLift * 3, 4.6, 5.6), { base: hex("#ffd8d0"), lite: hex("#ffffff"), puff: 4, rim: 0 });
  // fingers
  FING.forEach((F, i) => {
    const li = st.lift[i + 1], folded = i === 1 ? st.fold : 0, strain = i === 2 ? st.strain : 0;
    const len = i === 1 ? F.len * (1 - 0.72 * folded) : F.len, r = F.r * (1 + li * 0.17);
    const jx = strain * Math.sin(f * 2.9) * 1.1, x = F.x + jx, tip = BASE - len;
    paint(x - r - 3, tip - r - 3, x + r + 3, BASE + 6, capsule(x, BASE + 4, x, tip, r * 1.02, r), fingerMat(li, strain, folded, r, tip, x));
    if (folded > 0.3) paint(x - r, tip - r, x + r, tip + r, ell(x, tip + 2, r * 0.9, r * 0.7), { base: hex("#d89070"), lite: hex("#ffd0b0"), puff: 4, rim: 0, alpha: sat((folded - 0.3) * 2) });
    if (strain > 0.05) for (let k = 0; k < 3; k++) { const a = sat(strain) * (0.5 + 0.5 * Math.sin(f * 0.8 + k)); paint(x + r + 2, tip + 4 + k * 7, x + r + 12, tip + 8 + k * 7, capsule(x + r + 3, tip + 6 + k * 7, x + r + 9, tip + 3 + k * 7, 0.9), flat("#ff4a4a", a)); }
  });
  pop();
};

// ---------- x-ray of the same hand: bones, extensor tendons and the band that ties middle + ring ----------
export const xrayBg = (f: number) => {
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const scan = ((y - f * 3) % 160 + 160) % 160 < 3 ? 0.06 : 0;
    put(x, y, mix(hex("#0a2a3a"), hex("#02080e"), sat(Math.hypot((x - 135) / 210, (y - 280) / 260))).map(v => v + scan) as RGB);
  }
};
export const xrayHand = (cx: number, cy: number, s: number, st: HandState, f: number, bandPulse: number) => {
  push(cx, cy, 0, s, s);
  const sil = union(rbox(0, 0, 33, 34, 14), rbox(0, 50, 27, 30, 10), capsule(-27, 12, -50, -16, 8), ...FING.map((F, i) => capsule(F.x, BASE, F.x, BASE - (i === 1 ? F.len * (1 - 0.72 * st.fold) : F.len), F.r)));
  paint(-70, -100, 70, 90, sil, { base: hex("#4ad8e8"), flat: true, line: hex("#8af0ff"), rim: 0, alpha: 0.18 });
  const bone: Mat = { base: hex("#e8fbff"), lite: hex("#ffffff"), dark: hex("#5ab0c8"), puff: 3, line: hex("#2a8aa8"), rim: 0 };
  // wrist bones
  for (let k = 0; k < 6; k++) { const bx = -18 + (k % 3) * 18, by = 44 + Math.floor(k / 3) * 12; paint(bx - 9, by - 7, bx + 9, by + 7, ell(bx, by, 7.5, 5.2), bone); }
  // thumb
  paint(-56, -26, -16, 34, capsule(-18, 30, -33, 4, 3.4), bone); paint(-56, -26, -16, 20, capsule(-36, 0, -46, -14, 3), bone);
  FING.forEach((F, i) => {
    const len = i === 1 ? F.len * (1 - 0.72 * st.fold) : F.len;
    paint(F.x - 8, -32, F.x + 8, 40, capsule(F.x * 0.55, 34, F.x, BASE + 2, 3.2, 2.8), bone); // metacarpal
    const segs = [0.42, 0.33, 0.25]; let y0 = BASE - 1;
    for (let k = 0; k < 3; k++) {
      const l = len * segs[k] - 2; if (l < 1) break;
      paint(F.x - 7, y0 - l - 4, F.x + 7, y0 + 4, capsule(F.x, y0, F.x, y0 - l, 3 - k * 0.4), bone); y0 -= l + 2;
    }
  });
  // extensor tendons (glowing) from fingertips to the wrist
  FING.forEach((F, i) => {
    const len = i === 1 ? F.len * (1 - 0.72 * st.fold) : F.len, tight = i === 1 ? st.fold : 0, red = i === 2 ? st.strain : 0;
    const c = red > 0.05 ? mix(hex("#ffb84e"), hex("#ff3a3a"), red * (0.6 + 0.4 * Math.sin(f * 0.9))) : mix(hex("#ffb84e"), hex("#fff2a0"), tight);
    const jx = red * Math.sin(f * 2.9) * 0.8;
    paint(-60, -100, 60, 80, capsule(F.x + jx, BASE - len + 4, F.x * 0.3, 70, 1.3 + tight * 0.5), { base: c, flat: true, line: null, rim: 0, alpha: 0.95 });
  });
  // the connecting band (juncturae tendinum) between middle and ring
  const bc = mix(hex("#ffb84e"), hex("#ff3a3a"), bandPulse);
  paint(-14, -16, 14, 6, capsule(FING[1].x * 0.8, -4, FING[2].x * 0.8, -10, 2.2 + bandPulse * 1.2), { base: bc, flat: true, line: null, rim: 0 });
  pop();
  if (bandPulse > 0.05) glow(cx, cy - 7 * s, 26 * s, hex("#ff4a4a"), 0.35 * bandPulse);
  return [cx, cy - 7 * s] as [number, number];
};

/** Padlock icon (for the hook), shackle open when `open` > 0. */
export const padlock = (x: number, y: number, s: number, open: number, shake: number) => {
  push(x + shake, y, 0, s, s);
  paint(-12, -26 - open * 8, 12, 0, arc(0, -10 - open * 8, 8, -Math.PI, 0, 2.4), { base: hex("#c8ccd8"), lite: hex("#ffffff"), dark: hex("#5a5e78"), puff: 3 });
  paint(-14, -12, 14, 14, rbox(0, 1, 12, 11, 3), { base: hex("#ffc83a"), lite: hex("#fff0a0"), dark: hex("#9a5a1a"), puff: 6 });
  paint(-4, -6, 4, 8, union(circle(0, -1, 2.6), rbox(0, 4, 1.2, 4, 0.6)), { base: hex("#3a1a0a"), flat: true, line: null, rim: 0 });
  pop();
};

export const sparkle = (x: number, y: number, r: number, c: RGB, a = 1) => {
  x = Math.round(x); y = Math.round(y);
  for (let i = -r; i <= r; i++) { put(x + i, y, c, a); put(x, y + i, c, a); }
};
export { glow, light, lerp, addPx, rect, hash };
