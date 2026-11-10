// coffee-nap v2: detailed, more realistic pixel art (adult proportions, textured room, anatomy, ball-and-stick molecules)
import { W, H, RGB, SDF, Mat, hex, mix, sat, lerp, hash, noise, fbm, put, addPx, rect, glow, paint, push, pop, circle, ell, rbox, capsule, blend, union, minus, toWorld, light } from "./gfx";
import { arc, Label } from "./art";
import { tri } from "./art7";

const flat = (c: string, a = 1): Mat => ({ base: hex(c), flat: true, line: null, rim: 0, alpha: a });
const shade = (base: string, lite: string, dark: string, puff = 8, extra: Partial<Mat> = {}): Mat => ({ base: hex(base), lite: hex(lite), dark: hex(dark), puff, ...extra });
const softShadow = (cx: number, cy: number, rx: number, ry: number, a: number, c = "#1a0e08") => {
  for (let y = Math.floor(cy - ry); y <= cy + ry; y++) for (let x = Math.floor(cx - rx); x <= cx + rx; x++) {
    const d = Math.hypot((x - cx) / rx, (y - cy) / ry); if (d < 1) put(x, y, hex(c), a * (1 - d * d));
  }
};
export const DESK = 356;
export const S = 1.35;   // person scale

// ======================= ROOM =======================
const WX0 = 62, WX1 = 208, WY0 = 132, WY1 = 258;
export const room = (f: number, sun: number) => {
  const rain = 1 - sun;
  // plaster wall: two-tone paint, soft noise, window light falloff, lamp warmth on the left
  for (let y = 0; y < DESK; y++) for (let x = 0; x < W; x++) {
    const n = fbm(x * 0.09, y * 0.09) * 0.06 + (hash(x, y) - 0.5) * 0.025;
    let c = mix(hex("#3c5560"), hex("#4f6c74"), y / DESK);
    if (y > 286) c = mix(hex("#5a6a5e"), hex("#4a5a50"), (y - 286) / 54);            // wainscot panel
    if (y === 286 || y === 287) c = hex("#8a9a88");
    const wl = sat(1 - Math.hypot((x - 135) / 170, (y - 200) / 150));                    // daylight from the window
    c = mix(c, mix(hex("#9ab0c0"), hex("#fff0c8"), sun), wl * (0.18 + 0.22 * sun));
    const ll = sat(1 - Math.hypot((x - 40) / 110, (y - 300) / 90));                     // lamp warmth
    c = mix(c, hex("#ffb060"), ll * ll * 0.35);
    put(x, y, [c[0] + n, c[1] + n, c[2] + n]);
  }
  for (let y = 292; y < 334; y += 0) { for (const x0 of [8, 92, 176]) { for (let x = x0; x < x0 + 80; x++) { put(x, 292, hex("#3a463e"), 0.5); put(x, 333, hex("#7a8a78"), 0.4); } for (let yy = 292; yy < 334; yy++) { put(x0, yy, hex("#3a463e"), 0.5); put(x0 + 79, yy, hex("#7a8a78"), 0.4); } } break; }
  // ---- outside the window: rainy city in three depth layers ----
  for (let y = WY0; y < WY1; y++) {
    const t = (y - WY0) / (WY1 - WY0);
    const c = mix(mix(hex("#6a7a8e"), hex("#a8b4c0"), t), mix(hex("#3a7ad8"), hex("#cfeaff"), t), sun);
    for (let x = WX0; x < WX1; x++) put(x, y, c);
  }
  if (sun > 0) { glow(184, 154, 46, hex("#fff2c0"), 0.7 * sun); paint(174, 144, 194, 164, circle(184, 154, 8), { ...flat("#fffbe0"), alpha: sun }); }
  for (let i = 0; i < 3; i++) {                                            // slow clouds
    const cx = ((i * 71 + f * 0.2) % 200) + WX0 - 20, cy = 146 + (i % 2) * 12;
    paint(cx - 30, cy - 14, cx + 30, cy + 10, blend(5, ell(cx, cy, 20, 6), circle(cx - 7, cy - 4, 7), circle(cx + 6, cy - 6, 8)),
      { base: mix(hex("#8a96a4"), hex("#ffffff"), sun), lite: mix(hex("#a8b2be"), hex("#ffffff"), sun), dark: mix(hex("#6a7684"), hex("#d0e0f0"), sun), puff: 7, rim: 0, line: null, alpha: 0.85 });
  }
  const layer = (seed: number, base: number, hmin: number, hmax: number, wmin: number, col: RGB, winC: RGB, winA: number, fogA: number) => {
    let x = WX0 - 6; let k = 0;
    while (x < WX1) {
      const w = wmin + Math.floor(hash(k, seed) * 14), h = hmin + Math.floor(hash(k, seed + 1) * (hmax - hmin)), top = base - h;
      for (let yy = Math.max(top, WY0); yy < Math.min(base, WY1); yy++) for (let xx = Math.max(x, WX0); xx < Math.min(x + w, WX1); xx++) {
        let c = col;
        if (xx === x || xx === x + 1) c = mix(col, hex("#000000"), 0.15);
        if (xx === x + w - 1) c = mix(col, hex("#ffffff"), 0.08 + 0.15 * sun);
        const wx = (xx - x - 3) % 5, wy = (yy - top - 4) % 6;
        if (xx > x + 2 && xx < x + w - 2 && yy > top + 3 && wx >= 0 && wx < 2 && wy >= 0 && wy < 3) {
          const on = hash(Math.floor((xx - x) / 5) + k * 7, Math.floor((yy - top) / 6) + seed) > 0.45;
          c = on ? mix(c, winC, winA) : mix(c, hex("#000000"), 0.2);
        }
        put(xx, yy, mix(c, mix(hex("#9aa6b4"), hex("#bfdcf2"), sun), fogA));
      }
      x += w + 1 + Math.floor(hash(k, seed + 2) * 4); k++;
    }
  };
  layer(11, WY1 - 34, 18, 60, 14, mix(hex("#5a6676"), hex("#7a9ab8"), sun), hex("#ffe0a0"), 0.5 * rain, 0.45);
  layer(23, WY1 - 10, 22, 70, 18, mix(hex("#3a4452"), hex("#5a7896"), sun), hex("#ffd27a"), 0.85 * rain + 0.2 * sun, 0.15);
  // rain streaks outside + drops sliding down the glass (refracted highlight)
  if (rain > 0) for (let i = 0; i < 80; i++) {
    const x0 = WX0 + hash(i, 1) * (WX1 - WX0), sp = 6 + hash(i, 2) * 3, y = WY0 + ((hash(i, 3) * 300 + f * sp) % (WY1 - WY0));
    for (let k = 0; k < 6; k++) put(x0 - k * 0.35, y - k, hex("#dce8f4"), 0.35 * rain * (1 - k / 6));
  }
  for (let i = 0; i < 14; i++) {
    const x = WX0 + 6 + hash(i, 7) * (WX1 - WX0 - 12), y = WY0 + ((hash(i, 8) * 140 + f * (0.25 + hash(i, 9) * 0.5)) % (WY1 - WY0 - 4));
    const r = 1 + Math.floor(hash(i, 10) * 2);
    for (let t = 1; t < 10; t++) put(x, y - t - r, hex("#c8d8e8"), 0.18 * rain * (1 - t / 10));
    for (let dy = -r; dy <= r; dy++) for (let dx = -r; dx <= r; dx++) if (dx * dx + dy * dy <= r * r) put(x + dx, y + dy, hex(dy > 0 ? "#5a6a7a" : "#e8f4ff"), 0.75 * rain);
    put(x - 1, y - 1, hex("#ffffff"), 0.9 * rain);
  }
  // ---- window frame with depth: inner reveal, sash bars, sill ----
  const frame = shade("#e6e2d8", "#ffffff", "#8a8678", 3);
  paint(WX0 - 10, WY0 - 10, WX1 + 10, WY1 + 4, minus(rbox(135, (WY0 + WY1) / 2 - 2, (WX1 - WX0) / 2 + 7, (WY1 - WY0) / 2 + 6, 1), rbox(135, (WY0 + WY1) / 2, (WX1 - WX0) / 2, (WY1 - WY0) / 2, 0)), frame);
  for (let y = WY0; y < WY1; y++) { put(WX0, y, hex("#5a5a50"), 0.6); put(WX0 + 1, y, hex("#5a5a50"), 0.3); }
  for (let x = WX0; x < WX1; x++) { put(x, WY0, hex("#5a5a50"), 0.6); put(x, WY0 + 1, hex("#5a5a50"), 0.3); }
  paint(132, WY0, 138, WY1, rbox(135, (WY0 + WY1) / 2, 2, (WY1 - WY0) / 2, 0), frame);
  paint(WX0, 192, WX1, 199, rbox(135, 195.5, (WX1 - WX0) / 2, 2, 0), frame);
  paint(WX0 - 16, WY1 - 2, WX1 + 16, WY1 + 10, rbox(135, WY1 + 4, (WX1 - WX0) / 2 + 13, 4, 1), shade("#f0ece2", "#ffffff", "#9a968a", 3));
  for (let x = WX0 - 12; x < WX1 + 12; x++) for (let y = WY1 + 9; y < WY1 + 14; y++) put(x, y, hex("#1a2428"), 0.35 * (1 - (y - WY1 - 9) / 5));
  // succulent pot on the sill
  softShadow(80, WY1 - 1, 10, 2, 0.4);
  paint(70, WY1 - 16, 90, WY1, minus(rbox(80, WY1 - 7, 8, 7, 2), rbox(80, WY1 - 15, 10, 1, 0)), shade("#c8643a", "#f0a070", "#6a2a14", 5));
  for (let i = 0; i < 7; i++) { const a = -Math.PI / 2 + (i - 3) * 0.42, lx = 80 + Math.cos(a) * 7, ly = WY1 - 15 + Math.sin(a) * 6;
    paint(lx - 6, ly - 6, lx + 6, ly + 6, ell(lx, ly, 2.4, 4.5), shade("#6aa86a", "#b0e0a0", "#2a5a3a", 3)); }
  // ---- curtains with folds ----
  const curtain = (x0: number, x1: number, side: number) => {
    for (let y = WY0 - 22; y < WY1 + 20; y++) {
      const tie = y > WY1 - 30 && y < WY1 - 22, pinch = y > WY1 - 40 ? 0.75 : 1;
      for (let x = x0; x < x1; x++) {
        const u = (x - x0) / (x1 - x0), ww = side < 0 ? u : 1 - u;
        if (ww > pinch && y > WY1 - 40) continue;
        const fold = Math.sin((x - x0) * 0.9 + Math.sin(y * 0.03) * 0.8), lt = 0.5 + 0.5 * fold;
        let c = mix(hex("#7a2e2a"), hex("#c8604a"), lt * 0.8);
        c = mix(c, hex("#ffd8a0"), sun * 0.12 * lt);
        if (tie) c = mix(hex("#d8b060"), hex("#8a6a2a"), 1 - lt);
        put(x, y, c);
      }
    }
  };
  curtain(30, WX0 + 4, -1); curtain(WX1 - 4, 240, 1);
  for (let x = 24; x < 246; x++) { put(x, WY0 - 24, hex("#3a3030")); put(x, WY0 - 23, hex("#7a6a60")); }   // rail
  // framed photo on the right wall
  paint(240, 172, 268, 206, rbox(254, 189, 12, 15, 1), shade("#2a2420", "#5a4a40", "#100c08", 3));
  for (let y = 177; y < 201; y++) for (let x = 246; x < 262; x++) put(x, y, mix(mix(hex("#f0b070"), hex("#5a8ab0"), (y - 177) / 24), hex("#3a6a3a"), y > 194 ? 0.7 : 0));
  // wall shadow cast by the window light around the person is added by the sitter
};

// ======================= DESK =======================
export const desk = (f: number, sun: number) => {
  // top face (seen slightly from above) with planks and grain
  for (let y = DESK - 6; y < DESK + 5; y++) for (let x = 0; x < W; x++) {
    const plank = Math.floor((x + 13) / 64), g = Math.sin(x * 0.18 + plank * 3 + noise(x * 0.05 + plank, y * 0.6) * 5);
    let c = mix(hex("#b8743e"), hex("#d89458"), 0.5 + 0.5 * g * 0.6);
    if ((x + 13) % 64 === 0) c = hex("#6a3a1e");
    c = mix(c, hex("#ffe0a8"), sat(1 - Math.abs(x - 135) / 140) * (0.08 + 0.12 * sun));
    put(x, y, c);
  }
  for (let x = 0; x < W; x++) { put(x, DESK + 5, hex("#f0b880")); put(x, DESK + 6, hex("#d08a50")); }
  for (let y = DESK + 7; y < DESK + 14; y++) for (let x = 0; x < W; x++) put(x, y, mix(hex("#a0602e"), hex("#6a3a1a"), (y - DESK - 7) / 7));
  // front: drawers, wood grain, handles
  for (let y = DESK + 14; y < H; y++) for (let x = 0; x < W; x++) {
    const g = Math.sin(y * 0.9 + noise(x * 0.02, y * 0.15) * 7) * 0.5 + 0.5;
    let c = mix(hex("#6a3c20"), hex("#82502c"), g * 0.6 + noise(x * 0.1, y * 0.4) * 0.3);
    c = mix(c, hex("#20100a"), sat((y - DESK - 14) / 160) * 0.5);
    put(x, y, c);
  }
  for (const [x0, x1] of [[16, 126], [144, 254]]) {
    for (let x = x0; x <= x1; x++) { put(x, DESK + 24, hex("#2a160c")); put(x, DESK + 25, hex("#a8703e"), 0.6); put(x, DESK + 88, hex("#a8703e"), 0.5); put(x, DESK + 87, hex("#2a160c")); }
    for (let y = DESK + 24; y < DESK + 88; y++) { put(x0, y, hex("#2a160c")); put(x0 + 1, y, hex("#a8703e"), 0.5); put(x1, y, hex("#a8703e"), 0.5); put(x1 - 1, y, hex("#2a160c")); }
    const hx = (x0 + x1) / 2;
    paint(hx - 12, DESK + 46, hx + 12, DESK + 58, union(capsule(hx - 8, DESK + 52, hx + 8, DESK + 52, 2), capsule(hx - 8, DESK + 49, hx - 8, DESK + 52, 1.4), capsule(hx + 8, DESK + 49, hx + 8, DESK + 52, 1.4)), shade("#c8b070", "#fff4c0", "#6a5420", 2));
  }
};

// desk props that sit on the top (drawn after the person's body, before the arms)
export const deskProps = (f: number, sun: number) => {
  // stack of books
  softShadow(40, DESK + 1, 26, 3, 0.45);
  const bk: [number, number, string, string][] = [[40, DESK - 4, "#2a5a8a", "#e8e0c8"], [38, DESK - 11, "#8a2a2a", "#f0e8d0"], [42, DESK - 17, "#3a6a3a", "#e8e0c8"]];
  for (const [x, y, c, p] of bk) {
    paint(x - 24, y - 5, x + 24, y + 5, rbox(x, y, 21, 3.4, 1), shade(c, "#ffffff", "#101018", 3, { tex: (px, py) => (px > x + 17 ? hex(p) : Math.abs(px - x + 12) < 1 ? hex("#e0c070") : null) }));
  }
  // desk lamp: weighted base, two arm segments with spring, cone shade, bulb
  softShadow(30, DESK, 14, 3, 0.5);
  const metal = shade("#2e3440", "#8a96a8", "#0c0e14", 4);
  paint(14, DESK - 8, 46, DESK + 2, ell(30, DESK - 3, 13, 4), metal);
  paint(22, DESK - 74, 52, DESK - 2, union(capsule(30, DESK - 5, 26, DESK - 50, 1.8), capsule(26, DESK - 50, 46, DESK - 70, 1.8)), metal);
  for (let i = 0; i < 6; i++) put(29 - i * 0.6, DESK - 14 - i * 5, hex("#c8c8d0"));
  paint(22, DESK - 54, 30, DESK - 46, circle(26, DESK - 50, 2.6), shade("#c8c8d0", "#ffffff", "#5a5a6a", 2));
  push(52, DESK - 66, 0.5, 1, 1);
  paint(-16, -12, 16, 16, (x, y) => Math.max(Math.max(ell(0, 4, 13, 10)(x, y), -y - 4), -ell(0, 10, 10, 4)(x, y) + Math.max(0, y - 9) * 100), shade("#d8a040", "#ffe8a0", "#7a4a10", 6));
  pop();
  glow(58, DESK - 52, 16, hex("#fff8d0"), 0.9);
  // light pool on the desk
  for (let y = DESK - 6; y < DESK + 6; y++) for (let x = 20; x < 120; x++) { const d = Math.hypot((x - 66) / 50, (y - DESK) / 6); if (d < 1) addPx(x, y, hex("#ffc070"), 0.18 * (1 - d)); }
  // phone face down + pen
  paint(96, DESK - 4, 122, DESK + 4, rbox(109, DESK, 11, 2.2, 1.5), shade("#1a1c22", "#6a7080", "#000000", 2));
  paint(150, DESK - 3, 180, DESK + 3, capsule(152, DESK + 1, 176, DESK - 1, 1.2), shade("#2a5ab8", "#9ac0ff", "#0a1a4a", 1));
};

// ======================= PERSON (adult proportions) =======================
const SKIN = shade("#e8b08a", "#ffd8b8", "#9a5a42", 8);
const HOOD = shade("#d8962e", "#ffcc6a", "#6a3a14", 10);
const JAW: SDF = blend(4, ell(0, -94, 15, 17), ell(0, -82, 10.5, 9));
export type Face = { eye: "open" | "half" | "closed" | "wide"; mouth: "smile" | "flat" | "o" | "grin" | "sleep"; blink?: boolean };
export type Sit = { face: Face; tilt: number; lift: number; hl: [number, number]; hr: [number, number]; er?: [number, number]; erw?: number; mug?: "r" | null; mugTilt?: number; steam?: number };

// put in the current local frame (the person is drawn scaled)
const lput = (x: number, y: number, c: RGB, a = 1) => {
  const [X, Y] = toWorld(x, y), [X2, Y2] = toWorld(x + 1, y + 1);
  for (let yy = Math.floor(Y); yy < Math.max(Math.floor(Y) + 1, Math.floor(Y2)); yy++) for (let xx = Math.floor(X); xx < Math.max(Math.floor(X) + 1, Math.floor(X2)); xx++) put(xx, yy, c, a);
};
const head = (F: Face) => {
  // ears
  for (const s of [-1, 1]) {
    paint(s * 15 - 4, -98, s * 15 + 4, -84, ell(s * 15, -91, 3, 5), SKIN);
    lput(s * 15, -91, hex("#9a5a42"), 0.6);
  }
  // back hair mass (behind the face)
  paint(-19, -116, 19, -86, ell(0, -101, 17, 15), shade("#3a2216", "#7a4a2a", "#120806", 10));
  // face
  paint(-17, -114, 17, -70, JAW, { ...SKIN, puff: 14, tex: (x, y) => {
    if (y > -79 && y < -76 && Math.abs(x) < 8) return null;                                              // under-lip shadow
    return null; } });
  for (const sd of [-1, 1]) for (let y = -89; y <= -81; y++) for (let x = 4; x <= 14; x++) { const bl = sat(1 - Math.hypot((x - 9) / 4.5, (y + 85) / 3)); if (bl > 0) lput(sd * x, y, hex("#e8706a"), 0.22 * bl); }
  // nose: shaded ridge + nostrils
  for (let y = -91; y <= -85; y++) { lput(2, y, SKIN.dark!, 0.25 + (y + 91) * 0.05); lput(0, y, SKIN.lite!, 0.25); }
  lput(-1, -84, hex("#9a5a42"), 0.7); lput(3, -84, hex("#9a5a42"), 0.7); lput(0, -83, hex("#c07a5a"), 0.5); lput(1, -83, hex("#c07a5a"), 0.5); lput(2, -83, hex("#c07a5a"), 0.5);
  // eyes + brows
  const ink = hex("#2a1810");
  for (const s of [-1, 1]) {
    const ex = s * 6.5, ey = -93;
    const shut = F.eye === "closed" || F.blink;
    // brow
    const by = F.eye === "wide" ? -100 : F.eye === "half" ? -97 : -98.5;
    for (let i = -3; i <= 3; i++) { lput(ex + i, by + (s * i > 1 ? 0.6 : 0) - (Math.abs(i) < 2 ? 0.4 : 0), hex("#2a160c")); lput(ex + i, by + 1, hex("#5a3a2a"), 0.4); }
    if (shut) { for (let i = -3; i <= 3; i++) lput(ex + i, ey + (Math.abs(i) === 3 ? 0 : 1), ink); lput(ex + s * 3, ey + 1, ink, 0.6); continue; }
    const big = F.eye === "wide" ? 1 : 0;
    for (let j = -1 - big; j <= 1; j++) for (let i = -3; i <= 3; i++) if ((i * i) / 10 + (j * j) / (j < 0 ? (1.4 + big) ** 2 : 1.6) <= 1) lput(ex + i, ey + j, hex("#f4ece4"));
    for (let j = -1 - big; j <= 1; j++) for (let i = -1; i <= 1; i++) lput(ex + i + s * 0.3, ey + j, hex(Math.abs(i) + Math.abs(j) < 2 ? "#3a2014" : "#6a3a1e"));
    lput(ex + s * 0.3 - 0.6, ey - 1 - big, hex("#ffffff"));
    for (let i = -3; i <= 3; i++) lput(ex + i, ey - 2 - big, ink);                                          // upper lash line
    if (F.eye === "half") for (let i = -3; i <= 3; i++) { lput(ex + i, ey - 1, SKIN.dark!, 1); lput(ex + i, ey - 2, SKIN.base, 1); lput(ex + i, ey, ink); }
    lput(ex + i3(s), ey + 2, hex("#c08a70"), 0.5);
  }
  // mouth
  const lip = hex("#a8584a"), dk = hex("#4a1a14");
  if (F.mouth === "smile") { for (let i = -4; i <= 4; i++) lput(i, -79 - (Math.abs(i) > 2 ? 1 : 0) + (Math.abs(i) < 2 ? 0.3 : 0), dk); for (let i = -2; i <= 2; i++) lput(i, -78, lip, 0.6); }
  if (F.mouth === "flat" || F.mouth === "sleep") { for (let i = -3; i <= 3; i++) lput(i, -79, dk, F.mouth === "sleep" ? 0.7 : 1); for (let i = -2; i <= 2; i++) lput(i, -78, lip, 0.5); }
  if (F.mouth === "o") paint(-4, -83, 4, -74, ell(0, -78.5, 2.4, 3), { base: dk, flat: true, line: lip, rim: 0 });
  if (F.mouth === "grin") paint(-7, -83, 7, -73, (x, y) => Math.max(ell(0, -80, 6, 4.5)(x, y), -81.5 - y), { base: dk, flat: true, line: lip, rim: 0, tex: (x, y) => (y < -79.5 ? hex("#f4f0e8") : y > -77.5 && Math.abs(x) < 3 ? hex("#c85a5a") : null) });
  // front hair: swept fringe with strands
  const fringe: SDF = (x, y) => Math.max(ell(0, -103, 17.5, 13.5)(x, y), y - (-100 + Math.max(0, (x + 4) * 0.25) - Math.max(0, -x - 6) * 0.4 + Math.sin(x * 0.9) * 1.2));
  paint(-20, -120, 20, -94, blend(3, fringe, ell(-14, -98, 4, 7), ell(14, -99, 3.5, 6)), shade("#4a2a18", "#9a6a40", "#140a06", 9, {
    tex: (x, y, d) => (d < -1 && Math.sin(x * 1.3 + y * 0.5) > 0.75 ? hex("#7a4e2e") : null) }));
};
const i3 = (s: number) => s * 0; // keep under-eye shading centred

const ik = (sx: number, sy: number, hx: number, hy: number, l1: number, l2: number, bend: number): [number, number] => {
  let dx = hx - sx, dy = hy - sy, d = Math.hypot(dx, dy);
  const mx = l1 + l2 - 0.5; if (d > mx) { dx = dx / d * mx; dy = dy / d * mx; d = mx; }
  const a = Math.acos(Math.max(-1, Math.min(1, (l1 * l1 + d * d - l2 * l2) / (2 * l1 * Math.max(d, 1e-3))))), b = Math.atan2(dy, dx) + bend * a;
  return [sx + Math.cos(b) * l1, sy + Math.sin(b) * l1];
};

export const sitterBody = (cx: number, P: Sit) => {
  // soft shadow of the person on the wall/window behind (light from the lamp, left)
  for (let y = DESK - 140; y < DESK; y++) for (let x = cx - 20; x < cx + 80; x++) { const d = Math.hypot((x - cx - 28) / 52, (y - DESK + 60) / 84); if (d < 1) put(x, y, hex("#10181c"), 0.18 * (1 - d)); }
  push(cx, DESK - P.lift, 0, S, S);
  // torso in a hoodie: shoulders, chest, folds, drawstrings, kangaroo-pocket seam
  const torso: SDF = blend(10, ell(0, -50, 37, 14), rbox(0, -22, 32, 30, 10));
  paint(-40, -66, 40, 12, torso, { ...HOOD, puff: 22, tex: (x, y, d) => {
    if (d < -1 && Math.abs(Math.abs(x) - 22 - Math.sin(y * 0.2) * 2) < 1 && y > -40) return mix(HOOD.base, HOOD.dark!, 0.35);   // side folds
    if (y > -16 && y < -14.6 && Math.abs(x) < 20) return mix(HOOD.base, HOOD.dark!, 0.45);                                      // pocket seam
    return null; } });
  // neck + shadow under the chin
  paint(-10, -80, 10, -56, rbox(0, -66, 8, 10, 3), { ...SKIN, puff: 5, tex: (x, y) => (y < -71 ? SKIN.dark! : null) });
  // hood bunched around the neck
  paint(-25, -72, 25, -50, minus(ell(0, -61, 22, 9), ell(0, -65, 9, 5)), { ...HOOD, base: hex("#c07e22"), puff: 6 });
  for (const s of [-1, 1]) { for (let t = 0; t < 16; t++) put(s * (5 + t * 0.05), -54 + t, hex("#f4ecd8")); paint(s * 5.8 - 2, -40, s * 5.8 + 2, -36, circle(s * 5.8, -38, 1.3), shade("#c8c0b0", "#ffffff", "#6a6458", 1)); }
  // head (tilts at the neck)
  push(0, -66, P.tilt, 1, 1); push(0, 66, 0, 1, 1);
  head(P.face);
  pop(); pop();
  pop();
};

export const sitterArms = (cx: number, P: Sit, f: number) => {
  push(cx, DESK - P.lift, 0, S, S);
  const arm = (s: number, h: [number, number], el?: [number, number]) => {
    const sx = s * 31, sy = -54, hx = h[0], hy = h[1] + P.lift;
    const k = ik(sx, sy, hx, hy, 30, 28, s > 0 ? 1 : -1), w = el ? (P.erw ?? 1) : 0, ex = el ? lerp(k[0], el[0], w) : k[0], ey = el ? lerp(k[1], el[1], w) : k[1];
    const x0 = Math.min(sx, ex, hx) - 12, x1 = Math.max(sx, ex, hx) + 12, y0 = Math.min(sy, ey, hy) - 12, y1 = Math.max(sy, ey, hy) + 12;
    paint(x0, y0, x1, y1, blend(4, capsule(sx, sy, ex, ey, 9, 7.5), capsule(ex, ey, hx, hy, 7.5, 6)), { ...HOOD, puff: 9,
      tex: (x, y, d) => (d < -1.5 && Math.hypot(x - ex, y - ey) < 5 && Math.sin((x - ex) * 1.2 + (y - ey)) > 0.6 ? mix(HOOD.base, HOOD.dark!, 0.4) : null) });
    // cuff + hand with finger hints
    const ax = hx - ex, ay = hy - ey, al = Math.hypot(ax, ay) || 1, ux = ax / al, uy = ay / al;
    paint(hx - 9, hy - 9, hx + 9, hy + 9, capsule(hx - ux * 3, hy - uy * 3, hx - ux * 1, hy - uy * 1, 6.5), { ...HOOD, base: hex("#c07e22"), puff: 3 });
    const px = hx + ux * 4, py = hy + uy * 4;
    paint(px - 8, py - 8, px + 8, py + 8, blend(2, ell(px, py, 4.6, 4.2), capsule(px, py, px + ux * 4 - s * uy * 2, py + uy * 4 + s * ux * 2, 2.2)), { ...SKIN, puff: 4,
      tex: (x, y, d) => (d < -1 && Math.abs((x - px) * uy - (y - py) * ux) < 0.5 && (x - px) * ux + (y - py) * uy > 0 ? SKIN.dark! : null) });
    return [px, py];
  };
  arm(-1, P.hl);
  const [rx, ry] = arm(1, P.hr, P.er);
  if (P.mug === "r") { const [X, Y] = toWorld(rx - 1, ry - 3); pop(); mug(X, Y, P.mugTilt ?? 0, P.steam ?? 1, f, false, S); return; }
  pop();
};

// ======================= MUG =======================
export const mug = (x: number, y: number, tilt: number, steam: number, f: number, onDesk = true, sc = S) => {
  if (onDesk) softShadow(x + 2, y + 9.5 * sc, 11 * sc, 2.5, 0.5);
  push(x, y, tilt, sc, sc);
  const cer = shade("#e8e0d4", "#ffffff", "#8a7e70", 8, { tex: (px, py, d) => (d < -1 && px > -6 && px < -4 && py < 6 ? hex("#ffffff") : py > 1 && py < 4 ? hex("#2a7a8a") : null) });
  paint(3, -8, 16, 7, minus(ell(9, -0.5, 5.5, 6), ell(9, -0.5, 2.6, 3.4)), shade("#e8e0d4", "#ffffff", "#8a7e70", 3));
  paint(-11, -11, 9, 11, (px, py) => Math.max(rbox(-1, 0, 8.5, 9.5, 1.5)(px, py), -ell(-1, -9.5, 8.5, 2.2)(px, py) - (py < -9.5 ? 0 : 99)), cer);
  paint(-10, -12, 8, -7, ell(-1, -9.5, 7.5, 1.9), { base: hex("#4a2412"), flat: true, line: hex("#f4f0e8"), rim: 0, tex: (px, py) => (px < -4 && py < -10 ? hex("#a8683a") : null) });
  pop();
  if (steam > 0) for (let k = 0; k < 3; k++) for (let i = 0; i < 22; i++) {
    const u = ((i / 22 + f * 0.015 + k * 0.33) % 1), sx = x - 4 + k * 4 + Math.sin(u * 6 + f * 0.08 + k * 2) * (1.5 + u * 3), sy = y - 13 * sc - u * 30;
    put(sx, sy, hex("#ffffff"), 0.35 * steam * Math.sin(Math.PI * u)); put(sx + 1, sy, hex("#ffffff"), 0.15 * steam * Math.sin(Math.PI * u));
  }
};

// ======================= ALARM CLOCK (chrome bells, enamel body) =======================
export const alarm = (x: number, f: number, ring: number, L: Label[]) => {
  const sh = ring > 0 ? Math.sin(f * 2.3) * 1.6 * ring : 0, y = DESK - 15, rot = ring > 0 ? Math.sin(f * 1.7) * 0.1 * ring : 0;
  softShadow(x, DESK + 1, 14, 2.5, 0.5);
  push(x + sh, y, rot, 1, 1);
  const chrome = shade("#b8c0c8", "#ffffff", "#3a4048", 6, { tex: (px, py, d, lam) => (lam > 0.8 ? hex("#ffffff") : lam < 0.25 ? hex("#2a3038") : null) });
  const enamel = shade("#b8302a", "#ff8a7a", "#4a0a0a", 8);
  for (const s of [-1, 1]) paint(s * 9 - 7, -21, s * 9 + 7, -7, (px, py) => Math.max(circle(s * 9, -11, 6)(px, py), py + 11), chrome);
  paint(-6, -19, 6, -11, capsule(-4, -15, 4, -15, 1.1), chrome);
  paint(-2, -22, 2, -15, capsule(0, -20, 0, -15, 1), chrome);
  for (const s of [-1, 1]) paint(s * 8 - 4, 6, s * 8 + 4, 16, capsule(s * 6, 9, s * 9, 14, 1.6), chrome);
  paint(-15, -15, 15, 15, circle(0, 0, 12.5), enamel);
  paint(-12, -12, 12, 12, circle(0, 0, 10), { base: hex("#fbf6ea"), lite: hex("#ffffff"), dark: hex("#c8bea8"), puff: 7, rim: 0, line: hex("#6a6a6a") });
  for (let k = 0; k < 12; k++) { const a = k * Math.PI / 6; const [px, py] = toWorld(Math.cos(a) * 8, Math.sin(a) * 8); put(px, py, hex("#3a3a3a"), k % 3 ? 0.5 : 1); }
  paint(-3, -9, 3, 3, capsule(0, 0, -2, -6, 0.8), flat("#1a1a22"));
  paint(-3, -3, 9, 3, capsule(0, 0, 6, 1, 0.8), flat("#1a1a22"));
  paint(-2, -8, 2, 8, capsule(0, 2, 0, -7, 0.4), flat("#d82a2a"));
  for (let i = 0; i < 4; i++) { const [px, py] = toWorld(-6 + i, -7 + i); put(px, py, hex("#ffffff"), 0.55); }   // glass glint
  pop();
  if (ring > 0) {
    for (const s of [-1, 1]) for (let k = 0; k < 2; k++) {
      const r = 18 + k * 6 + ((f * 0.5) % 6);
      for (let a = -0.6; a <= 0.6; a += 0.05) put(x + s * Math.cos(a) * r, y - 8 + Math.sin(a) * r, hex("#ffe14e"), 0.9 * ring);
    }
    L.push({ s: "RING!", x: x - 34, y: y - 48 + Math.round(Math.sin(f * 0.8) * 2), c: "#ffe14e", size: 16 });
  }
};

// energy battery overlay (UI)
export const battery = (x: number, y: number, lvl: number, a: number, L: Label[]) => {
  if (a <= 0) return;
  paint(x - 14, y - 34, x + 14, y + 34, minus(rbox(x, y + 2, 12, 30, 3), rbox(x, y + 2, 9, 27, 1)), { base: hex("#f2f2f2"), lite: hex("#ffffff"), dark: hex("#8a8a9a"), puff: 3, alpha: a });
  paint(x - 6, y - 34, x + 6, y - 26, rbox(x, y - 30, 5, 3, 1), { base: hex("#f2f2f2"), puff: 2, alpha: a });
  const c = lvl < 0.34 ? hex("#ff4a4a") : lvl < 0.67 ? hex("#ffd84a") : hex("#55efc4"), n = Math.max(1, Math.round(lvl * 5));
  for (let i = 0; i < n; i++) rect(x - 7, y + 24 - i * 10.5, 14, 8, c, a);
  if (a > 0.5) L.push({ s: "ENERGY", x: x - 17, y: y + 38, c: lvl > 0.67 ? "#55efc4" : "#ff6a6a", size: 16 });
};

// ======================= ANATOMY VIEW =======================
export const PATH: [number, number][] = [[152, 376], [146, 352], [142, 326], [136, 300], [127, 278], [126, 256], [132, 236]];
export const along = (u: number): [number, number] => {
  const seg = PATH.length - 1, t = Math.min(seg - 1e-6, Math.max(0, u * seg)), k = Math.floor(t), r = t - k;
  return [lerp(PATH[k][0], PATH[k + 1][0], r), lerp(PATH[k][1], PATH[k + 1][1], r)];
};
const BODY: SDF = blend(6,
  ell(135, 226, 20, 25), rbox(135, 260, 8, 12, 4),
  blend(14, ell(135, 290, 58, 16), rbox(135, 360, 44, 72, 22)), ell(135, 440, 50, 34),
  capsule(80, 292, 70, 380, 10, 8), capsule(70, 380, 64, 452, 8, 6.5), capsule(190, 292, 200, 380, 10, 8), capsule(200, 380, 206, 452, 8, 6.5));
export const anatomy = (f: number, kick: number) => {
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const v = Math.hypot((x - 135) / 190, (y - 320) / 260), scan = (y + Math.floor(f * 0.7)) % 3 === 0 ? 0.03 : 0;
    put(x, y, mix(mix(hex("#122830"), hex("#04090c"), sat(v)), hex("#5ad8e6"), scan));
  }
  // body: translucent skin with glowing contour
  for (let y = 180; y < H; y++) for (let x = 0; x < W; x++) {
    const d = BODY(x + 0.5, y + 0.5);
    if (d < 0) put(x, y, mix(hex("#1e3a44"), hex("#2a5260"), sat(-d / 20)), 0.85);
    if (d > -1.6 && d < 1.2) put(x, y, hex("#9ef0f8"), 0.9 - Math.abs(d) * 0.4);
    else if (d >= 1.2 && d < 6) put(x, y, hex("#5ad8e6"), 0.12 * (1 - d / 6));
  }
  // skeleton hints: spine + ribs + clavicles
  for (let y = 268; y < 420; y += 6) paint(129, y - 3, 141, y + 3, rbox(135, y, 4.5, 2, 1), { base: hex("#c8d8d8"), lite: hex("#ffffff"), dark: hex("#5a7a80"), puff: 2, rim: 0, line: null, alpha: 0.45 });
  for (let i = 0; i < 6; i++) { const y = 296 + i * 10; for (const s of [-1, 1]) for (let t = 0; t <= 1; t += 0.02) { const xx = 135 + s * (6 + Math.sin(t * Math.PI * 0.8) * (34 - i * 1.5)), yy = y + t * 14 - Math.sin(t * Math.PI) * 4; put(xx, yy, hex("#c8d8d8"), 0.28); } }
  for (const s of [-1, 1]) for (let t = 0; t <= 1; t += 0.02) put(135 + s * (6 + t * 40), 284 - Math.sin(t * Math.PI) * 3, hex("#d8e8e8"), 0.45);
  // lungs
  for (const s of [-1, 1]) paint(135 + s * 40 - 24, 288, 135 + s * 40 + 24, 356, blend(6, ell(135 + s * 22, 322, 16, 30), ell(135 + s * 26, 340, 14, 14)),
    { base: hex("#c86a7a"), lite: hex("#ffb0b8"), dark: hex("#5a2030"), puff: 14, rim: 0, line: null, alpha: 0.5 });
  // liver (viewer's left) and stomach (viewer's right)
  paint(96, 352, 150, 386, blend(6, ell(118, 366, 22, 11), ell(134, 370, 12, 8)), { base: hex("#7a2a24"), lite: hex("#c85a4a"), dark: hex("#3a0a08"), puff: 10, rim: 0, alpha: 0.85 });
  const stom: SDF = blend(7, ell(156, 372, 13, 10), capsule(146, 354, 152, 366, 5), ell(146, 382, 10, 6));
  paint(130, 346, 174, 394, stom, { base: hex("#e8909a"), lite: hex("#ffd0d4"), dark: hex("#8a3a4a"), puff: 9, rim: 0,
    tex: (x, y) => (y > 374 + Math.sin(x * 0.5 + f * 0.15) * 1.2 && stom(x, y) < -1.5 ? mix(hex("#5a2e14"), hex("#8a4a20"), 0.5 + 0.5 * Math.sin(x + f * 0.2)) : null) });
  // esophagus from the throat to the stomach
  for (let t = 0; t <= 1; t += 0.005) { const x = lerp(135, 146, t * t), y = lerp(262, 352, t); put(x, y, hex("#d87a84"), 0.75); put(x + 1, y, hex("#a84a5a"), 0.6); }
  // heart + arteries (carotid up to the brain, branches to the arms)
  paint(128, 308, 160, 336, blend(4, circle(140, 318, 7), circle(150, 318, 7), tri(133, 320, 157, 320, 146, 334)), { base: hex("#c8202a"), lite: hex("#ff7a7a"), dark: hex("#5a0a10"), puff: 7 });
  const beat = 1 + 0.35 * Math.max(0, Math.sin(f * 0.42)) ** 6;
  glow(145, 322, 16 * beat, hex("#ff3a3a"), 0.25);
  const vessel = (pts: [number, number][], c: string, a: number) => { for (let k = 0; k < pts.length - 1; k++) for (let t = 0; t <= 1; t += 0.03) put(lerp(pts[k][0], pts[k + 1][0], t), lerp(pts[k][1], pts[k + 1][1], t), hex(c), a); };
  vessel(PATH, "#ff4a4a", 0.9);
  vessel([[142, 326], [148, 300], [144, 278], [144, 256], [138, 236]], "#ff4a4a", 0.7);
  vessel([[140, 300], [110, 292], [84, 296], [74, 360], [68, 440]], "#e83a3a", 0.5);
  vessel([[148, 300], [160, 292], [186, 296], [196, 360], [202, 440]], "#e83a3a", 0.5);
  vessel([[140, 330], [138, 400], [118, 446]], "#e83a3a", 0.5); vessel([[140, 400], [152, 446]], "#e83a3a", 0.5);
  vessel([[130, 330], [128, 410]], "#4a6aff", 0.45);
  // brain: two hemispheres with gyri, cerebellum hint
  const bc = mix(hex("#e8a8b0"), hex("#ffe08a"), kick);
  const brain: SDF = blend(3, ell(128, 222, 11, 13), ell(142, 222, 11, 13));
  paint(112, 204, 158, 242, brain, { base: bc, lite: mix(bc, hex("#ffffff"), 0.5), dark: mix(bc, hex("#5a1a2a"), 0.6), puff: 9,
    tex: (x, y, d) => {
      if (Math.abs(x - 135) < 0.6 && d < -1) return mix(bc, hex("#3a0a1a"), 0.6);
      const g = Math.sin((x - 135) * 0.9 + Math.sin((y - 222) * 0.7) * 2.2) * Math.cos((y - 222) * 0.8 + Math.sin(x * 0.5));
      return d < -1 && Math.abs(g) < 0.12 ? mix(bc, hex("#7a2a3a"), 0.5) : null; } });
  if (kick > 0) glow(135, 222, 56, hex("#ffe14e"), 0.6 * kick);
};
export const caffeineDot = (x: number, y: number, a = 1) => {
  glow(x, y, 6, hex("#ffc84a"), 0.6 * a);
  paint(x - 3, y - 3, x + 3, y + 3, circle(x, y, 2), { base: hex("#ffd84a"), lite: hex("#ffffff"), dark: hex("#c87a1a"), puff: 2, rim: 0, line: null, alpha: a });
};

// ======================= SYNAPSE =======================
export const MEM = 344;
export const RX = [44, 106, 166, 228];
export const RECV = (x: number, f: number) => MEM - 24 + Math.sin(x * 0.05 + f * 0.04) * 2;
const lipidTop = (x: number, f: number) => MEM + Math.sin(x * 0.05 + f * 0.04) * 2;
export const synapse = (f: number, lit: number) => {
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const n = fbm(x * 0.03 + f * 0.003, y * 0.03);
    put(x, y, mix(mix(hex("#1a0e2e"), hex("#3a1a48"), n), hex("#ff9a3a"), lit * 0.14 * sat(1 - Math.abs(y - MEM) / 140)));
  }
  // presynaptic terminal (the sending nerve ending) bulging down from the top
  const term: SDF = ell(135, 110, 168, 130);
  for (let y = 0; y < 250; y++) for (let x = 0; x < W; x++) {
    const d = term(x + 0.5, y + 0.5);
    if (d < -4) put(x, y, mix(hex("#5a3a6a"), hex("#3a2450"), fbm(x * 0.05, y * 0.05)), 0.9);
    else if (d < -2.5) put(x, y, hex("#f0c8e8"), 0.9); else if (d < -1.5) put(x, y, hex("#8a5a9a"), 0.9); else if (d < 0) put(x, y, hex("#f0c8e8"), 0.9);
  }
  // synaptic vesicles + a mitochondrion inside the terminal
  for (let i = 0; i < 16; i++) {
    const vx = 22 + hash(i, 5) * 226, vy = 168 + hash(i, 6) * 60 + Math.sin(f * 0.05 + i) * 1.5, r = 5 + hash(i, 7) * 3;
    if (term(vx, vy) > -r - 4) continue;
    paint(vx - r - 1, vy - r - 1, vx + r + 1, vy + r + 1, minus(circle(vx, vy, r), circle(vx, vy, r - 1.6)), { base: hex("#f0c8e8"), lite: hex("#ffffff"), dark: hex("#9a6aa8"), puff: 2, rim: 0, line: hex("#5a3a6a") });
    paint(vx - r, vy - r, vx + r, vy + r, circle(vx, vy, r - 2), { base: hex("#7a4a8a"), lite: hex("#a87ab8"), puff: r, rim: 0, line: null, alpha: 0.7 });
  }
  paint(150, 150, 236, 186, ell(194, 168, 34, 11), { base: hex("#c8604a"), lite: hex("#ffa080"), dark: hex("#5a1a14"), puff: 8,
    tex: (x, y, d) => (d < -2 && Math.abs(Math.sin((x - 194) * 0.45)) < 0.25 ? hex("#ffd0b0") : null) });
  // drifting particles in the cleft
  for (let i = 0; i < 18; i++) { const x = (hash(i, 1) * 300 + f * (0.2 + hash(i, 2) * 0.3)) % 280 - 5, y = 250 + hash(i, 3) * 70 + Math.sin(f * 0.06 + i) * 3; put(x, y, hex("#c8a8e8"), 0.5); }
  // postsynaptic membrane: lipid bilayer (heads + tails)
  for (let x = 0; x < W; x++) {
    const t = lipidTop(x, f);
    for (let y = Math.floor(t); y < H; y++) {
      const d = y - t;
      let c: RGB;
      if (d < 3) c = mix(hex("#ffd8f0"), hex("#e898d0"), ((x % 4) + 0.5) / 4);
      else if (d < 13) c = mix(hex("#f4e8b0"), hex("#c8b070"), ((x + Math.floor(d)) % 3 === 0 ? 0.6 : 0.1));
      else if (d < 16) c = mix(hex("#ffd8f0"), hex("#e898d0"), ((x % 4) + 0.5) / 4);
      else c = mix(hex("#7a3a7a"), hex("#2a0e30"), sat((d - 16) / 120));
      put(x, y, c);
    }
    if (x % 4 === 1) { put(x, t, hex("#ffffff"), 0.7); put(x, t + 14, hex("#ffffff"), 0.4); }
  }
  // adenosine receptors: 7-helix bundles spanning the membrane with a binding pocket on top
  for (const x of RX) {
    const t = lipidTop(x, f);
    const col = mix(hex("#3ab8c8"), hex("#ffb84a"), lit), lite = mix(hex("#a8f4ff"), hex("#fff0b0"), lit), dk = mix(hex("#0a3a5a"), hex("#7a3a0a"), lit);
    for (let k = -3; k <= 3; k++) {
      const hx = x + k * 3.2, top = t - 14 + Math.abs(k) * 2.2 - (Math.abs(k) === 0 ? -6 : 0);
      paint(hx - 3, top - 2, hx + 3, t + 22, capsule(hx, top, hx + Math.sin(k) * 0.8, t + 20, 2.1), { base: col, lite, dark: dk, puff: 2, tex: (px, py) => (Math.sin(py * 1.4 + k) > 0.7 ? lite : null) });
    }
    if (lit > 0) glow(x, t - 12, 22, hex("#ffb84a"), 0.45 * lit);
  }
};

// ---- ball-and-stick molecules (2-D projection of the real atom layout) ----
type Atom = [number, number, "C" | "N" | "O" | "H"];
const B5 = 5.2;
const ring6 = [...Array(6)].map((_, k) => [Math.cos((-90 + 60 * k) * Math.PI / 180) * B5, Math.sin((-90 + 60 * k) * Math.PI / 180) * B5] as [number, number]);
const pc: [number, number] = [ring6[1][0] + B5 / (2 * Math.tan(Math.PI / 5)), 0], R5 = B5 / (2 * Math.sin(Math.PI / 5));
const pent = (deg: number): [number, number] => [pc[0] + Math.cos(deg * Math.PI / 180) * R5, pc[1] + Math.sin(deg * Math.PI / 180) * R5];
const out = (p: [number, number], c: [number, number], k = 1): [number, number] => { const dx = p[0] - c[0], dy = p[1] - c[1], l = Math.hypot(dx, dy); return [p[0] + dx / l * B5 * k, p[1] + dy / l * B5 * k]; };
// purine core: C6 N1 C2 N3 C4 C5 (six-ring), N7 C8 N9 (five-ring)
const C6 = ring6[0], N1 = ring6[5], C2 = ring6[4], N3 = ring6[3], C4 = ring6[2], C5 = ring6[1], N7 = pent(-72), C8 = pent(0), N9 = pent(72);
const core: Atom[] = [[...C6, "C"], [...N1, "N"], [...C2, "C"], [...N3, "N"], [...C4, "C"], [...C5, "C"], [...N7, "N"], [...C8, "C"], [...N9, "N"]];
const coreB: [number, number][] = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 0], [5, 6], [6, 7], [7, 8], [8, 4]];
const O0: [number, number] = [0, 0];
const centre = (atoms: Atom[]) => { const mx = atoms.reduce((s, a) => s + a[0], 0) / atoms.length, my = atoms.reduce((s, a) => s + a[1], 0) / atoms.length; return atoms.map(a => [a[0] - mx, a[1] - my, a[2]] as Atom); };
// caffeine: 1,3,7-trimethylxanthine (O on C2 and C6, CH3 on N1, N3, N7)
const CAF = (() => {
  const a: Atom[] = [...core], b = [...coreB];
  const add = (p: [number, number], el: Atom[2], to: number) => { a.push([...p, el]); b.push([to, a.length - 1]); return a.length - 1; };
  add(out(C6, O0), "O", 0); add(out(C2, O0), "O", 2);
  for (const [p, idx, c] of [[N1, 1, O0], [N3, 3, O0], [N7, 6, pc]] as [[number, number], number, [number, number]][]) {
    const m = out(p, c); const mi = add(m, "C", idx);
    const dir = [m[0] - p[0], m[1] - p[1]];
    add([m[0] + dir[0] * 0.55 - dir[1] * 0.35, m[1] + dir[1] * 0.55 + dir[0] * 0.35], "H", mi);
    add([m[0] + dir[0] * 0.55 + dir[1] * 0.35, m[1] + dir[1] * 0.55 - dir[0] * 0.35], "H", mi);
  }
  return { atoms: centre(a), bonds: b };
})();
// adenosine: adenine (NH2 on C6) + ribose on N9
const ADE = (() => {
  const a: Atom[] = [...core], b = [...coreB];
  const add = (p: [number, number], el: Atom[2], to: number) => { a.push([...p, el]); b.push([to, a.length - 1]); return a.length - 1; };
  const n6 = out(C6, O0); const ni = add(n6, "N", 0);
  add([n6[0] - 3, n6[1] - 3], "H", ni); add([n6[0] + 3, n6[1] - 3], "H", ni);
  const c1 = out(N9, pc); const c1i = add(c1, "C", 8);
  const u = [(c1[0] - N9[0]) / B5, (c1[1] - N9[1]) / B5], rc: [number, number] = [c1[0] + u[0] * R5, c1[1] + u[1] * R5];
  const a0 = Math.atan2(c1[1] - rc[1], c1[0] - rc[0]), rv = [1, 2, 3, 4].map(j => [rc[0] + Math.cos(a0 + j * 1.2566) * R5, rc[1] + Math.sin(a0 + j * 1.2566) * R5] as [number, number]);
  const c2 = add(rv[0], "C", c1i), c3 = add(rv[1], "C", c2), c4 = add(rv[2], "C", c3), o4 = add(rv[3], "O", c4); b.push([o4, c1i]);
  add(out(rv[0], rc, 0.9), "O", c2); add(out(rv[1], rc, 0.9), "O", c3);
  const c5 = out(rv[2], rc); const c5i = add(c5, "C", c4); add(out(c5, rv[2], 0.9), "O", c5i);
  return { atoms: centre(a), bonds: b };
})();
const EL: Record<string, [string, string, string, number]> = { C: ["#4a525a", "#a0aab4", "#14181c", 2.5], N: ["#3a5ae8", "#a8b8ff", "#0a1a5a", 2.5], O: ["#e8302a", "#ffa898", "#5a0a08", 2.5], H: ["#e8e8ee", "#ffffff", "#8a8a9a", 1.5] };
export const molecule = (kind: "aden" | "caf", x: number, y: number, rot: number, a = 1, s = 1) => {
  const M = kind === "caf" ? CAF : ADE, co = Math.cos(rot), si = Math.sin(rot);
  const P = M.atoms.map(([ax, ay, el]) => [x + (ax * co - ay * si) * s, y + (ax * si + ay * co) * s, el] as Atom);
  for (const [i, j] of M.bonds) { const p = P[i], q = P[j];
    paint(Math.min(p[0], q[0]) - 3, Math.min(p[1], q[1]) - 3, Math.max(p[0], q[0]) + 3, Math.max(p[1], q[1]) + 3, capsule(p[0], p[1], q[0], q[1], 0.9 * s), { base: hex("#c8c8d0"), lite: hex("#ffffff"), dark: hex("#5a5a6a"), puff: 1, rim: 0, line: null, alpha: a }); }
  for (const p of P) { const [b, l, d, r] = EL[p[2]];
    paint(p[0] - r * s - 2, p[1] - r * s - 2, p[0] + r * s + 2, p[1] + r * s + 2, circle(p[0], p[1], r * s), { base: hex(b), lite: hex(l), dark: hex(d), puff: r * s, rim: 0.4, line: hex("#0a0610"), alpha: a }); }
};
