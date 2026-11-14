// Chapter 2 data-viz: the leaky memory bucket inside a head, Ebbinghaus forgetting curve, memories dissolving to dust,
// the brain "cleaning", the HSAM calendar. Full-frame SVGs (inserts), our own designs.
import React from "react";
import { W, H, rnd, sat, ease, easeOut, lerp } from "../engine/core";
import { Glow } from "../engine/fx";
import { Vignette, dateOf } from "./Palace";

const GOLD = "#ffc94a";
// a head in profile (our character style: round head, beanie optional) with a glass bucket inside.
// drain: 0 = nothing leaks (Lina), 1 = most drops leak out the bottom. fill rises when nothing drains.
export const LeakyBucket: React.FC<{ f: number; drain: number; beanie?: boolean; label: string; overflow?: number; tint?: string }> = ({ f, drain, beanie, label, overflow = 0, tint = "#7ab8ff" }) => {
  const cx = 960, cy = 520, bx = 960, by = 560, bw = 300, bh = 290;
  const level = drain > 0.5 ? 0.18 + 0.03 * Math.sin(f / 9) : Math.min(1, 0.2 + f / 160);
  const drops = Array.from({ length: 60 }, (_, i) => {
    const t0 = i * 4, t = f - t0; if (t < 0) return null;
    const leaks = rnd(i, 3) < drain, x = bx - bw * 0.35 + rnd(i, 1) * bw * 0.7, c = rnd(i, 5) > 0.5 ? tint : GOLD;
    const yIn = by - 520 + t * 14, surface = by + bh / 2 - level * bh;
    if (yIn < surface) return <circle key={i} cx={x} cy={yIn} r={9} fill={c} opacity={0.9} />;
    if (!leaks) return null;
    const t2 = (yIn - surface) / 14, yOut = by + bh / 2 + Math.max(0, t2 - 8) * 16;
    return t2 > 8 ? <circle key={i} cx={x} cy={yOut} r={8} fill={c} opacity={Math.max(0, 1 - (yOut - by - bh / 2) / 260)} /> : null;
  });
  return <svg width={W} height={H} style={{ position: "absolute" }}>
    <defs><radialGradient id="lb_bg" cx="0.5" cy="0.45" r="0.8"><stop offset="0" stopColor="#24305a" /><stop offset="1" stopColor="#090c1a" /></radialGradient>
      <clipPath id="lb_cl"><path d={`M${bx - bw / 2} ${by - bh / 2} L${bx + bw / 2} ${by - bh / 2} L${bx + bw * 0.4} ${by + bh / 2} L${bx - bw * 0.4} ${by + bh / 2} Z`} /></clipPath></defs>
    <rect width={W} height={H} fill="url(#lb_bg)" />
    {/* head silhouette (profile, facing left) */}
    <circle cx={cx} cy={cy - 40} r={330} fill="#1c2240" stroke="#3a4a80" strokeWidth={6} />
    <path d={`M${cx - 330} ${cy - 60} Q${cx - 380} ${cy + 20} ${cx - 336} ${cy + 40}`} stroke="#3a4a80" strokeWidth={6} fill="none" />
    <path d={`M${cx - 420} ${H + 20} Q${cx - 400} ${cy + 330} ${cx - 160} ${cy + 300} L${cx + 160} ${cy + 300} Q${cx + 400} ${cy + 330} ${cx + 420} ${H + 20} Z`} fill="#1c2240" stroke="#3a4a80" strokeWidth={6} />
    {beanie && <><path d={`M${cx - 300} ${cy - 210} Q${cx - 280} ${cy - 470} ${cx} ${cy - 470} Q${cx + 280} ${cy - 470} ${cx + 304} ${cy - 210} Z`} fill="#e3a83b" />
      <rect x={cx - 316} y={cy - 250} width={632} height={60} rx={28} fill="#c8902e" /></>}
    {/* bucket */}
    <g clipPath="url(#lb_cl)">
      <rect x={bx - bw} y={by + bh / 2 - level * bh} width={bw * 2} height={bh} fill={drain > 0.5 ? tint : GOLD} opacity={0.55} />
      <rect x={bx - bw} y={by + bh / 2 - level * bh} width={bw * 2} height={6} fill="#fff" opacity={0.5} />
    </g>
    <path d={`M${bx - bw / 2} ${by - bh / 2} L${bx - bw * 0.4} ${by + bh / 2} L${bx + bw * 0.4} ${by + bh / 2} L${bx + bw / 2} ${by - bh / 2}`} stroke="#cfe2ff" strokeWidth={6} fill="none" opacity={0.9} />
    {drain > 0.5 && [-0.25, 0, 0.22].map((k, i) => <circle key={i} cx={bx + k * bw} cy={by + bh / 2} r={10} fill="#090c1a" stroke="#cfe2ff" strokeWidth={3} />)}
    {drops}
    {overflow > 0 && <><Glow x={bx} y={by - bh / 2} r={400 * overflow} color={GOLD} o={0.9} />
      {Array.from({ length: 30 }, (_, i) => { const a = -Math.PI * rnd(i, 2), d = overflow * (100 + rnd(i, 3) * 500); return <circle key={i} cx={bx + Math.cos(a) * d} cy={by - bh / 2 + Math.sin(a) * d * 0.7} r={6 + rnd(i, 4) * 8} fill={GOLD} opacity={1 - overflow * 0.5} />; })}</>}
    <text x={110} y={990} fontFamily="Inter" fontWeight={900} fontSize={58} fill={drain > 0.5 ? "#9ac4ff" : GOLD} letterSpacing={6}>{label}</text>
  </svg>;
};

// Ebbinghaus-style forgetting curve, drawn over time k (0..1)
export const ForgettingCurve: React.FC<{ f: number }> = ({ f }) => {
  const k = ease(f / 40), x0 = 300, y0 = 820, w = 1320, h = 560;
  // Ebbinghaus (1885) savings data: minutes → % remembered; drawn on a log time axis so early points don't overlap
  const data = [[0, 100], [20, 58], [60, 44], [540, 36], [1440, 34], [2880, 28], [8640, 25], [44640, 21]];
  const X = (t: number) => x0 + Math.log10(1 + t) / Math.log10(44641) * w, Y = (r: number) => y0 - r / 100 * h;
  const pts: number[][] = []; for (let i = 0; i < data.length - 1; i++) for (let j = 0; j < 12; j++) { const u = j / 12, t = data[i][0] + (data[i + 1][0] - data[i][0]) * u, r = data[i][1] + (data[i + 1][1] - data[i][1]) * u; pts.push([X(t), Y(r)]); }
  pts.push([X(44640), Y(21)]);
  const n = Math.max(2, Math.floor(pts.length * k));
  const marks = [[20, "20 MIN", 58], [60, "1 HOUR", 44], [1440, "1 DAY", 34], [44640, "1 MONTH", 21]] as const;
  return <svg width={W} height={H} style={{ position: "absolute" }}>
    <rect width={W} height={H} fill="#0b0e1a" />
    <Glow x={960} y={500} r={900} color="#4a6aff" o={0.15} />
    <text x={x0} y={180} fontFamily="Inter" fontWeight={900} fontSize={52} fill="#fff">HOW MUCH YOU STILL REMEMBER</text>
    <line x1={x0} y1={y0} x2={x0 + w} y2={y0} stroke="#3a4468" strokeWidth={4} /><line x1={x0} y1={y0} x2={x0} y2={y0 - h - 20} stroke="#3a4468" strokeWidth={4} />
    {[0, 0.5, 1].map(v => <text key={v} x={x0 - 20} y={y0 - v * h + 12} fontFamily="Inter" fontWeight={700} fontSize={30} fill="#7a86aa" textAnchor="end">{v * 100}%</text>)}
    <path d={"M" + pts.slice(0, n).map(p => p.join(" ")).join(" L")} stroke="#ff6a5a" strokeWidth={10} fill="none" strokeLinecap="round" />
    <path d={"M" + pts.slice(0, n).map(p => p.join(" ")).join(" L") + ` L${pts[n - 1][0]} ${y0} L${x0} ${y0} Z`} fill="#ff6a5a" opacity={0.12} />
    {marks.map(([t, l, r], i) => X(t) <= pts[n - 1][0] + 1 && <g key={i}><line x1={X(t)} y1={y0} x2={X(t)} y2={y0 + 16} stroke="#7a86aa" strokeWidth={3} />
      <text x={X(t)} y={y0 + 56} fontFamily="Inter" fontWeight={800} fontSize={28} fill="#aab4d4" textAnchor="middle">{l}</text>
      <circle cx={X(t)} cy={Y(r)} r={11} fill="#ff6a5a" /><text x={X(t) + 18} y={Y(r) - 18} fontFamily="Inter" fontWeight={900} fontSize={34} fill="#fff">{r}%</text></g>)}
  </svg>;
};

// a remembered thing breaking into dust (k 0..1): label in the corner
export const Dissolve: React.FC<{ f: number; kind: "lunch" | "sweater" | "gone"; k: number }> = ({ f, kind, k }) => {
  const parts = Array.from({ length: 260 }, (_, i) => { const x = 660 + rnd(i, 1) * 600, y = 300 + rnd(i, 2) * 480, d = sat(k * 1.6 - rnd(i, 3) * 0.6);
    return <rect key={i} x={x + d * (200 + rnd(i, 4) * 500)} y={y - d * (100 + rnd(i, 5) * 300)} width={8} height={8} fill={["#e8a46a", "#d8d0c0", "#a86a4a", "#7ab8ff"][i % 4]} opacity={d > 0 ? 1 - d : 0} />; });
  return <svg width={W} height={H} style={{ position: "absolute" }}>
    <rect width={W} height={H} fill="#10121e" />
    <g opacity={1 - sat(k * 1.4)} style={{ filter: `blur(${k * 4}px)` }}>
      {kind === "lunch" && <g><rect x={640} y={520} width={640} height={300} rx={30} fill="#9aa6b8" /><circle cx={820} cy={640} r={110} fill="#f4f1ea" /><ellipse cx={820} cy={640} rx={80} ry={60} fill="#e8b04a" /><rect x={980} y={560} width={240} height={180} rx={18} fill="#f4f1ea" /><rect x={1000} y={580} width={200} height={70} rx={10} fill="#8ac87a" /><rect x={1000} y={660} width={200} height={60} rx={10} fill="#d8603a" /></g>}
      {kind === "sweater" && <g><path d="M700 820 L720 470 Q760 410 860 400 L1060 400 Q1160 410 1200 470 L1220 820 Z" fill="#6a9a5a" />{[0, 1, 2, 3].map(r => <path key={r} d={`M720 ${520 + r * 80} L1200 ${520 + r * 80}`} stroke="#4a7a3a" strokeWidth={14} strokeDasharray="30 18" />)}<path d="M880 400 Q960 470 1040 400" stroke="#4a7a3a" strokeWidth={18} fill="none" /></g>}
      {kind === "gone" && null}
    </g>
    {parts}
    <text x={120} y={160} fontFamily="Inter" fontWeight={900} fontSize={64} fill="#fff" opacity={kind === "gone" ? 0 : 1}>{kind === "lunch" ? "LAST TUESDAY'S LUNCH" : kind === "sweater" ? "YOUR TEACHER'S SWEATER" : ""}</text>
    {kind === "gone" && <text x={960} y={580} fontFamily="Inter" fontWeight={900} fontSize={160} fill="#fff" textAnchor="middle" opacity={sat(f / 8)} letterSpacing={20}>GONE.</text>}
  </svg>;
};

// the brain "cleaning": a brain of glowing dots; a soft wave sweeps across, dim dots fade, bright ones stay
export const BrainSweep: React.FC<{ f: number }> = ({ f }) => {
  const wave = lerp(380, 1560, ease(f / 60));
  const dots = Array.from({ length: 420 }, (_, i) => { const a = rnd(i, 1) * Math.PI * 2, r = Math.sqrt(rnd(i, 2));
    const x = 960 + Math.cos(a) * r * 470, y = 520 + Math.sin(a) * r * 300 * (1 - 0.15 * Math.cos(a)); const keep = rnd(i, 3) > 0.82;
    const gone = !keep && x < wave; return <circle key={i} cx={x} cy={y} r={keep ? 7 : 5} fill={keep ? GOLD : "#7ab8ff"} opacity={gone ? Math.max(0, 0.7 - (wave - x) / 120) : keep ? 1 : 0.7} />; });
  return <svg width={W} height={H} style={{ position: "absolute" }}>
    <rect width={W} height={H} fill="#0b0d18" />
    <path d="M500 560 Q470 300 720 230 Q900 150 1080 210 Q1360 220 1430 420 Q1480 600 1330 700 Q1200 800 960 790 Q640 800 540 690 Z" fill="#1c2038" stroke="#3a4468" strokeWidth={6} />
    <path d="M960 220 Q930 450 980 780" stroke="#2c3254" strokeWidth={8} fill="none" />
    {Array.from({ length: 14 }, (_, i) => { const x = 560 + (i % 7) * 130, y = 330 + Math.floor(i / 7) * 220; return <path key={i} d={`M${x} ${y} q30 -40 60 0 t60 0 q20 40 -10 70 t-50 30`} stroke="#2c3254" strokeWidth={7} fill="none" strokeLinecap="round" />; })}
    {dots}
    <rect x={wave - 60} y={150} width={120} height={700} fill="url(#bw)" />
    <defs><linearGradient id="bw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stopColor="#7ab8ff" stopOpacity={0} /><stop offset="0.5" stopColor="#bfe0ff" stopOpacity={0.35} /><stop offset="1" stopColor="#7ab8ff" stopOpacity={0} /></linearGradient></defs>
  </svg>;
};

// HSAM: a desk calendar flipping to random dates; each landing date shows its remembered day
export const Calendar: React.FC<{ f: number }> = ({ f }) => {
  const seg = Math.floor(f / 30), t = f - seg * 30;
  const flipping = t < 10, idx = 1200 + [37, 911, 2650, 1544, 402, 3001, 1777, 220][seg % 8] + (flipping ? Math.floor(t * 7) : 0);
  const [dd, mm, yy] = dateOf(idx).split(" ");
  return <svg width={W} height={H} style={{ position: "absolute" }}>
    <rect width={W} height={H} fill="#141022" />
    <Glow x={700} y={520} r={700} color="#ffd890" o={0.18} />
    <g transform="translate(330 220)">
      <rect x={0} y={0} width={620} height={660} rx={30} fill="#f4f1e8" />
      <rect x={0} y={0} width={620} height={150} rx={30} fill="#c8302c" /><rect x={0} y={110} width={620} height={40} fill="#c8302c" />
      {[110, 250, 370, 510].map(x => <rect key={x} x={x} y={-30} width={22} height={70} rx={10} fill="#5a5a66" />)}
      <text x={310} y={110} fontFamily="Inter" fontWeight={900} fontSize={80} fill="#fff" textAnchor="middle" letterSpacing={8}>{mm}</text>
      <text x={310} y={480} fontFamily="Inter" fontWeight={900} fontSize={300} fill="#1a1a24" textAnchor="middle">{dd}</text>
      <text x={310} y={600} fontFamily="Inter" fontWeight={800} fontSize={60} fill="#7a7a88" textAnchor="middle">{yy}</text>
      {flipping && <rect x={0} y={150} width={620} height={510 * (1 - (t * 7 % 1))} fill="#e8e4da" opacity={0.85} />}
    </g>
    {!flipping && <g opacity={easeOut((t - 10) / 8)} transform={`translate(1090 300) scale(${0.9 + 0.1 * easeOut((t - 10) / 8)})`}>
      <rect x={-14} y={-14} width={548} height={428} rx={18} fill={GOLD} opacity={0.35} style={{ filter: "blur(8px)" }} />
      <rect x={0} y={0} width={520} height={400} rx={10} fill="#fff6dc" /><Vignette x={16} y={16} w={488} h={368} i={idx} />
    </g>}
  </svg>;
};
