import { W, H, RGB, hex, mix, sat, lerp, easeOut, easeInOut, backOut, makeFB, target, quantize, textBlock, glyphRun, put, light, darken, Line } from "./gfx";
import { Label } from "./art";
import { park, hydrant, ball, shadowBlob, dog, owner, coneDisc, GROUND } from "./art8";
import timing from "./timing.json";

export { W, H };
const B = timing.beats, T = timing as any;
const fbA = makeFB(), fbB = makeFB();
type Txt = [string, string][][];
export const BEATS: Line[][] = (timing.texts as unknown as Txt).map(lines => lines.map(segs => ({ segs: segs.map(([t, c]) => (c ? { t, c } : { t })) })));
// dog: screen-space x range shown in dog vision (red + green collapse into dull yellow)
type Out = { ui: number; zoom?: number; zx?: number; zy?: number; dog?: { x0: number; x1: number; amt: number; line?: boolean } };
const RED = "#ff3a3a", BLUE = "#3a7aff";

const s1 = (f: number, L: Label[]): Out => {
  park(f); hydrant(238, GROUND - 60);
  shadowBlob(178, GROUND + 2, 9); ball(178, GROUND - 7, 8, RED);
  const lost = easeInOut((f - 70) / 14);
  dog(84, GROUND, 1, { run: 0, phase: 0, headDown: lost * (0.6 + 0.3 * Math.sin(f * 0.25)), wag: f < T.sweep[0] ? 1 : 0.15, happy: f < T.sweep[0] ? 0.5 : 0 }, f);
  const ui = L.length;
  if (f > T.sweep[1]) L.push({ s: "?", x: 150, y: GROUND - 118, c: "#ffd84a", size: 32 });
  const sw = easeInOut((f - T.sweep[0]) / (T.sweep[1] - T.sweep[0]));
  return { ui: ui + (f > T.sweep[1] ? 1 : 0), zoom: lerp(1.3, 1, backOut(f / 16)), zx: 135, zy: 340, dog: { x0: 0, x1: sw * W, amt: 1, line: sw > 0 && sw < 1 } };
};

// split screen through the ball: your eyes (left) vs your dog's (right)
const s2 = (f: number, L: Label[]): Out => {
  const l = f - B[1];
  park(f); hydrant(196, GROUND - 6);
  shadowBlob(135, GROUND + 3, 13); ball(135, GROUND - 11, 12, RED, l * 0.02);
  dog(40 + Math.sin(l * 0.05) * 6, GROUND, 1, { run: 0.15, phase: l * 0.25, headDown: 1, wag: 0.4, happy: 0 }, f);
  return { ui: L.length, zoom: 1.5, zx: 135, zy: GROUND - 30, dog: { x0: 135, x1: W, amt: 1, line: true } };
};

const s3 = (f: number, L: Label[]): Out => {
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) put(x, y, mix(hex("#2a2a5a"), hex("#0a0a20"), sat(Math.hypot((x - 135) / 220, (y - 290) / 280))));
  const l = f - B[2], a = easeOut(l / 14), b = easeOut((l - 30) / 14);
  if (a > 0) coneDisc(72, lerp(330, 286, a), 46, ["#ff4a4a", "#4ad84a", "#4a7aff"], f, L, "YOU", "#ffffff");
  if (b > 0) coneDisc(198, lerp(330, 286, b), 46, ["#4a7aff", "#ffd84a"], f, L, "DOG", "#ffffff");
  if (l > 50) { L.push({ s: "NO RED CONES", x: 152, y: 372, c: "#ff5a4a" }); }
  return { ui: L.length };
};

// throw a blue ball instead, seen through the dog's eyes
const s4 = (f: number, L: Label[]): Out => {
  park(f); hydrant(238, GROUND - 60);
  shadowBlob(178, GROUND - 58, 5); ball(178, GROUND - 63, 5, RED);   // the old red ball, still lying in the grass
  const thrown = f >= T.throw, hx = 40 + 42, hy = GROUND - 116;
  owner(40, GROUND, thrown ? lerp(2.6, 1.2, easeOut((f - T.throw) / 10)) : 2.6 + Math.sin(f * 0.4) * 0.08, thrown ? "grin" : "smile");
  const t = sat((f - T.throw) / (T.land - T.throw)), caught = f >= T.catch;
  const dcx = lerp(104, 132, easeInOut((f - T.throw - 6) / (T.catch - T.throw - 6))), running = thrown && !caught;
  dog(dcx, GROUND, 1, { run: running ? 1 : 0, phase: f * 0.7, headDown: 0, wag: 1, happy: caught ? 1 : 0.4, mouthBall: caught ? BLUE : undefined }, f);
  if (!caught) {
    const bx = thrown ? lerp(hx, 206, t) : hx, by = thrown ? (t < 1 ? lerp(hy, GROUND - 8, t) - Math.sin(Math.PI * t) * 56 : GROUND - 8 - Math.abs(Math.sin((f - T.land) * 0.5)) * 10) : hy;
    if (thrown) shadowBlob(bx, GROUND + 2, 6);
    ball(bx, by, 8, BLUE, f * 0.3);
  }
  const ui = L.length;
  L.push({ s: "DOG VISION", x: 8, y: 150, c: "#ffd84a" });
  return { ui, dog: { x0: 0, x1: W, amt: 1 } };
};

// back to human vision; the dog keeps the blue ball, the red one is still lying there
const s5 = (f: number, L: Label[]): Out => {
  const l = f - B[4], back = easeInOut((f - (B[5] - 24)) / 22);
  park(f); hydrant(238, GROUND - 60);
  shadowBlob(178, GROUND + 2, 9); ball(178, GROUND - 7, 8, RED);
  const hop = Math.abs(Math.sin(l * 0.3)) * 5 * (1 - back);
  dog(84, GROUND - hop, 1, { run: 0, phase: 0, headDown: 0, wag: 1, happy: back > 0.5 ? 0.5 : 1, mouthBall: back > 0.5 ? undefined : BLUE }, f);
  return { ui: L.length, zoom: lerp(1, 1.3, back), zx: 135, zy: 340, dog: { x0: 0, x1: W, amt: 1 - sat(l / 14) } };
};

const SCENES = [s1, s2, s3, s4, s5];
export const beatIndex = (f: number) => { let i = 0; while (i < SCENES.length - 1 && f >= B[i + 1]) i++; return i; };

const draw = (f: number, L: Label[]) => {
  light.dir = [-0.5, -0.65, 0.6]; light.rimDir = [0.8, -0.45]; light.tint = [1, 1, 1]; light.rim = hex("#fff2b0"); light.rimAmt = 0.7;
  target(fbA);
  const o = SCENES[beatIndex(f)](f, L);
  const z = o.zoom ?? 1;
  if (Math.abs(z - 1) > 1e-3) {
    const cx = o.zx ?? 135, cy = o.zy ?? 240;
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      const X = Math.floor(cx + (x + 0.5 - cx) / z), Y = Math.floor(cy + (y + 0.5 - cy) / z), i = (y * W + x) * 3;
      const j = (Math.min(H - 1, Math.max(0, Y)) * W + Math.min(W - 1, Math.max(0, X))) * 3;
      fbB[i] = fbA[j]; fbB[i + 1] = fbA[j + 1]; fbB[i + 2] = fbA[j + 2];
    }
    fbA.set(fbB);
    for (let k = 0; k < o.ui; k++) { const l = L[k]; l.x = Math.round(cx + (l.x - cx) * z); l.y = Math.round(cy + (l.y - cy) * z); }
  }
  if (o.dog && o.dog.amt > 0) {
    const { x0, x1, amt } = o.dog;
    for (let y = 0; y < H; y++) for (let x = Math.max(0, Math.floor(x0)); x < Math.min(W, Math.floor(x1)); x++) {
      // dichromat approximation: everything lands on a blue <-> yellow axis, brightness kept
      const i = (y * W + x) * 3, r = fbA[i], g = fbA[i + 1], b = fbA[i + 2], Y = 0.5 * r + 0.5 * g, Lm = 0.3 * r + 0.59 * g + 0.11 * b, sg = b - Y;
      const nr = sg > 0 ? Lm - sg * 0.3 : Lm - sg * 0.25, ng = sg > 0 ? Lm - sg * 0.1 : Lm - sg * 0.2, nb = sg > 0 ? Lm + sg * 0.7 : Lm + sg * 0.6;
      fbA[i] = lerp(r, sat(nr), amt); fbA[i + 1] = lerp(g, sat(ng), amt); fbA[i + 2] = lerp(b, sat(nb), amt);
    }
    if (o.dog.line) { const lx = Math.floor(x0 > 0 ? x0 : x1); for (let y = 150; y < H; y++) { put(lx, y, hex("#ffffff")); put(lx + 1, y, hex("#ffffff"), 0.5); } }
    if (o.dog.line && x0 > 0) { L.push({ s: "YOU", x: 50, y: 152, c: "#ffffff", size: 24 }); L.push({ s: "YOUR DOG", x: 164, y: 152, c: "#ffd84a", size: 24 }); }
  }
  const d = hex("#0a2a1a");
  darken(56, 72, d, 0, 0.55); for (let y = 72; y < 134; y++) for (let x = 0; x < W; x++) put(x, y, d, 0.55); darken(134, 150, d, 0.55, 0);
};

// slide transition: the next scene pushes the old one out to the left
const CUTS = [B[1], B[2], B[3], B[4]];
const HALF = 6;
export const CHARS_PER_FRAME = 1.6;
const flush = (out: Uint8ClampedArray, L: Label[]) => { for (const l of L) if (l.s) glyphRun(out, l.s, l.x, l.y, hex(l.c), l.size ?? 16, !l.plain); };

export const renderFrame = (f: number, out: Uint8ClampedArray) => {
  const L: Label[] = [];
  const cut = CUTS.find((c: number) => f >= c - HALF && f < c + HALF);
  draw(f, L);
  if (cut !== undefined) {
    const cur = fbA.slice(), lc = L.slice();
    L.length = 0; draw(f < cut ? cut : cut - 1, L);
    const other = fbA.slice(), lo = L.slice();
    const prev = f < cut ? cur : other, next = f < cut ? other : cur;
    const p = easeInOut((f - (cut - HALF)) / (HALF * 2)), off = Math.round(p * W), mixed = new Float32Array(W * H * 3);
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      const i = (y * W + x) * 3, fromPrev = x < W - off, sx = fromPrev ? x + off : x - (W - off), j = (y * W + sx) * 3, src = fromPrev ? prev : next;
      mixed[i] = src[j]; mixed[i + 1] = src[j + 1]; mixed[i + 2] = src[j + 2];
    }
    quantize(mixed, out);
    const useNext = p > 0.5, labs = useNext ? (f < cut ? lo : lc) : (f < cut ? lc : lo), dx = useNext ? W - off : -off;
    flush(out, labs.map(l => ({ ...l, x: l.x + dx })));
  } else { quantize(fbA, out); flush(out, L); }
  const bi = beatIndex(f), lf = f - B[bi], lines = BEATS[bi].map((l, i) => (bi === 0 && i === 1 ? { ...l, big: true } : l));
  if (bi === 0) textBlock(out, lines, 80, 999);
  else if (lf >= 3 && (bi === BEATS.length - 1 || B[bi + 1] - f > 3)) textBlock(out, lines, 88, (lf - 3) * CHARS_PER_FRAME);
};
