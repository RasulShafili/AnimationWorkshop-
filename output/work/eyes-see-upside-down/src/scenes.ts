import { W, H, RGB, hex, mix, sat, lerp, sstep, easeOut, easeInOut, backOut, hash, bayer, makeFB, target, quantize, textBlock, glyphRun, rect, put, glow, light, push, pop, darken, Line } from "./gfx";
import { Label, tod, room, rug, hero, sparkle } from "./art";
import { tree, eyeSection, rays, brainChar, picture, goggles, calendar } from "./art4";
import timing from "./timing.json";

const B = timing.beats, ON = timing.gogglesOn, OFF = timing.gogglesOff;
const fbA = makeFB(), fbB = makeFB();
type Txt = [string, string][][];
export const BEATS: Line[][] = (timing.texts as unknown as Txt).map(lines => lines.map(segs => ({ segs: segs.map(([t, c]) => (c ? { t, c } : { t })) })));
const PI = Math.PI, HX = 128, FEET = 372, HEADY = FEET - 146;
const blink = (f: number) => (f + 40) % 97 < 4;
type Out = { rot: number; ui: number; post?: () => void };

const bedroom = (f: number, L: Label[], t = 0.3) => { const k = tod(t); room(k, f, L); rug(HX, 384, k); return k; };
const navy = (cx = 135, cy = 280) => {
  light.tint = [1, 1, 1]; light.rim = hex("#8fd8ff"); light.rimAmt = 0.8;
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) put(x, y, mix(hex("#16206a"), hex("#05061e"), sat(Math.hypot((x - cx) / 200, (y - cy) / 260))));
};

const s1 = (f: number, L: Label[]): Out => {
  bedroom(f, L);
  hero(HX, FEET, 1, { armL: 0.2, armR: 2.5 + Math.sin(f * 0.35) * 0.25 }, { eye: "open", mouth: "grin", blink: blink(f) });
  return { rot: lerp(0.9 * PI, PI, backOut(f / 24)) + Math.sin(f * 0.06) * 0.015, ui: L.length };
};

const s2 = (f: number, L: Label[]): Out => {
  navy(160, 300);
  const l = f - B[1];
  tree(44, 332, 1.0);
  const e = eyeSection(186, 300, 64, 1, f);
  const up = sat((l - 8) / 56);
  rays(44, 268, 330, e.lensX, e.lensY, e.retinaX, e.lensY, 36, up);
  if (up >= 1) { push(e.retinaX - 9, e.lensY, PI, 0.5, 0.5); tree(0, 34, 1, sat((l - 64) / 10)); pop(); glow(e.retinaX - 9, e.lensY, 22, hex("#ffe600"), 0.4); }
  const ui = L.length;
  if (l > 20) L.push({ s: "LENS", x: e.lensX - 14, y: 352, c: "#5ce1e6" });
  if (l > 66) L.push({ s: "RETINA", x: 200, y: 240, c: "#ff8aa0" });
  return { rot: 0, ui };
};

const s3 = (f: number, L: Label[]): Out => {
  const l = f - B[2];
  light.tint = [1, 1, 1]; light.rimAmt = 0.4;
  // the back wall of the eye: a carpet of rods and cones
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const cx = (x % 9), cy = (y + (Math.floor(x / 9) % 2) * 5) % 10;
    const rod = Math.hypot(cx - 4, cy - 5) < 3.4;
    let c = mix(hex("#4a0a2a"), hex("#1a0418"), sat(Math.hypot((x - 135) / 200, (y - 280) / 260)));
    if (rod) c = mix(c, hex("#ff7a9a"), 0.35 + 0.2 * Math.sin(f * 0.1 + x * 0.3 + y * 0.2));
    put(x, y, c);
  }
  const a = sstep(4, 24, l);
  glow(135, 290, 120, hex("#ffe600"), 0.35 * a);
  push(135, 266, PI + Math.sin(f * 0.04) * 0.03, 2.3, 2.3); tree(0, -10, 1, a); pop();
  return { rot: 0, ui: L.length };
};

const s4 = (f: number, L: Label[]): Out => {
  navy(135, 300);
  const l = f - B[3], turn = easeInOut((l - 22) / 34);
  brainChar(135, 330, 1.25, turn > 0.05 && turn < 0.95 ? "focus" : "happy", f);
  picture(135, 208, PI * (1 - turn), 1.15);
  if (turn > 0.95 && l < 80) for (let i = 0; i < 8; i++) { const ang = i / 8 * PI * 2 + l * 0.05, r = 54 + (l - 56) * 1.5; sparkle(135 + Math.cos(ang) * r, 208 + Math.sin(ang) * r * 0.8, 2, hex("#ffe600"), sat(1 - (l - 56) / 24)); }
  // curved arrows around the frame while it spins
  if (turn > 0 && turn < 1) for (let i = 0; i < 24; i++) { const ang = -PI * 0.9 + i * 0.07 + turn * PI; put(135 + Math.cos(ang) * 56, 208 + Math.sin(ang) * 46, hex("#55efc4"), 0.9); put(135 - Math.cos(ang) * 56, 208 - Math.sin(ang) * 46, hex("#55efc4"), 0.9); }
  return { rot: 0, ui: L.length };
};

const heroG = (f: number, L: Label[], face: { eye: "open" | "wide" | "closed"; mouth: "smile" | "grin" | "o" | "flat" }, pose = { armL: 0.2, armR: 0.2 }, gy: number | null = HEADY + 1) => {
  hero(HX, FEET, 1, pose, { ...face, blink: false });
  if (gy !== null) goggles(HX, gy);
};

const s5 = (f: number, L: Label[]): Out => {
  bedroom(f, L);
  const t = f - ON, gy = t < 0 ? HEADY - 120 + 0 * t : HEADY + 1 - Math.abs(Math.sin(t * 0.5)) * 10 * Math.exp(-t * 0.18);
  const drop = t < 0 ? lerp(HEADY - 130, HEADY + 1, easeInOut((f - B[4]) / 20)) : gy;
  heroG(f, L, { eye: "open", mouth: t > 0 ? "o" : "smile" }, { armL: 0.2, armR: 0.2 }, drop);
  return { rot: 0, ui: L.length };
};

const s6 = (f: number, L: Label[]): Out => {
  const l = f - B[5];
  bedroom(f, L);
  const wob = Math.sin(l * 0.3) * 0.25;
  heroG(f, L, { eye: "open", mouth: "o" }, { armL: 1.1 + wob, armR: 0.6 - wob });
  // sweat drops
  for (let i = 0; i < 2; i++) { const t = ((l + i * 20) % 40) / 40; put(HX + 36, HEADY - 18 + t * 24, hex("#8ad8ff")); put(HX + 36, HEADY - 17 + t * 24, hex("#8ad8ff")); }
  return { rot: PI + Math.sin(l * 0.11) * 0.05, ui: L.length };
};

const s7 = (f: number, L: Label[]): Out => {
  const l = f - B[6], p = easeInOut((l - 8) / 84);
  bedroom(f, L);
  heroG(f, L, { eye: "open", mouth: p > 0.9 ? "grin" : "flat" }, { armL: 0.2, armR: p > 0.9 ? 2.4 : 0.2 });
  const ui = L.length;
  return { rot: PI * (1 - p), ui, post: () => calendar(200, 146, Math.min(8, 1 + Math.floor(p * 7.99)), L) };
};

const s8 = (f: number, L: Label[]): Out => {
  const l = f - B[7], t = f - OFF;
  bedroom(f, L);
  const off = t > 0;
  hero(HX, FEET, 1, { armL: 0.2, armR: off ? 2.6 : lerp(0.2, 2.9, easeOut((l - 6) / 16)) }, { eye: off ? "wide" : "open", mouth: off ? "o" : "flat" });
  if (!off) goggles(HX, HEADY + 1 - easeIn((l - 12) / 13) * 18);
  else { const gx = HX + 30 + t * 3, gy = HEADY - 30 - t * 6 + t * t * 0.35; if (gy < H) goggles(gx, gy); }
  if (t > 16) for (let i = 0; i < 4; i++) { const ang = f * 0.18 + i * PI / 2; sparkle(HX + Math.cos(ang) * 30, HEADY - 40 + Math.sin(ang) * 8, 2, hex("#ffe600"), 1); }
  return { rot: PI * backOut(sat((t - 14) / 16)), ui: L.length };
};
const easeIn = (t: number) => Math.pow(sat(t), 3);

const s9 = (f: number, L: Label[]): Out => {
  const l = f - B[8];
  navy(135, 300);
  brainChar(135, 318, 1.3, l > 30 && l < 62 ? "wink" : "happy", f);
  picture(135, 206, Math.sin(l * 0.05) * 0.06, 1.0);
  for (let i = 0; i < 10; i++) { const ang = i / 10 * PI * 2 + l * 0.03, r = 98 + Math.sin(l * 0.1 + i) * 6; sparkle(135 + Math.cos(ang) * r, 300 + Math.sin(ang) * r * 0.9, i % 3 ? 1 : 2, hex(i % 2 ? "#55efc4" : "#ffe600"), 0.8); }
  return { rot: 0, ui: L.length };
};

const SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9];
export const beatIndex = (f: number) => { let i = 0; while (i < 8 && f >= B[i + 1]) i++; return i; };

// draw a frame into fbA, rotating the world (not the captions) when the scene asks for it
const drawRot = (f: number, L: Label[]) => {
  light.dir = [-0.5, -0.62, 0.6]; light.rimDir = [0.8, -0.45];
  target(fbA);
  const o = SCENES[beatIndex(f)](f, L);
  if (Math.abs(o.rot) > 1e-3) {
    const c = Math.cos(-o.rot), s = Math.sin(-o.rot), cx = 135, cy = 240, bg = hex("#0a0820");
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      const dx = x + 0.5 - cx, dy = y + 0.5 - cy, sx = Math.floor(cx + c * dx - s * dy), sy = Math.floor(cy + s * dx + c * dy), i = (y * W + x) * 3;
      if (sx < 0 || sy < 0 || sx >= W || sy >= H) { fbB[i] = bg[0]; fbB[i + 1] = bg[1]; fbB[i + 2] = bg[2]; continue; }
      const j = (sy * W + sx) * 3; fbB[i] = fbA[j]; fbB[i + 1] = fbA[j + 1]; fbB[i + 2] = fbA[j + 2];
    }
    fbA.set(fbB);
    L.splice(0, o.ui); // world labels would not rotate, so drop them
    // a flipped room puts the floor behind the caption: veil it so the text stays readable
    const v = sat(Math.abs(Math.sin(o.rot / 2)) * 1.2), d = hex("#0e0828");
    darken(56, 78, d, 0, 0.8 * v); for (let y = 78; y < 132; y++) for (let x = 0; x < W; x++) put(x, y, d, 0.8 * v); darken(132, 154, d, 0.8 * v, 0);
  }
  o.post?.();
};

const CUTS = [B[1], B[2], B[3], B[4], B[8]];
const HALF = 7;
export const CHARS_PER_FRAME = 1.6;
const flush = (out: Uint8ClampedArray, L: Label[]) => { for (const l of L) if (l.s) glyphRun(out, l.s, l.x, l.y, hex(l.c), l.size ?? 16, !l.plain); };

export const renderFrame = (f: number, out: Uint8ClampedArray) => {
  const L: Label[] = [];
  const cut = CUTS.find(c => Math.abs(f - c) < HALF);
  drawRot(f, L);
  if (cut !== undefined) {
    const keep = fbA.slice(), l2: Label[] = [];
    drawRot(f < cut ? cut : cut - 1, l2);
    const p = (f - (cut - HALF)) / (HALF * 2), from = f < cut ? keep : fbA, to = f < cut ? fbA : keep;
    const mixed = new Float32Array(W * H * 3);
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      const src = bayer(x >> 2, y >> 2) < p ? to : from, i = (y * W + x) * 3;
      mixed[i] = src[i]; mixed[i + 1] = src[i + 1]; mixed[i + 2] = src[i + 2];
    }
    quantize(mixed, out);
    if (p > 0.5 === f >= cut) flush(out, L);
  } else { quantize(fbA, out); flush(out, L); }
  const bi = beatIndex(f), lf = f - B[bi], lines = BEATS[bi].map((l, i) => (bi === 0 && i === 1 ? { ...l, big: true } : l));
  if (bi === 0) textBlock(out, lines, 80, 999);
  else if (lf >= 3 && B[bi + 1] - f > 3) textBlock(out, lines, 88, (lf - 3) * CHARS_PER_FRAME);
};
