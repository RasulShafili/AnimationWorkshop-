import { W, H, RGB, hex, mix, sat, lerp, sstep, easeOut, easeInOut, backOut, hash, bayer, makeFB, target, quantize, textBlock, glyphRun, textWidth, rect, put, glow, light, push, pop, darken, Line } from "./gfx";
import { Label, hero, headArt, sparkle } from "./art";
import { COURIER, RECEIVER, GAMER, cap, nightStreet, van, bike, leaflet, doorstep, box, bubble, stopwatch, homeToServer, stadium, camera, livingRoom, filmFrame, gameScreen, icon } from "./art5";
import T from "./timing.json";

const SEC = T.sections, HS = T.handshake, DV = T.delivery, UD = T.udp;
const fbA = makeFB(), fbB = makeFB();
type Hd = { title: string; sub?: string; c?: string };
const SC = 0.55; // character scale

const walk = (f: number) => ({ armL: 0.25 + Math.sin(f * 0.35) * 0.35, armR: 0.25 - Math.sin(f * 0.35) * 0.35 });
const courier = (x: number, f: number, pose = { armL: 0.2, armR: 0.2 }, face: any = { eye: "open", mouth: "smile" }, bob = 0) => {
  const br = 1 + 0.018 * Math.sin(f * 0.13);
  hero(x, 232 - bob, br, pose, face, 0, SC, COURIER, "#3a2a2a");
  cap(x, 232 - bob - 146 * SC * br, SC);
};
const receiver = (x: number, f: number, pose = { armL: 0.2, armR: 0.2 }, face: any = { eye: "open", mouth: "smile" }) => hero(x, 230, 1 + 0.018 * Math.sin(f * 0.13 + 2), pose, { blink: (f + 30) % 90 < 4, ...face }, 0, SC, RECEIVER, "#2a1a3a");

const s1 = (l: number, f: number, L: Label[]): Hd | null => {
  const vx = lerp(-150, 50, easeOut(l / 90));
  nightStreet(f, l < 90 ? l * 2 : 180);
  for (let i = 0; i < 3; i++) { // far-lane traffic so the street never freezes
    const cx = ((f * (2.2 + i * 0.7) + i * 190) % 640) - 80, col = ["#e8c84e", "#e84a5a", "#5ac8e8"][i];
    rect(cx, 214, 22, 6, hex(col)); rect(cx + 4, 210, 12, 4, hex("#bfe8ff")); glow(cx + 22, 217, 10, hex("#fff0b0"), 0.5);
  }
  const idle = l >= 90 ? (Math.floor(f / 2) % 2) : 0;
  van(vx, 238 - idle, f, l < 90, L);
  if (l >= 90) for (let i = 0; i < 4; i++) { const t = ((f + i * 9) % 36) / 36; glow(vx - 6 - t * 18, 228 - t * 10, 4 + t * 6, hex("#c8c8d8"), 0.35 * (1 - t)); }
  if (l > 30 && l < 150) {
    const bx = lerp(-60, 540, (l - 30) / 70);
    bike(bx, 252, f, L);
    for (let i = 0; i < 10; i++) { const t0 = 30 + i * 6, t = l - t0; if (t > 0 && t < 60) leaflet(lerp(-60, 540, (t0 - 30) / 70) + 10 - t * 0.8, 210 - t * 1.2 + t * t * 0.06, t * 0.3 + i); }
  }
  if (l > 100) { L.push({ s: "Diqqətli, etibarlı", x: 40, y: 246, c: "#8ad0ff" }); L.push({ s: "Sürətli, zəmanətsiz", x: 330, y: 186, c: "#ff9a9a" }); }
  return null;
};

const s2 = (l: number, f: number, L: Label[]): Hd => {
  const cy = homeToServer(f);
  for (let i = 0; i < 6; i++) {
    const t = ((l - i * 26) % 160) / 70;
    if (l - i * 26 < 0 || t < 0 || t > 1) continue;
    const x = lerp(110, 360, t), y = x < 150 ? lerp(160, 112, (x - 110) / 40) : x > 330 ? lerp(112, 120, (x - 330) / 30) : cy(x) - 2;
    box(x, y, (i % 4) + 1, L, 0.7);
  }
  return { title: "Məlumat internetdə kiçik paketlərlə gedir", sub: "Paketləri necə daşımaq? Nəqliyyat qatı: TCP və ya UDP" };
};

const s3 = (l: number, f: number, L: Label[]): Hd => {
  const open = sstep(HS.doorOpen, HS.doorOpen + 14, l);
  doorstep(f, open);
  if (open > 0.5) receiver(340, f, { armL: 0.2, armR: l > HS.shake ? lerp(0.2, 1.25, sstep(HS.shake, HS.shake + 10, l)) : 0.2 });
  const cx = lerp(-40, 230, easeOut(l / 50)), walking = l < 50;
  const knock = l >= HS.knock && l < HS.knock + 10;
  const shakeP = l > HS.shake ? sstep(HS.shake, HS.shake + 10, l) : 0;
  courier(cx + (l > HS.shake ? shakeP * 30 : 0), f, walking ? walk(f) : { armL: 0.2, armR: knock ? 1.5 + Math.sin(l * 2) * 0.3 : lerp(0.2, 1.25, shakeP) }, { eye: "open", mouth: "smile" }, walking ? Math.abs(Math.sin(f * 0.35)) * 2 : 0);
  if (shakeP > 0.9) { for (let i = 0; i < 6; i++) sparkle(290 + Math.cos(i + l * 0.2) * 16, 168 + Math.sin(i * 2 + l * 0.2) * 10, 2, hex("#ffe600"), 0.9); }
  if (l >= HS.syn && l < HS.syn + 70) bubble(150, 90, 150, "SYN: Bağlantı?", L, 1, "#ffe9a0");
  if (l >= HS.synack && l < HS.synack + 70) bubble(260, 76, 170, "SYN-ACK: Hazıram!", L, -1, "#c8f0ff");
  if (l >= HS.ack && l < HS.ack + 70) bubble(140, 90, 150, "ACK: Başlayaq!", L, 1, "#c8ffd8");
  if (l >= HS.shake + 10) L.push({ s: "Bağlantı quruldu ✓".replace(" ✓", ""), x: 182, y: 70, c: "#55efc4", size: 24 });
  return { title: "1. TCP əlaqə yönümlüdürmü? Bəli!", sub: "Göndərmədən əvvəl bağlantı qurur: SYN -> SYN-ACK -> ACK" };
};

const s4 = (l: number, f: number, L: Label[]): Hd => {
  doorstep(f, 1);
  receiver(340, f, { armL: 0.2, armR: 0.2 });
  courier(200, f, { armL: 0.7, armR: 0.7 });
  const B = DV.boxes;
  // boxes already received, stacked behind the receiver in arrival order (3 slots in after its resend)
  const got: number[] = [];
  B.forEach((t, i) => { if (i === DV.lostBox) { if (l > DV.resend + 22) got.push(3); } else if (l > t + 22) got.push(i + 1); });
  const order = got.slice().sort((a, b) => a - b);
  const stacked = l > DV.stack ? order : got;
  stacked.forEach((n, k) => box(392 + (k % 2) * 30, 230 - Math.floor(k / 2) * 23, n, L, 1));
  const fly = (t0: number, n: number, lose = false) => {
    const t = (l - t0) / 22;
    if (t < 0 || t > 1) return;
    if (lose && t > 0.45) { // falls and is lost
      const u = (t - 0.45) / 0.55; box(250 + u * 10, 190 + u * u * 40, n, L, 1, 1 - u); return;
    }
    box(lerp(222, 318, t), 192 - Math.sin(t * Math.PI) * 26, n, L, 1);
  };
  B.forEach((t, i) => fly(t, i + 1, i === DV.lostBox));
  fly(DV.resend, 3);
  B.forEach((t, i) => { if (i !== DV.lostBox && l >= t + 24 && l < t + 70) bubble(300, 84, 92, `ACK ${i + 1}`, L, -1, "#c8ffd8"); });
  if (l >= DV.resend + 24 && l < DV.resend + 70) bubble(300, 84, 92, "ACK 3", L, -1, "#c8ffd8");
  if (l > B[DV.lostBox] + 12 && l < B[DV.lostBox] + 60) L.push({ s: "İTDİ!", x: 248, y: 236, c: "#ff5a7a", size: 24 });
  if (l > B[DV.lostBox] && l < DV.resend + 10) {
    stopwatch(170, 120, sat((l - B[DV.lostBox]) / (DV.timeout - B[DV.lostBox])), l >= DV.timeout);
    if (l >= DV.timeout) bubble(70, 66, 120, "Yenidən 3!", L, 1, "#ffe9a0");
  }
  if (l > DV.stack) for (let i = 0; i < 4; i++) sparkle(396 + i * 10, 170 + Math.sin(l * 0.2 + i) * 4, 1, hex("#ffe600"), 0.8);
  if (l < B[DV.lostBox] + 6) return { title: "3. ACK nədir?", sub: "Alan tərəfin \"aldım\" təsdiqi. Hər paket nömrələnir." };
  if (l < DV.stack) return { title: "4. TCP-də etibarlılıq necə təmin olunur?", sub: "ACK gəlməsə, taymer bitir və paket yenidən göndərilir" };
  return { title: "4. TCP-də etibarlılıq necə təmin olunur?", sub: "Nömrə · ACK · taymer · təkrar göndərmə · düzgün ardıcıllıq" };
};

const s5 = (l: number, f: number, L: Label[]): Hd => {
  stadium(0, 240, f); livingRoom(240, 240, f, l >= UD.glitch[0] && l < UD.glitch[1] ? 0.35 : 0, l > UD.goal && l < UD.goal + 70);
  rect(239, 0, 2, H, hex("#0a0820"));
  camera(196, 252, f);
  for (let k = 0; k * UD.every <= l; k++) {
    const t0 = k * UD.every, t = (l - t0) / 30;
    if (t < 0 || t > 1) continue;
    const x = lerp(220, 310, t), y = lerp(200, 100, t) - Math.sin(t * Math.PI) * 50;
    if (t0 === UD.lost) { if (t > 0.5) filmFrame(x, y, (t - 0.5) * 2); else filmFrame(x, y); continue; }
    filmFrame(x, y);
  }
  if (l >= UD.lost + 15 && l < UD.lost + 60) L.push({ s: "1 kadr itdi", x: 250, y: 150, c: "#ff9a9a", size: 24 });
  if (l > UD.goal && l < UD.goal + 70) L.push({ s: "QOL!", x: 340, y: 140, c: "#ffe600", size: 32 });
  L.push({ s: "CANLI", x: 8, y: 52, c: "#ff5a5a" });
  return l < UD.lost ? { title: "2. UDP necə işləyir?", sub: "Bağlantı qurmur, ACK gözləmir: sadəcə göndərir" } : { title: "2. UDP necə işləyir?", sub: "Bir kadr itsə də yayım dayanmır, davam edir" };
};

const s6 = (l: number, f: number, L: Label[]): Hd => {
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) put(x, y, mix(hex("#1a1040"), hex("#0a0820"), y / H));
  glow(120, 150, 140, hex("#3a7ae8"), 0.25); glow(360, 150, 140, hex("#55efc4"), 0.25);
  rect(0, 222, W, 48, hex("#3a2a2a")); rect(0, 222, W, 2, hex("#6a4a4a"));
  gameScreen(30, 70, 180, 120, f, true, L); gameScreen(270, 70, 180, 120, f, false, L);
  L.push({ s: "TCP", x: 104, y: 196, c: "#8ad0ff", size: 24 }, { s: "UDP", x: 344, y: 196, c: "#55efc4", size: 24 });
  L.push({ s: "PING 300 MS", x: 34, y: 74, c: "#ff6a6a" }, { s: "PING 20 MS", x: 274, y: 74, c: "#55efc4" });
  if (l > 120) L.push({ s: "Gözləyir, ilişir", x: 70, y: 236, c: "#ff9a9a" }, { s: "Axıcı oyun", x: 324, y: 236, c: "#55efc4" });
  return { title: "5. UDP nə zaman üstündür?", sub: "Gecikmə vacib olanda: oyun · video zəng · canlı yayım · DNS" };
};

const s7 = (l: number, f: number, L: Label[]): Hd => {
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) put(x, y, x < 240 ? mix(hex("#0a2a6a"), hex("#061a3a"), y / H) : mix(hex("#0a4a3a"), hex("#062a22"), y / H));
  rect(239, 50, 2, 210, hex("#ffffff"), 0.3);
  L.push({ s: "TCP", x: 102, y: 54, c: "#8ad0ff", size: 32 }, { s: "UDP", x: 342, y: 54, c: "#55efc4", size: 32 });
  const tcp: [string, string][] = [["web", "Veb (HTTP/HTTPS)"], ["mail", "E-poçt (SMTP)"], ["file", "Fayl (FTP)"]];
  const udp: [string, string][] = [["game", "Onlayn oyun"], ["call", "Video zəng"], ["live", "Canlı yayım"], ["dns", "DNS"]];
  tcp.forEach(([k, s], i) => { const a = sstep(20 + i * 22, 30 + i * 22, l); if (a <= 0) return; const y = 112 + i * 46; icon(k, 46, y + (1 - a) * 10, f); if (a > 0.6) L.push({ s, x: 74, y: y - 10, c: "#ffffff", size: 24 }); });
  udp.forEach(([k, s], i) => { const a = sstep(100 + i * 22, 110 + i * 22, l); if (a <= 0) return; const y = 104 + i * 40; icon(k, 284, y + (1 - a) * 10, f); if (a > 0.6) L.push({ s, x: 312, y: y - 10, c: "#ffffff", size: 24 }); });
  return { title: "6. Tətbiq nümunələri", sub: "Hər paket vacibdirsə TCP, sürət vacibdirsə UDP" };
};

const ROWS: [string, string, string][] = [
  ["Bağlantı", "Var (əl sıxma)", "Yoxdur"],
  ["Etibarlılıq", "Zəmanətli (ACK)", "Zəmanət yoxdur"],
  ["Ardıcıllıq", "Qorunur", "Qorunmur"],
  ["Sürət", "Daha yavaş", "Daha sürətli"],
  ["Başlıq", "20 bayt", "8 bayt"],
  ["Nümunə", "Veb, e-poçt", "Oyun, zəng, DNS"],
];
const s8 = (l: number, f: number, L: Label[]): Hd => {
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) put(x, y, mix(hex("#1a1450"), hex("#0a0820"), y / H));
  const x0 = 24, c1 = 140, c2 = 300, x1 = 456, y0 = 52, rh = 26;
  const shown = Math.min(ROWS.length + 1, Math.floor(sat((l - T.tableRow0) / (T.tableStep * 7)) * 7.99));
  for (let r = 0; r < shown; r++) {
    const y = y0 + r * rh, head = r === 0;
    rect(x0, y, x1 - x0, rh - 2, hex(head ? "#2a2a7a" : r % 2 ? "#221a5a" : "#2a2266"));
    if (head) { L.push({ s: "TCP", x: c1 + 60, y: y + 1, c: "#8ad0ff", size: 24 }, { s: "UDP", x: c2 + 60, y: y + 1, c: "#55efc4", size: 24 }); continue; }
    const [a, b, c] = ROWS[r - 1];
    L.push({ s: a, x: x0 + 6, y: y + 1, c: "#ffe600", size: 24, plain: true }, { s: b, x: c1 + 8, y: y + 1, c: "#ffffff", size: 24, plain: true }, { s: c, x: c2 + 8, y: y + 1, c: "#ffffff", size: 24, plain: true });
  }
  if (shown > 0) { rect(c1, y0, 1, shown * rh - 2, hex("#5a5ab8")); rect(c2, y0, 1, shown * rh - 2, hex("#5a5ab8")); }
  if (shown >= ROWS.length + 1) { const sx = ((l - T.tableRow0 - T.tableStep * 7) * 6) % 600 - 60; for (let y = y0 + rh; y < y0 + shown * rh; y++) for (let x = Math.max(x0, sx); x < Math.min(x1, sx + 24); x++) put(x, y, hex("#ffffff"), 0.08); }
  if (l > 230) {
    const a = sstep(230, 245, l); L.push({ s: "Təşəkkürlər!", x: 162, y: 238 + Math.round((1 - a) * 8), c: "#55efc4", size: 32 });
    for (let i = 0; i < 8; i++) { const tw = Math.sin(f * 0.25 + i * 1.7); if (tw > 0) sparkle(150 + i * 25 + Math.sin(i) * 6, 236 + (i % 2) * 30, tw > 0.7 ? 2 : 1, hex(i % 2 ? "#ffe600" : "#ffffff"), tw); }
  }
  return { title: "TCP və UDP: müqayisə cədvəli" };
};

const SCENES = [s1, s2, s3, s4, s5, s6, s7, s8];
export const secIndex = (f: number) => { let i = 0; while (i < 7 && f >= SEC[i + 1]) i++; return i; };
const draw = (f: number, L: Label[]) => { light.dir = [-0.5, -0.62, 0.6]; light.rimDir = [0.8, -0.45]; light.tint = [1, 1, 1]; light.rim = hex("#ffd27a"); light.rimAmt = 0.6; const i = secIndex(f); return SCENES[i](f - SEC[i], f, L); };

const flush = (out: Uint8ClampedArray, L: Label[]) => { for (const l of L) if (l.s) glyphRun(out, l.s, l.x, l.y, hex(l.c), l.size ?? 16, !l.plain); };
const centre = (out: Uint8ClampedArray, s: string, y: number, size: number, c: string, chars = 999) => glyphRun(out, s.slice(0, Math.max(0, Math.floor(chars))), Math.round(240 - textWidth(s, size) / 2), y, hex(c), size);

const HALF = 8;
export const renderFrame = (f: number, out: Uint8ClampedArray) => {
  const L: Label[] = [];
  const cut = SEC.slice(1, 8).find(c => Math.abs(f - c) < HALF);
  target(fbA); let hd = draw(f, L);
  if (cut !== undefined) {
    const keep = fbA.slice(), L2: Label[] = [];
    target(fbA); const hd2 = draw(f < cut ? cut : cut - 1, L2);
    const p = (f - (cut - HALF)) / (HALF * 2), from = f < cut ? keep : fbA, to = f < cut ? fbA : keep;
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) { const src = bayer(x >> 2, y >> 2) < p ? to : from, i = (y * W + x) * 3; fbB[i] = src[i]; fbB[i + 1] = src[i + 1]; fbB[i + 2] = src[i + 2]; }
    if (p > 0.5 !== f >= cut) { L.length = 0; L.push(...L2); hd = hd2; }
    target(fbB);
  }
  // heading band
  const i = secIndex(f), lf = f - SEC[i];
  if (hd) { darken(0, 48, hex("#0a0820"), 0.78, 0.78); darken(48, 56, hex("#0a0820"), 0.78, 0); }
  quantize(cut !== undefined ? fbB : fbA, out);
  flush(out, L);
  if (hd) { centre(out, hd.title, 4, 24, "#ffffff", lf * 2); if (hd.sub) centre(out, hd.sub, 28, 16, "#ffe600", (lf - 10) * 2.2); }
  if (i === 0) { centre(out, "TCP vs UDP", 34, 32, "#ffffff"); centre(out, "Şəfili Rəsul · Kompüter şəbəkələri · 24A", 70, 16, "#ffe600"); }
};
export { W, H } from "./gfx";
