import { W, H, RGB, SDF, Mat, hex, mix, sat, clamp, lerp, sstep, hash, noise, fbm, put, addPx, rect, glow, paint, push, pop,
  circle, ell, rbox, capsule, blend, union, minus, light, toWorld, scl } from "./gfx";
import { arc, sparkle, Label, Suit } from "./art";

export const COURIER: Suit = { pj: hex("#b86a32"), pjLite: hex("#f0a860"), pjDark: hex("#5a2a2a"), stripe: null, shoe: hex("#3a2a3a") };
export const RECEIVER: Suit = { pj: hex("#6a4ae8"), pjLite: hex("#a890ff"), pjDark: hex("#2a1a7a"), stripe: null, shoe: hex("#f0f0f0") };
export const GAMER: Suit = { pj: hex("#e8483e"), pjLite: hex("#ff9a8a"), pjDark: hex("#7a1a3a"), stripe: null, shoe: hex("#2a2a3a") };

const flat = (c: string, alpha = 1): Mat => ({ base: hex(c), flat: true, line: null, rim: 0, alpha });

// cap for the courier (call after hero; head centre in world coords, scale sc)
export const cap = (hx: number, hy: number, sc: number) => {
  push(hx, hy, 0, sc, sc);
  paint(-36, -40, 36, -10, (x, y) => Math.max(ell(0, -14, 34, 26)(x, y), y + 14), { base: hex("#ffc94e"), lite: hex("#fff0a0"), dark: hex("#a8602a"), puff: 10 });
  paint(-10, -22, 46, -8, rbox(20, -15, 24, 4, 3), { base: hex("#e8a83e"), puff: 3 });
  pop();
};

// ---------- night street ----------
export const nightStreet = (f: number, scroll: number) => {
  for (let y = 0; y < H; y++) { const c = mix(hex("#0a0a3a"), hex("#4a2a7a"), Math.pow(y / 210, 1.4)); for (let x = 0; x < W; x++) put(x, y, c); }
  for (let i = 0; i < 90; i++) put(hash(i, 1) * W, hash(i, 2) * 120, hex("#ffffff"), 0.4 + 0.5 * Math.sin(f * 0.13 + i) ** 2);
  glow(400, 40, 50, hex("#ffe6a0"), 0.35); paint(388, 28, 412, 52, circle(400, 40, 10), { base: hex("#fff2c0"), flat: true, line: null, rim: 0 });
  for (const [k, par, base, hgt, col] of [[0, 0.2, 150, 70, "#1e1650"], [1, 0.5, 175, 60, "#2a1e66"]] as const) {
    for (let x = 0; x < W; x++) {
      const u = x + scroll * par, b = Math.floor(u / 22), h = 20 + hash(b, k + 5) * hgt, top = base + 40 - h;
      for (let y = Math.round(top); y < 212; y++) {
        const lit = (Math.floor(u) % 6 === 2) && (y % 7 === 3) && hash(b * 13 + Math.floor(u / 6), y) > 0.55;
        put(x, y, lit ? hex("#ffd86b") : hex(col));
      }
    }
  }
  rect(0, 210, W, 12, hex("#5a5a7a")); rect(0, 210, W, 1, hex("#8a8aa8"));
  for (let x = 0; x < W; x++) for (let y = 222; y < H; y++) put(x, y, mix(hex("#2a2a3a"), hex("#1a1a28"), (y - 222) / 48));
  for (let i = -1; i < 12; i++) { const x = ((i * 48 - scroll) % 528 + 528) % 528 - 48; rect(x, 245, 24, 3, hex("#e8e0a0")); }
  for (let i = 0; i < 4; i++) { // street lamps
    const x = ((i * 140 + 40 - scroll * 1.0) % 560 + 560) % 560 - 40;
    rect(x, 120, 3, 92, hex("#3a3a5a")); rect(x - 6, 118, 12, 4, hex("#5a5a7a"));
    glow(x + 1, 124, 46, hex("#ffd27a"), 0.45); glow(x + 1, 214, 30, hex("#ffd27a"), 0.25, 0.25);
  }
};

export const van = (x: number, gy: number, f: number, moving: boolean, labels: Label[]) => {
  const spin = moving ? f * 0.5 : 0;
  paint(x - 2, gy - 66, x + 94, gy - 12, rbox(x + 46, gy - 39, 46, 26, 4), { base: hex("#f4f0e8"), lite: hex("#ffffff"), dark: hex("#8a8ab0"), puff: 10 });
  rect(x + 6, gy - 48, 80, 16, hex("#2a8ae8")); labels.push({ s: "TCP", x: Math.round(x + 32), y: gy - 49, c: "#ffffff", size: 24, plain: true });
  paint(x + 90, gy - 50, x + 130, gy - 12, rbox(x + 110, gy - 31, 19, 19, 6), { base: hex("#2a8ae8"), lite: hex("#8ad0ff"), dark: hex("#0a2a7a"), puff: 8 });
  paint(x + 104, gy - 46, x + 126, gy - 30, rbox(x + 116, gy - 38, 9, 7, 3), { base: hex("#bfe8ff"), lite: hex("#ffffff"), puff: 4, rim: 0 });
  glow(x + 130, gy - 22, 30, hex("#fff0b0"), 0.45);
  for (const wx of [x + 22, x + 72, x + 112]) {
    paint(wx - 11, gy - 23, wx + 11, gy - 1, circle(wx, gy - 12, 10), { base: hex("#22222e"), lite: hex("#4a4a5a"), puff: 6, rim: 0 });
    paint(wx - 5, gy - 18, wx + 5, gy - 6, circle(wx, gy - 12, 4), { base: hex("#9a9ab8"), puff: 3, rim: 0 });
    put(wx + Math.cos(spin) * 7, gy - 12 + Math.sin(spin) * 7, hex("#6a6a8a"));
  }
};

export const bike = (x: number, gy: number, f: number, labels: Label[]) => {
  for (const wx of [x, x + 44]) {
    paint(wx - 11, gy - 23, wx + 11, gy - 1, minus(circle(wx, gy - 12, 10), circle(wx, gy - 12, 6)), { base: hex("#22222e"), puff: 3, rim: 0 });
  }
  paint(x - 4, gy - 34, x + 50, gy - 10, blend(4, rbox(x + 22, gy - 20, 22, 6, 4), rbox(x + 34, gy - 28, 10, 6, 3)), { base: hex("#e8303a"), lite: hex("#ff8a8a"), dark: hex("#7a0a2a"), puff: 6 });
  paint(x + 12, gy - 62, x + 36, gy - 26, capsule(x + 22, gy - 30, x + 26, gy - 52, 6), { base: hex("#2a2a4a"), puff: 5 });
  paint(x + 16, gy - 74, x + 40, gy - 50, circle(x + 28, gy - 62, 10), { base: hex("#ffe14e"), lite: hex("#fff6c0"), dark: hex("#c0702a"), puff: 8 });
  paint(x + 28, gy - 66, x + 40, gy - 58, rbox(x + 34, gy - 62, 5, 3, 2), { base: hex("#2a2a4a"), flat: true, rim: 0 });
  labels.push({ s: "UDP", x: Math.round(x + 8), y: gy - 30, c: "#ffffff" });
  for (let i = 0; i < 5; i++) { const t = (f * 0.3 + i * 7) % 30; rect(x - 10 - t * 3, gy - 18 + (i % 3) * 4, 6 + t * 0.4, 1, hex("#ffffff"), 0.5 * (1 - t / 30)); }
};

export const leaflet = (x: number, y: number, r: number) => {
  push(x, y, r); paint(-6, -5, 6, 5, rbox(0, 0, 5, 3.5, 0.5), { base: hex("#f4f4ff"), puff: 2, rim: 0 }); pop();
};

// ---------- doorstep ----------
export const doorstep = (f: number, doorOpen: number) => {
  for (let y = 0; y < 228; y++) for (let x = 0; x < W; x++) {
    const row = Math.floor(y / 8), off = row % 2 ? 10 : 0, mortar = y % 8 === 0 || (x + off) % 20 === 0;
    const v = hash(Math.floor((x + off) / 20), row);
    put(x, y, mortar ? hex("#5a2a2a") : mix(hex("#a8503a"), hex("#c8684a"), v));
  }
  glow(240, 100, 280, hex("#ffb060"), 0.12);
  // window with warm light
  paint(56, 60, 150, 150, rbox(103, 105, 44, 42, 2), { base: hex("#e8b44e"), lite: hex("#fff0a0"), dark: hex("#7a4a2a"), puff: 3 });
  for (let y = 66; y < 145; y++) for (let x = 62; x < 145; x++) put(x, y, mix(hex("#ffe0a0"), hex("#ffb060"), (y - 66) / 80));
  rect(102, 66, 2, 79, hex("#7a4a2a")); rect(62, 104, 83, 2, hex("#7a4a2a"));
  glow(103, 105, 80, hex("#ffc870"), 0.3);
  // door frame + door
  paint(296, 92, 384, 230, rbox(340, 161, 42, 68, 2), { base: hex("#f0e6d0"), lite: hex("#ffffff"), dark: hex("#a89a80"), puff: 4 });
  for (let y = 100; y < 228; y++) for (let x = 304; x < 376; x++) put(x, y, mix(hex("#2a1a1a"), hex("#ffb060"), 0.25 * doorOpen));
  const dw = Math.round(72 * (1 - doorOpen * 0.82));
  paint(304, 100, 304 + dw, 228, rbox(304 + dw / 2, 164, Math.max(2, dw / 2), 64, 2), {
    base: hex("#2a6a5a"), lite: hex("#5aa890"), dark: hex("#0a2a2a"), puff: 6,
    tex: (x, y) => (dw > 30 && (Math.abs(y - 130) < 1 || Math.abs(y - 196) < 1) && x > 312 && x < 296 + dw ? hex("#1a4a3a") : null),
  });
  if (dw > 20) paint(304 + dw - 12, 160, 304 + dw - 2, 170, circle(304 + dw - 7, 165, 3), { base: hex("#ffd84e"), puff: 2 });
  // steps + mat + plant
  rect(0, 228, W, 42, hex("#6a6a7a")); rect(0, 228, W, 2, hex("#9a9aa8"));
  paint(286, 226, 394, 240, rbox(340, 233, 52, 6, 2), { base: hex("#9a9ab0"), puff: 3 });
  paint(400, 196, 430, 230, (x, y) => Math.max(Math.abs(x - 415) - (12 - (y - 200) * 0.1), Math.abs(y - 214) - 14), { base: hex("#d8643e"), puff: 6 });
  for (let i = 0; i < 5; i++) { const a = -0.9 + i * 0.45 + Math.sin(f * 0.05 + i) * 0.08; paint(395, 160, 435, 202, capsule(415, 200, 415 + Math.sin(a) * 22, 200 - Math.cos(a) * 30, 2, 5), { base: hex("#2fae7a"), lite: hex("#8ae8a0"), puff: 4 }); }
  rect(392, 120, 8, 10, hex("#e8e0c0")); glow(396, 126, 26, hex("#ffe6a0"), 0.5 + 0.06 * Math.sin(f * 0.7));
  const mx = 396 + Math.cos(f * 0.21) * 12 + Math.sin(f * 0.53) * 3, my = 124 + Math.sin(f * 0.27) * 8;
  put(mx, my, hex("#3a2a2a")); put(mx - 1, my - (Math.floor(f / 2) % 2), hex("#c8b8a8")); put(mx + 1, my - (Math.floor(f / 2) % 2), hex("#c8b8a8"));
};

export const box = (cx: number, by: number, n: number | null, labels: Label[], s = 1, alpha = 1) => {
  const hw = 13 * s, hh = 11 * s;
  paint(cx - hw - 2, by - hh * 2 - 2, cx + hw + 2, by + 2, rbox(cx, by - hh, hw, hh, 2), {
    base: hex("#d89a5a"), lite: hex("#f4c890"), dark: hex("#7a4a2a"), puff: 6, alpha,
    tex: (x) => (Math.abs(x - cx) < 2 * s ? hex("#c8803e") : null),
  });
  if (n !== null && alpha > 0.5) labels.push({ s: String(n), x: Math.round(cx - 3), y: Math.round(by - hh - 9), c: "#2a1a1a", size: 16, plain: true });
};

export const bubble = (x: number, y: number, w: number, text: string, labels: Label[], tail: -1 | 1, col = "#ffffff", tcol = "#1a1038") => {
  const h = 20;
  paint(x - 2, y - 2, x + w + 2, y + h + 8, union(rbox(x + w / 2, y + h / 2, w / 2, h / 2, 5), capsule(x + w / 2 + tail * w * 0.25, y + h - 2, x + w / 2 + tail * w * 0.32, y + h + 6, 3, 0.5)), { base: hex(col), flat: true, rim: 0, line: hex("#1a1038") });
  labels.push({ s: text, x: Math.round(x + w / 2 - text.length * 4.5 + 1), y: y + 1, c: tcol, size: 24, plain: true });
};

export const stopwatch = (cx: number, cy: number, p: number, alarm: boolean) => {
  paint(cx - 3, cy - 18, cx + 3, cy - 12, rbox(cx, cy - 15, 2, 2, 1), flat("#9a9ab8"));
  paint(cx - 14, cy - 14, cx + 14, cy + 14, circle(cx, cy, 12), { base: alarm ? hex("#ff4a5a") : hex("#f4f4ff"), lite: hex("#ffffff"), puff: 8, line: hex("#1a1038") });
  const a = p * Math.PI * 2;
  paint(cx - 12, cy - 12, cx + 12, cy + 12, capsule(cx, cy, cx + Math.sin(a) * 9, cy - Math.cos(a) * 9, 1), flat("#1a1038"));
  if (alarm) glow(cx, cy, 30, hex("#ff4a5a"), 0.5);
};

// ---------- home <-> server ----------
export const homeToServer = (f: number) => {
  for (let y = 0; y < H; y++) { const c = mix(hex("#2a5ac8"), hex("#8ad0ff"), y / 200); for (let x = 0; x < W; x++) put(x, y, c); }
  for (let i = 0; i < 4; i++) { const cx = ((i * 140 + f * 0.25) % 620) - 70, cy = 40 + i * 14; paint(cx - 30, cy - 12, cx + 30, cy + 10, union(ell(cx, cy, 24, 7), ell(cx + 10, cy - 5, 14, 8)), { base: hex("#ffffff"), lite: hex("#ffffff"), dark: hex("#c8d8f0"), line: null, puff: 6, rim: 0 }); }
  rect(0, 222, W, 48, hex("#4a9a4a")); rect(0, 222, W, 2, hex("#8ad88a"));
  // house
  paint(20, 120, 140, 224, rbox(80, 172, 56, 50, 2), { base: hex("#f2d2a0"), lite: hex("#fff0d0"), dark: hex("#a8805a"), puff: 10 });
  paint(10, 70, 150, 128, (x, y) => Math.max(Math.abs(x - 80) - (y - 74) * 1.2, y - 126), { base: hex("#c8403a"), lite: hex("#ff7a6a"), dark: hex("#6a1a2a"), puff: 8 });
  paint(40, 140, 100, 190, rbox(70, 165, 28, 23, 2), { base: hex("#7a4a2a"), puff: 2 });
  for (let y = 145; y < 186; y++) for (let x = 45; x < 96; x++) put(x, y, mix(hex("#3a2a6a"), hex("#5a4a9a"), (y - 145) / 40));
  // person at a laptop inside the window
  paint(56, 160, 84, 186, circle(70, 168, 7), { base: hex("#f7c49a"), puff: 5 }); paint(60, 156, 80, 168, (x, y) => Math.max(circle(70, 166, 8)(x, y), y - 165), { base: hex("#e0702e"), puff: 5 });
  paint(54, 174, 86, 186, rbox(70, 181, 14, 5, 2), { base: hex("#17a58f"), puff: 3 });
  paint(72, 172, 96, 186, rbox(84, 182, 10, 3, 1), { base: hex("#9a9ab8"), puff: 2 }); glow(84, 178, 14, hex("#5ce1e6"), 0.6);
  // server building
  paint(330, 50, 470, 224, rbox(400, 137, 68, 86, 3), { base: hex("#5a6a8a"), lite: hex("#8a9ac8"), dark: hex("#2a2a4a"), puff: 10 });
  for (let r = 0; r < 6; r++) for (let c = 0; c < 4; c++) {
    const x = 344 + c * 32, y = 64 + r * 25;
    rect(x, y, 26, 18, hex("#1a1a2a"));
    for (let k = 0; k < 3; k++) { const on = Math.sin(f * 0.3 + r * 2 + c * 3 + k * 1.7) > 0.2; rect(x + 3 + k * 7, y + 4, 4, 2, hex(on ? "#55efc4" : "#1a5a4a")); rect(x + 3 + k * 7, y + 10, 4, 2, hex(Math.sin(f * 0.21 + k + r) > 0.5 ? "#ffd86b" : "#4a3a1a")); }
  }
  // poles + cable
  for (const px of [150, 330]) rect(px - 2, 110, 4, 114, hex("#5a3a2a"));
  const cableY = (x: number) => 112 + Math.sin(((x - 150) / 180) * Math.PI) * 26;
  for (let x = 150; x <= 330; x++) { put(x, cableY(x), hex("#1a1a2a")); put(x, cableY(x) + 1, hex("#1a1a2a")); }
  return cableY;
};

// ---------- stadium + living room ----------
export const stadium = (x0: number, w: number, f: number) => {
  for (let y = 0; y < H; y++) for (let x = x0; x < x0 + w; x++) {
    let c: RGB;
    if (y < 70) c = mix(hex("#0a0a3a"), hex("#2a2a6a"), y / 70);
    else if (y < 130) {
      // rows of fans: a head over a shirt in each 6x8 seat, bobbing a little
      const row = Math.floor((y - 70) / 8), seat = Math.floor((x - x0 + (row % 2) * 3) / 6), lx = (x - x0 + (row % 2) * 3) % 6;
      const bob = Math.sin(f * 0.25 + seat * 0.9 + row) > 0.6 ? 1 : 0, ly = (y - 70) % 8 + bob;
      const shirt = hex(["#ff5a5a", "#5ce1e6", "#ffe14e", "#ffffff", "#3a7ae8"][Math.floor(hash(seat, row) * 5)]);
      c = mix(hex("#2a1e4a"), hex("#3a2a5a"), row / 8);
      if (lx >= 2 && lx <= 3 && ly >= 1 && ly <= 2) c = hex(hash(seat, row + 9) > 0.5 ? "#f7c49a" : "#c08a5a");
      else if (lx >= 1 && lx <= 4 && ly >= 3 && ly <= 6) c = shirt;
    }
    else { const stripe = Math.floor((x - x0) / 30) % 2; c = stripe ? hex("#3aa84a") : hex("#4cbc5a"); if (y === 132 || y === 268 || x === x0 + Math.floor(w / 2)) c = hex("#e8ffe8"); }
    put(x, y, c);
  }
  for (const lx of [x0 + 30, x0 + w - 30]) { rect(lx - 1, 20, 3, 50, hex("#8a8aa8")); glow(lx, 22, 60, hex("#fff6d0"), 0.5); rect(lx - 8, 16, 18, 6, hex("#fff6d0")); }
  // players chasing the ball
  const bx = x0 + w / 2 + Math.sin(f * 0.05) * w * 0.32, by = 200 + Math.sin(f * 0.08) * 34;
  for (let i = 0; i < 6; i++) {
    const px = bx + Math.cos(i * 1.7 + f * 0.03) * (20 + i * 9), py = by + Math.sin(i * 2.3 + f * 0.04) * 22, team = i % 2 ? "#ff4a5a" : "#3a7ae8";
    paint(px - 5, py - 16, px + 5, py, rbox(px, py - 7, 3.5, 6, 2), { base: hex(team), puff: 3, rim: 0 });
    paint(px - 4, py - 22, px + 4, py - 12, circle(px, py - 17, 3), { base: hex("#f7c49a"), puff: 2, rim: 0 });
  }
  paint(bx - 4, by - 4, bx + 4, by + 4, circle(bx, by, 2.6), { base: hex("#ffffff"), puff: 2, rim: 0 });
};

export const camera = (x: number, gy: number, f: number) => {
  rect(x - 1, gy - 40, 2, 40, hex("#2a2a3a")); rect(x - 12, gy - 2, 24, 2, hex("#2a2a3a"));
  paint(x - 20, gy - 58, x + 22, gy - 36, rbox(x, gy - 47, 18, 9, 3), { base: hex("#3a3a4a"), lite: hex("#7a7a9a"), puff: 5 });
  paint(x + 14, gy - 54, x + 30, gy - 40, rbox(x + 22, gy - 47, 7, 5, 2), { base: hex("#1a1a2a"), puff: 3 });
  if (Math.floor(f / 10) % 2) { rect(x - 14, gy - 52, 3, 3, hex("#ff3a3a")); glow(x - 13, gy - 51, 6, hex("#ff3a3a"), 0.8); }
};

export const livingRoom = (x0: number, w: number, f: number, glitch: number, cheer: boolean) => {
  for (let y = 0; y < H; y++) for (let x = x0; x < x0 + w; x++) put(x, y, y < 200 ? mix(hex("#3a2a6a"), hex("#5a3a8a"), y / 200) : mix(hex("#7a4a30"), hex("#5a3020"), (y - 200) / 70));
  glow(x0 + w / 2, 110, 120, hex("#5ce1e6"), 0.25);
  // TV with a miniature match
  const tx = x0 + w / 2 - 70, ty = 50, tw = 140, th = 84;
  rect(tx - 4, ty - 4, tw + 8, th + 8, hex("#1a1a2a"));
  for (let y = ty; y < ty + th; y++) for (let x = tx; x < tx + tw; x++) {
    let c = Math.floor((x - tx) / 14) % 2 ? hex("#3aa84a") : hex("#4cbc5a");
    if (glitch > 0 && hash(Math.floor((x - tx) / 6) + f * 7, Math.floor((y - ty) / 5)) < glitch) c = hex(["#ff4aff", "#4affff", "#1a1a1a", "#ffffff"][Math.floor(hash(x, y + f) * 4)]);
    put(x, y, c);
  }
  const bx = tx + tw / 2 + Math.sin(f * 0.05) * tw * 0.32, by = ty + th / 2 + Math.sin(f * 0.08) * th * 0.3;
  for (let i = 0; i < 6; i++) { const px = bx + Math.cos(i * 1.7 + f * 0.03) * (8 + i * 4), py = by + Math.sin(i * 2.3 + f * 0.04) * 9; rect(px - 1, py - 3, 3, 5, hex(i % 2 ? "#ff4a5a" : "#3a7ae8")); }
  rect(bx, by, 2, 2, hex("#ffffff"));
  rect(tx + tw / 2 - 20, ty + th + 4, 40, 6, hex("#2a2a3a"));
  // sofa + viewer from behind
  paint(x0 + w / 2 - 80, 180, x0 + w / 2 + 80, 262, union(rbox(x0 + w / 2, 236, 76, 22, 8), rbox(x0 + w / 2, 206, 70, 22, 8)), { base: hex("#c8403a"), lite: hex("#ff7a6a"), dark: hex("#5a1a2a"), puff: 12 });
  const jump = cheer ? Math.abs(Math.sin(f * 0.4)) * 6 : 0;
  paint(x0 + w / 2 - 24, 160 - jump, x0 + w / 2 + 24, 214 - jump, rbox(x0 + w / 2, 196 - jump, 20, 18, 8), { base: hex("#6a4ae8"), puff: 10 });
  paint(x0 + w / 2 - 16, 150 - jump, x0 + w / 2 + 16, 182 - jump, circle(x0 + w / 2, 166 - jump, 13), { base: hex("#2a1a3a"), lite: hex("#5a4a6a"), puff: 10 });
  if (cheer) for (const sd of [-1, 1]) paint(x0 + w / 2 + sd * 30 - 8, 130 - jump, x0 + w / 2 + sd * 30 + 8, 190 - jump, capsule(x0 + w / 2 + sd * 18, 186 - jump, x0 + w / 2 + sd * 28, 146 - jump, 5), { base: hex("#6a4ae8"), puff: 4 });
};

export const filmFrame = (x: number, y: number, broken = 0) => {
  if (broken > 0) { for (let i = 0; i < 6; i++) { const a = i * 1.05, r = broken * 16; rect(x + Math.cos(a) * r - 2, y + Math.sin(a) * r - 2, 4, 4, hex("#e8e8ff"), 1 - broken); } return; }
  rect(x - 9, y - 7, 18, 14, hex("#1a1a2a")); rect(x - 6, y - 4, 12, 8, hex("#4cbc5a"));
  for (let k = -1; k <= 1; k++) { rect(x - 8 + (k + 1) * 6, y - 6, 2, 1, hex("#ffffff")); rect(x - 8 + (k + 1) * 6, y + 5, 2, 1, hex("#ffffff")); }
  glow(x, y, 12, hex("#ffffff"), 0.25);
};

// ---------- game monitor ----------
export const gameScreen = (x: number, y: number, w: number, h: number, f: number, lag: boolean, labels: Label[]) => {
  rect(x - 4, y - 4, w + 8, h + 8, hex("#1a1a2a")); rect(x + w / 2 - 12, y + h + 4, 24, 10, hex("#2a2a3a")); rect(x + w / 2 - 24, y + h + 13, 48, 3, hex("#2a2a3a"));
  // when lagging, the picture only updates every 22 frames (packets waiting for retransmission)
  const ff = lag ? Math.floor(f / 22) * 22 : f;
  for (let yy = y; yy < y + h; yy++) for (let xx = x; xx < x + w; xx++) put(xx, yy, mix(hex("#2a5ac8"), hex("#8ad0ff"), (yy - y) / h));
  const scroll = ff * 1.4;
  for (let xx = x; xx < x + w; xx++) {
    const u = xx - x + scroll, top = y + h - 22 - (Math.floor(u / 40) % 3 === 1 ? 14 : 0);
    for (let yy = top; yy < y + h; yy++) put(xx, yy, yy === top ? hex("#8ae88a") : hex("#9a5a34"));
  }
  for (let i = 0; i < 6; i++) { const cx = x + ((i * 47 - scroll) % (w + 40) + w + 40) % (w + 40) - 20, cy = y + h - 44; if (cx > x + 2 && cx < x + w - 2) { paint(cx - 4, cy - 4, cx + 4, cy + 4, circle(cx, cy, 3), { base: hex("#ffd84e"), puff: 2, rim: 0 }); } }
  const jump = Math.abs(Math.sin(ff * 0.18)) * 16, px = x + w * 0.3, py = y + h - 22 - jump;
  paint(px - 6, py - 18, px + 6, py, rbox(px, py - 9, 5, 8, 2), { base: hex("#e8483e"), puff: 3, rim: 0 });
  paint(px - 5, py - 26, px + 5, py - 16, circle(px, py - 21, 4), { base: hex("#f7c49a"), puff: 3, rim: 0 });
  if (lag && Math.floor(f / 8) % 2) { rect(x + w / 2 - 20, y + 14, 40, 16, hex("#000000"), 0.6); labels.push({ s: "...", x: x + w / 2 - 12, y: y + 12, c: "#ffffff", size: 24, plain: true }); }
};

// ---------- icons (centre, size ~30 px) ----------
export const icon = (kind: string, cx: number, cy: number, f: number) => {
  const b = Math.sin(f * 0.1 + cx) * 1.5; cy += b;
  if (kind === "web") { paint(cx - 16, cy - 16, cx + 16, cy + 16, circle(cx, cy, 14), { base: hex("#3a8ae8"), lite: hex("#9ad0ff"), puff: 10, tex: (x, y) => (Math.abs(x - cx) < 1 || Math.abs(y - cy) < 1 || Math.abs(Math.hypot((x - cx) * 2, y - cy) - 14) < 1.2 ? hex("#e8f4ff") : null) }); }
  if (kind === "mail") { paint(cx - 18, cy - 12, cx + 18, cy + 12, rbox(cx, cy, 16, 11, 2), { base: hex("#f4f0e8"), puff: 6, tex: (x, y) => (Math.abs(Math.abs(x - cx) * 0.7 - (y - cy + 11) * 1) < 1.2 && y < cy + 2 ? hex("#c8403a") : null) }); }
  if (kind === "file") { paint(cx - 18, cy - 14, cx + 18, cy + 14, union(rbox(cx, cy + 2, 16, 11, 2), rbox(cx - 8, cy - 9, 8, 4, 2)), { base: hex("#ffc94e"), lite: hex("#fff0a0"), dark: hex("#c0702a"), puff: 8 }); }
  if (kind === "game") { paint(cx - 20, cy - 12, cx + 20, cy + 12, blend(6, rbox(cx, cy, 14, 8, 6), circle(cx - 12, cy + 4, 7), circle(cx + 12, cy + 4, 7)), { base: hex("#5a5ae8"), lite: hex("#9aa0ff"), puff: 8 }); rect(cx - 13, cy - 1, 7, 2, hex("#ffffff")); rect(cx - 10, cy - 4, 2, 7, hex("#ffffff")); rect(cx + 9, cy - 3, 3, 3, hex("#ff4a5a")); rect(cx + 13, cy, 3, 3, hex("#55efc4")); }
  if (kind === "call") { paint(cx - 18, cy - 14, cx + 18, cy + 14, rbox(cx - 3, cy, 12, 10, 3), { base: hex("#e8483e"), puff: 6 }); paint(cx + 6, cy - 10, cx + 20, cy + 10, (x, y) => Math.max(Math.abs(y - cy) - (x - cx - 8) * 0.8, x - cx - 18), { base: hex("#e8483e"), puff: 4 }); }
  if (kind === "live") { paint(cx - 18, cy - 14, cx + 18, cy + 14, rbox(cx, cy - 1, 16, 11, 2), { base: hex("#2a2a3a"), puff: 4 }); rect(cx - 13, cy - 9, 26, 16, hex("#4cbc5a")); if (Math.floor(f / 12) % 2) { rect(cx + 6, cy - 7, 5, 5, hex("#ff3a3a")); } }
  if (kind === "dns") { paint(cx - 16, cy - 16, cx + 18, cy + 18, union(minus(circle(cx - 3, cy - 3, 11), circle(cx - 3, cy - 3, 7)), capsule(cx + 5, cy + 5, cx + 14, cy + 14, 3)), { base: hex("#55efc4"), lite: hex("#c8fff0"), puff: 5 }); }
};
