// Insert close-ups (≈40% of shots should be inserts): full-frame AbsoluteFill SVGs with their own light.
import React from "react";
import { W, H, sat, ease, easeOut, rnd, lerp } from "../engine/core";
import { Glow, Shaft } from "../engine/fx";
import { Noise } from "../engine/tex";
import { Hatchback } from "./Cars";

const Mitt: React.FC<{ x: number; y: number; r?: number; c?: string; rot?: number; sleeve?: string }> = ({ x, y, r = 70, c = "#24212f", rot = 0, sleeve = "#7a5a3e" }) => <g transform={`rotate(${rot} ${x} ${y})`}>
  <rect x={x - r * 0.75} y={y - r * 3.4} width={r * 1.5} height={r * 2.8} rx={r * 0.4} fill={sleeve} />
  <rect x={x - r * 0.8} y={y - r * 0.95} width={r * 1.6} height={r * 0.42} rx={r * 0.2} fill="#000" opacity={0.25} />
  <circle cx={x} cy={y} r={r} fill={c} /><circle cx={x + r * 0.75} cy={y - r * 0.35} r={r * 0.42} fill={c} />
  <ellipse cx={x - r * 0.3} cy={y - r * 0.45} rx={r * 0.35} ry={r * 0.2} fill="#fff" opacity={0.18} />
</g>;

// coat sleeve from (x0,y0) (off-screen) to the wrist (x1,y1): tapered, shaded, with fold lines and a cuff
export const Sleeve: React.FC<{ x0: number; y0: number; x1: number; y1: number; w0?: number; w1?: number; c?: string; cuff?: string; dark?: string }> = ({ x0, y0, x1, y1, w0 = 190, w1 = 120, c = "#7a5a3e", cuff = "#5a3f28", dark = "#3a2a1c" }) => {
  const dx = x1 - x0, dy = y1 - y0, L = Math.hypot(dx, dy), nx = -dy / L, ny = dx / L;
  const P = (t: number, side: number, w: number) => [x0 + dx * t + nx * side * w / 2, y0 + dy * t + ny * side * w / 2];
  const a1 = P(0, 1, w0), a2 = P(1, 1, w1), b2 = P(1, -1, w1), b1 = P(0, -1, w0);
  const c1 = P(0.86, 1, w1 * 1.08), c2 = P(1, 1, w1 * 1.1), c3 = P(1, -1, w1 * 1.1), c4 = P(0.86, -1, w1 * 1.08);
  const id = `sl${Math.round(x1)}${Math.round(y1)}`;
  return <g>
    <defs><linearGradient id={id} gradientUnits="userSpaceOnUse" x1={P(0.5, 1, w0)[0]} y1={P(0.5, 1, w0)[1]} x2={P(0.5, -1, w0)[0]} y2={P(0.5, -1, w0)[1]}>
      <stop offset="0" stopColor={c} /><stop offset="0.35" stopColor={c} /><stop offset="1" stopColor={dark} /></linearGradient></defs>
    <path d={`M${a1} L${a2} L${b2} L${b1} Z`} fill={`url(#${id})`} />
    {[0.3, 0.5, 0.68].map((t, i) => { const p1 = P(t, 1, w0 * (1 - t) + w1 * t), p2 = P(t + 0.06, -0.2, w0 * (1 - t) + w1 * t); return <path key={i} d={`M${p1} Q${P(t + 0.03, 0.4, w0)} ${p2}`} stroke={dark} strokeOpacity={0.45} strokeWidth={5} fill="none" strokeLinecap="round" />; })}
    <path d={`M${a1} L${a2}`} stroke="#fff" strokeOpacity={0.18} strokeWidth={6} />
    <path d={`M${c1} L${c2} L${c3} L${c4} Z`} fill={cuff} />
  </g>;
};
// a hand gripping something on its right side: sleeve from the top-right, mitten wrapped around, thumb in front
const Grip: React.FC<{ x: number; y: number; c?: string }> = ({ x, y, c = "#2a2636" }) => <g>
  <Sleeve x0={x + 640} y0={y - 520} x1={x + 70} y1={y - 10} />
  <ellipse cx={x + 30} cy={y + 10} rx={66} ry={82} fill={c} />
  <ellipse cx={x + 8} cy={y - 26} rx={26} ry={16} fill="#fff" opacity={0.15} />
  <ellipse cx={x - 34} cy={y + 30} rx={30} ry={22} fill={c} />
  <ellipse cx={x - 40} cy={y + 24} rx={12} ry={7} fill="#fff" opacity={0.18} />
</g>;

const MetalTable: React.FC<{ y?: number }> = ({ y = 640 }) => <>
  <defs><linearGradient id="mt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#6f7c92" /><stop offset="1" stopColor="#3a4458" /></linearGradient></defs>
  <rect x={0} y={0} width={W} height={y} fill="#141b2a" />
  <rect x={0} y={y} width={W} height={H - y} fill="url(#mt)" />
  <Noise x={0} y={y} w={W} h={H - y} freq={0.04} stretch={20} o={0.3} />
  {Array.from({ length: 7 }, (_, i) => <line key={i} x1={0} y1={y + 30 + i * 70} x2={W} y2={y + 30 + i * 70} stroke="#fff" strokeOpacity={0.03} strokeWidth={2} />)}
</>;

const Cup: React.FC<{ x: number; y: number; s?: number; lid?: boolean }> = ({ x, y, s = 1, lid = true }) => <g transform={`translate(${x} ${y}) scale(${s})`}>
  <path d="M-80 -250 L80 -250 L62 0 L-62 0 Z" fill="#f2efe6" /><path d="M30 -250 L80 -250 L62 0 L36 0 Z" fill="#000" opacity={0.08} />
  {lid ? <rect x={-88} y={-272} width={176} height={34} rx={8} fill="#3a3530" /> : <ellipse cx={0} cy={-250} rx={80} ry={14} fill="#2e180a" />}<rect x={-74} y={-170} width={150} height={58} fill="#b0623a" />
  <text x={0} y={-130} fontFamily="Inter" fontWeight={900} fontSize={30} fill="#f2efe6" textAnchor="middle">JOE'S</text>
</g>;

// 1) a coffee cup slams onto the metal table (impact at frame t0)
export const CoffeeSlam: React.FC<{ f: number; t0?: number }> = ({ f, t0 = 8 }) => {
  const u = sat(f / t0), y = lerp(-200, 760, u * u), hit = f - t0, shake = hit >= 0 && hit < 10 ? (rnd(f, 1) - 0.5) * 24 * (1 - hit / 10) : 0;
  return <svg width={W} height={H} style={{ position: "absolute", transform: `translate(${shake}px,${shake * 0.6}px)` }}>
    <MetalTable y={520} />
    <Shaft pts={[[700, -50], [1220, -50], [1500, 1080], [420, 1080]]} color="#d6ecff" o={0.25} />
    <ellipse cx={960} cy={772} rx={hit >= 0 ? 150 : 90 + u * 50} ry={22} fill="#000" opacity={0.45} />
    <Cup x={960} y={y} s={1.15} />
    <Grip x={960 + 84} y={y - 150} />
    {hit >= 0 && hit < 24 && Array.from({ length: 16 }, (_, i) => { const a = -Math.PI * (0.1 + 0.8 * rnd(i, 3)), v = 8 + rnd(i, 4) * 14, t = hit;
      return <circle key={i} cx={960 + Math.cos(a) * v * t * 1.6} cy={460 + Math.sin(a) * v * t + 0.9 * t * t} r={5 + rnd(i, 5) * 7} fill="#6a3a1c" opacity={1 - t / 24} />; })}
    {hit >= 0 && <ellipse cx={960} cy={776} rx={Math.min(230, 60 + hit * 18)} ry={Math.min(30, 8 + hit * 2)} fill="#5a3218" opacity={0.75} />}
  </svg>;
};

// 2) the case photo slides across the table: a bent bicycle wheel lying on a wet road
export const PhotoInsert: React.FC<{ f: number }> = ({ f }) => {
  const u = easeOut(f / 30), px = lerp(1300, 900, u);
  return <svg width={W} height={H} style={{ position: "absolute" }}>
    <MetalTable y={-10} />
    <Glow x={900} y={520} r={760} color="#d6ecff" o={0.25} />
    {/* case folder */}
    <g transform="rotate(4 600 600)"><rect x={250} y={330} width={620} height={500} rx={10} fill="#c9a76a" /><rect x={250} y={300} width={220} height={50} rx={10} fill="#c9a76a" />
      <text x={290} y={420} fontFamily="Inter" fontWeight={900} fontSize={44} fill="#5a4220">CASE #4471</text><text x={290} y={470} fontFamily="Inter" fontWeight={700} fontSize={30} fill="#7a5a30">HIT AND RUN · 3 YRS · UNSOLVED</text>
      <rect x={280} y={520} width={300} height={70} fill="none" stroke="#c0392b" strokeWidth={8} transform="rotate(-8 430 555)" /><text x={300} y={572} fontFamily="Inter" fontWeight={900} fontSize={40} fill="#c0392b" transform="rotate(-8 430 555)">COLD CASE</text></g>
    {/* photo */}
    <g transform={`translate(${px} 260) rotate(${-5 + u * 3})`}>
      <rect x={0} y={0} width={640} height={540} fill="#f4f1e8" /><rect x={30} y={30} width={580} height={420} fill="#4a5262" />
      <rect x={30} y={300} width={580} height={150} fill="#2e3440" /><line x1={30} y1={380} x2={610} y2={380} stroke="#e8d27a" strokeWidth={8} strokeDasharray="40 30" />
      <g transform="translate(330 360) rotate(-8)">
        <circle cx={-120} cy={0} r={70} fill="none" stroke="#14161c" strokeWidth={9} /><circle cx={-120} cy={0} r={8} fill="#14161c" />
        <ellipse cx={120} cy={4} rx={70} ry={48} fill="none" stroke="#14161c" strokeWidth={9} transform="rotate(25 120 4)" /><circle cx={120} cy={4} r={8} fill="#14161c" />
        <path d="M-120 0 L-30 -2 L60 -80 L-60 -80 Z M-30 -2 L-60 -80 M60 -80 L120 4" stroke="#c0392b" strokeWidth={10} fill="none" strokeLinejoin="round" strokeLinecap="round" />
        <path d="M-60 -80 L-70 -104 M-92 -108 L-48 -108" stroke="#14161c" strokeWidth={10} strokeLinecap="round" />
        <path d="M60 -80 L52 -112 M30 -118 Q52 -128 74 -112" stroke="#14161c" strokeWidth={8} fill="none" strokeLinecap="round" />
      </g>
      <text x={40} y={505} fontFamily="Inter" fontWeight={700} fontSize={28} fill="#555">03 / 03 · ELM STREET</text>
    </g>
    <Sleeve x0={W + 300} y0={700} x1={px + 640} y1={742} w0={200} w1={118} />
    <ellipse cx={px + 600} cy={740} rx={64} ry={54} fill="#2a2636" /><ellipse cx={px + 586} cy={716} rx={20} ry={11} fill="#fff" opacity={0.15} />
  </svg>;
};

// 3) close-up of the spill (cause shown in the room shot before): the cup lies on its side, the lid has rolled away,
// coffee pours out of the mouth in a thick ribbon, spreads into an organic puddle with a highlight, reaches the case
// photo (stains its corner) and drips over the table edge.
export const CoffeeSpill: React.FC<{ f: number }> = ({ f }) => {
  const k = easeOut(f / 34), mouth = [880, 640];
  // a puddle that is mostly a flow: long in the pouring direction, thin, with a few finger-like lobes
  const R = 360 * k, pts = Array.from({ length: 72 }, (_, i) => { const a = i / 72 * Math.PI * 2;
    const lobes = 0.16 * Math.sin(3 * a + 0.6) + 0.1 * Math.sin(5 * a + 2.1) + 0.06 * Math.sin(9 * a + 1.3) + 0.22 * Math.max(0, Math.cos(a - 0.15)) ** 8;
    const r = R * (1 + lobes + 0.015 * Math.sin(13 * a + f * 0.2));
    return [mouth[0] + 30 + R * 0.62 + Math.cos(a) * r * 1.05, mouth[1] + 30 + Math.sin(a) * r * 0.24]; });
  const d = "M" + pts.map(p => p.map(v => v.toFixed(1)).join(" ")).join(" L") + " Z";
  const edge = 900;
  return <svg width={W} height={H} style={{ position: "absolute", transform: `scale(${1 + f * 0.002})`, transformOrigin: "900px 640px" }}>
    <defs>
      <linearGradient id="cs_t" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#56627a" /><stop offset="1" stopColor="#8a96ac" /></linearGradient>
      <radialGradient id="cs_c" cx="0.4" cy="0.4" r="0.7"><stop offset="0" stopColor="#7a4420" /><stop offset="0.6" stopColor="#4a2810" /><stop offset="1" stopColor="#2e180a" /></radialGradient>
      <clipPath id="cs_clip"><rect x={0} y={0} width={W} height={edge} /></clipPath>
    </defs>
    <rect width={W} height={300} fill="#141b2a" />
    <rect y={300} width={W} height={edge - 300} fill="url(#cs_t)" />
    <Noise x={0} y={300} w={W} h={edge - 300} freq={0.03} stretch={20} o={0.25} />
    <rect y={edge} width={W} height={60} fill="#3e475a" /><rect y={edge + 60} width={W} height={H - edge - 60} fill="#0e121c" />
    <Glow x={900} y={420} r={800} color="#d6ecff" o={0.25} />
    {/* case photo on the table; its corner gets stained */}
    <g transform="rotate(-7 1400 560)"><rect x={1240} y={430} width={400} height={300} fill="#f4f1e8" /><rect x={1262} y={452} width={356} height={210} fill="#4a5262" />
      <circle cx={1360} cy={600} r={44} fill="none" stroke="#14161c" strokeWidth={7} /><circle cx={1500} cy={600} r={44} fill="none" stroke="#14161c" strokeWidth={7} /><path d="M1360 600 L1420 600 L1460 550 L1390 550 Z" stroke="#c0392b" strokeWidth={7} fill="none" /></g>
    {/* puddle */}
    <g clipPath="url(#cs_clip)">
      <path d={d} fill="#2e180a" opacity={0.35} transform="translate(0 6)" />
      <path d={d} fill="url(#cs_c)" /><path d={d} fill="none" stroke="#b0784a" strokeWidth={4} opacity={0.55} />
      {/* flow streaks + window-light reflections on the liquid */}
      {[0, 1, 2].map(i => <path key={i} d={`M${mouth[0] + 40} ${mouth[1] + 24 + i * 12} Q${mouth[0] + 40 + R * 0.6} ${mouth[1] + 18 + i * 18} ${mouth[0] + 40 + R * 1.3} ${mouth[1] + 30 + i * 22}`} stroke="#8a5228" strokeWidth={3} fill="none" opacity={0.5} />)}
      <rect x={mouth[0] + 120 + R * 0.3} y={mouth[1] + 14} width={R * 0.5} height={6} rx={3} fill="#e8f2ff" opacity={0.35} />
      <rect x={mouth[0] + 140 + R * 0.35} y={mouth[1] + 26} width={R * 0.25} height={4} rx={2} fill="#e8f2ff" opacity={0.25} />
    </g>
    {/* drips over the table edge once the puddle reaches it */}
    {mouth[1] + 40 + R * 0.32 > edge - 20 && [0, 1, 2, 3].map(i => { const t = (f + i * 7) % 18, x = 900 + i * 110 + R * 0.2;
      return <g key={i}><path d={`M${x - 8} ${edge} Q${x} ${edge + 30} ${x + 8} ${edge}`} fill="#4a2810" /><ellipse cx={x} cy={edge + 40 + t * t * 1.4} rx={6} ry={9} fill="#4a2810" opacity={1 - t / 18} /></g>; })}
    {/* pouring ribbon from the cup mouth */}
    <path d={`M${mouth[0] - 6} ${mouth[1] - 26} Q${mouth[0] + 60} ${mouth[1] - 20} ${mouth[0] + 90 + 40 * k} ${mouth[1] + 30} L${mouth[0] + 70 + 40 * k} ${mouth[1] + 40} Q${mouth[0] + 40} ${mouth[1] + 10} ${mouth[0] - 6} ${mouth[1] + 22} Z`} fill="#5a3218" opacity={f < 30 ? 1 : Math.max(0, 1 - (f - 30) / 10)} />
    {/* the cup on its side (mouth to the right) + its lid rolled away */}
    <g transform={`translate(${mouth[0]} ${mouth[1]}) rotate(90)`}><Cup x={0} y={250} s={1.0} lid={false} /></g>
    {(() => { const u = easeOut(f / 20), lx = lerp(mouth[0] + 40, 1010, u), ly = lerp(mouth[1] - 40, 820, u) - Math.sin(Math.min(1, f / 10) * Math.PI) * 60;
      return <g><ellipse cx={lx} cy={828} rx={70} ry={12} fill="#000" opacity={0.25 * u} />
        <g transform={`translate(${lx} ${ly}) rotate(${(1 - u) * -50})`}><ellipse cx={0} cy={0} rx={84} ry={18} fill="#2e2a26" /><ellipse cx={0} cy={-5} rx={74} ry={12} fill="#55504a" /><ellipse cx={-20} cy={-7} rx={14} ry={4} fill="#1a1714" /></g></g>; })()}
    {f < 14 && Array.from({ length: 10 }, (_, i) => { const a = -Math.PI * (0.2 + 0.6 * i / 10), v = 10 + (i % 4) * 4; return <circle key={i} cx={mouth[0] + 80 + Math.cos(a) * v * f} cy={mouth[1] + 20 + Math.sin(a) * v * f + 1.2 * f * f} r={6 + (i % 3) * 3} fill="#5a3218" opacity={1 - f / 14} />; })}
  </svg>;
};

// 4) police database screen: plate typed → searching → MATCH FOUND
export const Screen: React.FC<{ f: number }> = ({ f }) => {
  const plate = "7KR-419", typed = plate.slice(0, Math.max(0, Math.floor((f - 6) / 3))), prog = sat((f - 34) / 24), match = f >= 60;
  return <svg width={W} height={H} style={{ position: "absolute" }}>
    <rect width={W} height={H} fill="#06090f" />
    <rect x={150} y={80} width={1620} height={920} rx={26} fill="#1a1f2a" />
    <rect x={190} y={120} width={1540} height={840} rx={8} fill="#0b1a2c" />
    <Glow x={960} y={540} r={900} color="#2a8aff" o={0.25} />
    <text x={240} y={200} fontFamily="Inter" fontWeight={900} fontSize={42} fill="#7ab8ff" letterSpacing={6}>DMV · PLATE SEARCH</text>
    <rect x={240} y={250} width={900} height={120} rx={12} fill="#06121f" stroke="#2a6ab8" strokeWidth={4} />
    <text x={280} y={335} fontFamily="Inter" fontWeight={900} fontSize={76} fill="#fff" letterSpacing={10}>{typed}{f % 20 < 10 && typed.length < plate.length ? "|" : ""}</text>
    <rect x={240} y={420} width={900} height={22} rx={11} fill="#10263c" /><rect x={240} y={420} width={900 * prog} height={22} rx={11} fill="#4aa8ff" />
    <text x={240} y={490} fontFamily="Inter" fontWeight={700} fontSize={30} fill="#5a86b0">{prog < 1 ? `searching 4,812,330 records… ${Math.floor(prog * 100)}%` : "1 result"}</text>
    {match && <g opacity={sat((f - 60) / 6)}>
      <rect x={1200} y={250} width={480} height={300} rx={14} fill="#0e2236" stroke="#3a7ac8" strokeWidth={3} />
      <g transform="translate(1245 520) scale(0.5)"><Hatchback /></g>
      <text x={1220} y={300} fontFamily="Inter" fontWeight={800} fontSize={26} fill="#9ac4ee">SILVER HATCHBACK · 2019</text>
      <rect x={240} y={600} width={1440} height={200} rx={16} fill="#3a0d10" stroke="#ff4a4a" strokeWidth={6} transform={`scale(${1 + 0.05 * Math.exp(-(f - 60) / 4)})`} style={{ transformOrigin: "960px 700px" }} />
      <text x={960} y={735} fontFamily="Inter" fontWeight={900} fontSize={110} fill="#ff5a5a" textAnchor="middle" letterSpacing={12}>MATCH FOUND</text>
    </g>}
    <rect x={190} y={120} width={1540} height={840} fill="url(#scan)" opacity={0.25} />
    <defs><pattern id="scan" width={4} height={4} patternUnits="userSpaceOnUse"><rect width={4} height={2} fill="#000" /></pattern></defs>
  </svg>;
};
