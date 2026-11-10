import { W, H, RGB, hex, mix, sat, lerp, easeOut, easeIn, easeInOut, backOut, makeFB, target, quantize, textBlock, glyphRun, put, light, darken, Line, textWidth } from "./gfx";
import { Label, sparkle } from "./art";
import { room, desk, deskProps, sitterBody, sitterArms, mug, alarm, battery, anatomy, along, caffeineDot, synapse, molecule, RX, RECV, Sit, DESK, S } from "./art10";
import timing from "./timing.json";

export { W, H };
const B = timing.beats, T = timing as any;
const fbA = makeFB(), fbB = makeFB();
type Txt = [string, string][][];
export const BEATS: Line[][] = (timing.texts as unknown as Txt).map(lines => lines.map(segs => ({ segs: segs.map(([t, c]) => (c ? { t, c } : { t })) })));
type Out = { ui: number; zoom?: number; zx?: number; zy?: number };

const CX = 135, MUGX = 196, MUGY = DESK - 13;
const REST_L: [number, number] = [-26, -4], REST_R: [number, number] = [26, -4];
const SIP_R: [number, number] = [11, -64], GRAB_R: [number, number] = [(MUGX - CX) / S + 1, -13 / S + 3];
const ER: [number, number] = [36, -34];
const lerp2 = (a: [number, number], b: [number, number], t: number): [number, number] => [lerp(a[0], b[0], t), lerp(a[1], b[1], t)];
const zzz = (f: number, x: number, y: number, L: Label[], a = 1) => {
  if (a <= 0) return;
  for (let i = 0; i < 3; i++) { const u = (f * 0.018 + i / 3) % 1; L.push({ s: "Z", x: Math.round(x + u * 22 + Math.sin(u * 8) * 3), y: Math.round(y - u * 40), c: "#c8e8ff", size: u > 0.5 ? 24 : 16 }); }
};
const deskScene = (f: number, P: Sit, sun: number, L: Label[], mugOnDesk: boolean, ring = 0) => {
  light.tint = mix([0.96, 0.98, 1.06] as RGB, [1.06, 1.02, 0.94] as RGB, sun) as RGB;
  room(f, sun);
  sitterBody(CX, P);
  desk(f, sun);
  deskProps(f, sun);
  if (mugOnDesk) mug(MUGX, MUGY, 0, 0.8, f);
  alarm(238, f, ring, L);
  sitterArms(CX, P, f);
};

// 1) hook: a sip of coffee, and straight to sleep
const s1 = (f: number, L: Label[]): Out => {
  const down = easeInOut((f - T.sipEnd) / (T.cupDown - T.sipEnd)), rest = easeInOut((f - T.cupDown) / 8);
  const held = f < T.cupDown;
  const hr = held ? lerp2(SIP_R, GRAB_R, down) : lerp2(GRAB_R, REST_R, rest);
  const sleepy = sat((f - T.cupDown) / (T.asleep - T.cupDown));
  const face = f < T.sipEnd ? { eye: "closed" as const, mouth: "smile" as const } : sleepy > 0.95 ? { eye: "closed" as const, mouth: "sleep" as const } : sleepy > 0.3 ? { eye: "half" as const, mouth: "flat" as const } : { eye: "open" as const, mouth: "smile" as const, blink: f > 36 && f < 39 };
  const P: Sit = { face, tilt: 0.2 * easeInOut((f - 50) / 14), lift: 0, hl: REST_L, hr, er: ER, erw: held ? 1 - down : 0, mug: held ? "r" : null, mugTilt: lerp(-0.55, 0, down), steam: 1 };
  deskScene(f, P, 0, L, !held);
  const ui = L.length;
  zzz(f, 162, 200, L, f > T.asleep ? 1 : 0);
  return { ui, zoom: lerp(1.3, 1, backOut(f / 16)), zx: CX, zy: 300 };
};

// 2) inside view: caffeine travels for 20 minutes while you sleep
const s2 = (f: number, L: Label[]): Out => {
  const l = f - B[1], D = T.kick - B[1] - 4, kick = easeOut((f - T.kick) / 10);
  anatomy(f, kick);
  for (let i = 0; i < 9; i++) {
    const u = (l - 4 - i * 9) / D;
    if (u <= 0 || u >= 1) continue;
    const [x, y] = along(u); caffeineDot(x + Math.sin(l * 0.3 + i) * 1.2, y);
  }
  if (kick > 0) for (let i = 0; i < 8; i++) { const a = i * 0.785 + f * 0.05, r = 30 + kick * 18; sparkle(135 + Math.cos(a) * r, 222 + Math.sin(a) * r * 0.8, 2, hex("#ffe14e"), 1 - sat((f - T.kick - 14) / 12)); }
  const m = sat((l - 6) / (T.kick - B[1] - 6)) * 20, mm = Math.floor(m), ss = Math.floor((m % 1) * 60);
  const clock = `${String(mm).padStart(2, "0")}:${String(f >= T.kick ? 0 : ss).padStart(2, "0")}`;
  const ui = L.length;
  L.push({ s: clock, x: Math.round(135 - textWidth(clock, 32) / 2), y: 168, c: f >= T.kick ? "#ffd84a" : "#ffffff", size: 32 });
  zzz(f, 160, 212, L, 1 - kick);
  if (kick > 0.3) L.push({ s: "BRAIN", x: 162, y: 226, c: "#ffd84a", size: 16 });
  else L.push({ s: "STOMACH", x: 172, y: 378, c: "#ffd0c0", size: 16 });
  return { ui, zoom: lerp(1.08, 1, easeOut(l / 30)), zx: 135, zy: 300 };
};

// 3) the synapse: sleepy adenosine leaves during the nap, caffeine docks in the empty spots
const s3 = (f: number, L: Label[]): Out => {
  const l = f - B[2], lit = easeOut((l - 92) / 14);
  synapse(f, lit);
  RX.forEach((x, i) => {
    const la = 12 + i * 10, u = easeIn((l - la) / 34), y0 = RECV(x, f) + 2;
    if (u < 1) {
      molecule("aden", x + Math.sin(u * 5 + i) * 12 * u, y0 - u * 110 + Math.sin(f * 0.15 + i) * 0.8 * (1 - u), (i % 2 ? 0.3 : -0.3) + u * 2.5 * (i % 2 ? 1 : -1), 1 - u * u, 1.25);
    }
    const lc = 66 + i * 7, v = (l - lc) / 14;
    if (v > 0) {
      const yy = v < 1 ? lerp(250, y0, easeIn(v)) : y0 - Math.abs(Math.sin((l - lc - 14) * 0.45)) * 4 * Math.exp(-(l - lc - 14) * 0.12);
      molecule("caf", x, yy, (1 - sat(v)) * 3 * (i % 2 ? 1 : -1), sat(v * 3), 1.25);
    }
  });
  if (lit > 0) for (let i = 0; i < 10; i++) { const x = (i * 29 + f * 3) % 270, y = 250 + ((i * 17 + f * 2) % 50); sparkle(x, y, 1, hex("#ffe14e"), lit * 0.8); }
  const ui = L.length;
  if (l > 6 && l < 50) L.push({ s: "ADENOSINE", x: 8, y: 262, c: "#c8a0ff", size: 16 });
  if (l > 84) L.push({ s: "CAFFEINE", x: 8, y: 262, c: "#ffd84a", size: 16 });
  return { ui };
};

// 4) the alarm at 20 minutes: wake up boosted, the rain clears
const s4 = (f: number, L: Label[]): Out => {
  const woke = f >= T.wake, w = f - T.wake;
  const ring = f < T.ring ? 0 : f < T.wake + 8 ? 1 : 1 - sat((f - T.wake - 8) / 8);
  const sun = easeInOut((w - 4) / 30), lift = woke ? Math.max(0, Math.sin(Math.min(Math.PI, w * 0.25))) * 16 : 0;
  const cheer = woke ? easeOut(w / 6) * (1 - easeInOut((w - 44) / 14)) : 0;
  const wave = Math.sin(f * 0.5) * 6 * cheer;
  const hl = lerp2(REST_L, [-44 + wave, -112 - lift], cheer), hr = lerp2(REST_R, [44 - wave, -112 - lift], cheer);
  const P: Sit = woke ? { face: { eye: w < 30 ? "wide" : "open", mouth: "grin" }, tilt: 0, lift, hl, hr }
    : { face: { eye: f >= T.ring ? "half" : "closed", mouth: f >= T.ring ? "o" : "sleep" }, tilt: f >= T.ring ? 0.1 : 0.2, lift: 0, hl: REST_L, hr: REST_R };
  deskScene(f, P, sun, L, true, ring);
  if (woke) for (let i = 0; i < 6; i++) { const a = i * 1.05 + f * 0.08, r = 72 + Math.sin(f * 0.2 + i) * 6; sparkle(CX + Math.cos(a) * r, 232 + Math.sin(a) * r * 0.8, 2, hex(i % 2 ? "#ffe14e" : "#ffffff"), 0.9); }
  const ui = L.length;
  if (!woke) zzz(f, 162, 200, L, f < T.ring ? 1 : 0);
  battery(238, 184, lerp(0.1, 1, easeOut((w - 4) / 36)), woke ? sat(w / 6) : 0, L);
  return { ui };
};

// 5) share ending, then reach for the mug again: the last frame is the first frame
const s5 = (f: number, L: Label[]): Out => {
  const l = f - B[4], back = easeInOut((f - (B[5] - 26)) / 24), grab = easeInOut((f - (B[5] - 40)) / 12), sip = easeInOut((f - (B[5] - 26)) / 22);
  const bob = Math.abs(Math.sin(l * 0.21)) * 3 * (1 - back);
  const hr = sip > 0 ? lerp2(GRAB_R, SIP_R, sip) : lerp2(REST_R, GRAB_R, grab), held = grab >= 1;
  const P: Sit = { face: back > 0.6 ? { eye: "closed", mouth: "smile" } : { eye: "open", mouth: "grin", blink: l % 50 > 46 }, tilt: Math.sin(l * 0.1) * 0.05 * (1 - back), lift: bob, hl: REST_L, hr, er: ER, erw: sip, mug: held ? "r" : null, mugTilt: lerp(0, -0.55, sip), steam: 1 };
  deskScene(f, P, 1 - back, L, !held);
  for (let i = 0; i < 4; i++) { const a = i * 1.57 + f * 0.06; sparkle(CX + Math.cos(a) * 70, 232 + Math.sin(a) * 50, 2, hex("#ffe14e"), 0.8 * (1 - back)); }
  const ui = L.length;
  battery(238, 184, 1, 1 - sat((f - (B[5] - 40)) / 10), L);
  return { ui, zoom: lerp(1, 1.3, back), zx: CX, zy: 300 };
};

const SCENES = [s1, s2, s3, s4, s5];
export const beatIndex = (f: number) => { let i = 0; while (i < SCENES.length - 1 && f >= B[i + 1]) i++; return i; };

const draw = (f: number, L: Label[]) => {
  light.dir = [-0.5, -0.65, 0.6]; light.rimDir = [0.8, -0.45]; light.tint = [1, 1, 1]; light.rim = hex("#ffe2b0"); light.rimAmt = 0.7;
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
  // soft shade behind the caption
  const d = hex("#0c1418");
  darken(56, 72, d, 0, 0.55); for (let y = 72; y < 150; y++) for (let x = 0; x < W; x++) put(x, y, d, 0.55); darken(150, 166, d, 0.55, 0);
};

// iris transition: the next scene opens from a growing coffee-ring circle
const CUTS = [B[1], B[2], B[3], B[4]];
const HALF = 7, IX = 135, IY = 290, IR = Math.hypot(IX, H - IY) + 4;
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
    const p = easeInOut((f - (cut - HALF)) / (HALF * 2)), r = p * IR, mixed = new Float32Array(W * H * 3);
    const ring = hex("#ffe8c0"), rim = hex("#6a3a1a");
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      const i = (y * W + x) * 3, d = Math.hypot(x + 0.5 - IX, y + 0.5 - IY), src = d < r ? next : prev;
      let c: RGB = [src[i], src[i + 1], src[i + 2]];
      if (p > 0 && p < 1 && Math.abs(d - r) < 3) c = Math.abs(d - r) < 1.6 ? ring : mix(c, rim, 0.7);
      mixed[i] = c[0]; mixed[i + 1] = c[1]; mixed[i + 2] = c[2];
    }
    quantize(mixed, out, 16, 0.7);
    const lp = f < cut ? lc : lo, ln = f < cut ? lo : lc, inside = (l: Label) => Math.hypot(l.x - IX, l.y - IY) < r;
    flush(out, lp.filter(l => !inside(l))); flush(out, ln.filter(inside));
  } else { quantize(fbA, out, 16, 0.7); flush(out, L); }
  const bi = beatIndex(f), lf = f - B[bi], lines = BEATS[bi].map((l, i) => (bi === 0 && i === 1 ? { ...l, big: true } : l));
  if (bi === 0) textBlock(out, lines, 80, 999);
  else if (lf >= 3 && (bi === BEATS.length - 1 || B[bi + 1] - f > 3)) textBlock(out, lines, 88, (lf - 3) * CHARS_PER_FRAME);
};
