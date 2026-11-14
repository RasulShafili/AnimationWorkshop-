// Insert close-ups (≈40% of shots should be inserts): full-frame AbsoluteFill SVGs with their own light.
import React from "react";
import { W, H, sat, ease, easeOut, rnd, lerp } from "../engine/core";
import { Glow, Shaft } from "../engine/fx";
import { Noise } from "../engine/tex";

const Mitt: React.FC<{ x: number; y: number; r?: number; c?: string; rot?: number; sleeve?: string }> = ({ x, y, r = 70, c = "#24212f", rot = 0, sleeve = "#7a5a3e" }) => <g transform={`rotate(${rot} ${x} ${y})`}>
  <rect x={x - r * 0.75} y={y - r * 3.4} width={r * 1.5} height={r * 2.8} rx={r * 0.4} fill={sleeve} />
  <rect x={x - r * 0.8} y={y - r * 0.95} width={r * 1.6} height={r * 0.42} rx={r * 0.2} fill="#000" opacity={0.25} />
  <circle cx={x} cy={y} r={r} fill={c} /><circle cx={x + r * 0.75} cy={y - r * 0.35} r={r * 0.42} fill={c} />
  <ellipse cx={x - r * 0.3} cy={y - r * 0.45} rx={r * 0.35} ry={r * 0.2} fill="#fff" opacity={0.18} />
</g>;

const MetalTable: React.FC<{ y?: number }> = ({ y = 640 }) => <>
  <defs><linearGradient id="mt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#6f7c92" /><stop offset="1" stopColor="#3a4458" /></linearGradient></defs>
  <rect x={0} y={0} width={W} height={y} fill="#141b2a" />
  <rect x={0} y={y} width={W} height={H - y} fill="url(#mt)" />
  <Noise x={0} y={y} w={W} h={H - y} freq={0.04} stretch={20} o={0.3} />
  {Array.from({ length: 7 }, (_, i) => <line key={i} x1={0} y1={y + 30 + i * 70} x2={W} y2={y + 30 + i * 70} stroke="#fff" strokeOpacity={0.03} strokeWidth={2} />)}
</>;

const Cup: React.FC<{ x: number; y: number; s?: number }> = ({ x, y, s = 1 }) => <g transform={`translate(${x} ${y}) scale(${s})`}>
  <path d="M-80 -250 L80 -250 L62 0 L-62 0 Z" fill="#f2efe6" /><path d="M30 -250 L80 -250 L62 0 L36 0 Z" fill="#000" opacity={0.08} />
  <rect x={-88} y={-272} width={176} height={34} rx={8} fill="#3a3530" /><rect x={-74} y={-170} width={150} height={58} fill="#b0623a" />
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
    <Mitt x={1010} y={y - 170} r={78} rot={-12} />
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
      <g transform="translate(320 330) rotate(-14)"><ellipse cx={-80} cy={0} rx={90} ry={70} fill="none" stroke="#1a1c22" strokeWidth={10} /><path d="M10 -10 Q80 -40 120 20 Q90 70 30 40" fill="none" stroke="#1a1c22" strokeWidth={10} />
        <path d="M-80 0 L20 -20 L60 -70 M20 -20 L-20 -80 L50 -80" stroke="#c0392b" strokeWidth={9} fill="none" strokeLinecap="round" /></g>
      <text x={40} y={505} fontFamily="Inter" fontWeight={700} fontSize={28} fill="#555">03 / 03 · ELM STREET</text>
    </g>
    <Mitt x={px + 600} y={600} r={74} rot={-70} />
  </svg>;
};

// 3) the detective's coffee tips over (start at t0)
export const CupTip: React.FC<{ f: number; t0?: number }> = ({ f, t0 = 6 }) => {
  const u = ease((f - t0) / 14), spill = sat((f - t0 - 12) / 30);
  return <svg width={W} height={H} style={{ position: "absolute" }}>
    <MetalTable y={430} />
    <Glow x={960} y={500} r={700} color="#d6ecff" o={0.2} />
    <path d={`M1000 760 Q${1000 - 500 * spill} ${760 - 40 * spill} ${1000 - 700 * spill} ${780 + 30 * spill} Q${1000 - 300 * spill} ${820 + 20 * spill} 1000 800 Z`} fill="#4a2810" opacity={0.9} />
    <ellipse cx={980} cy={790} rx={160} ry={24} fill="#000" opacity={0.35} />
    <g transform={`rotate(${-u * 88} 900 790)`}><Cup x={1000} y={790} s={1.05} /></g>
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
      <path d="M1250 470 L1290 400 Q1340 360 1430 360 L1560 360 Q1610 370 1630 420 L1640 470 Z" fill="#b8c0cc" /><circle cx={1310} cy={478} r={30} fill="#111" /><circle cx={1580} cy={478} r={30} fill="#111" />
      <text x={1220} y={300} fontFamily="Inter" fontWeight={800} fontSize={26} fill="#9ac4ee">SILVER HATCHBACK · 2019</text>
      <rect x={240} y={600} width={1440} height={200} rx={16} fill="#3a0d10" stroke="#ff4a4a" strokeWidth={6} transform={`scale(${1 + 0.05 * Math.exp(-(f - 60) / 4)})`} style={{ transformOrigin: "960px 700px" }} />
      <text x={960} y={735} fontFamily="Inter" fontWeight={900} fontSize={110} fill="#ff5a5a" textAnchor="middle" letterSpacing={12}>MATCH FOUND</text>
    </g>}
    <rect x={190} y={120} width={1540} height={840} fill="url(#scan)" opacity={0.25} />
    <defs><pattern id="scan" width={4} height={4} patternUnits="userSpaceOnUse"><rect width={4} height={2} fill="#000" /></pattern></defs>
  </svg>;
};
