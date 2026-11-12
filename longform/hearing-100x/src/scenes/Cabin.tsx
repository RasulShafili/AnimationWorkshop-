// The mountains: layered snowy peaks, pine forests, the cabin with warm windows and chimney smoke, falling snow.
// Reused for the move (ch6), the avalanche (ch7) and the porch phone call (ch8).
import React from "react";
import { Layer, W, H, rnd, lerp, sat } from "../engine/core";
import { Glow, Shaft } from "../engine/fx";
import { Noise, AO, Wood } from "../engine/tex";
const Pine: React.FC<{ x: number; y: number; s: number; c: string; snow?: string }> = ({ x, y, s, c, snow = "#e8f0ff" }) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-6} y={-30} width={12} height={34} fill="#2a1a14" />
    {[0, 1, 2].map(k => <g key={k}><path d={`M0 ${-200 + k * 55} L${-60 + k * -12} ${-90 + k * 50} L${60 + k * 12} ${-90 + k * 50} Z`} fill={c} /><path d={`M0 ${-200 + k * 55} L${-22 - k * 4} ${-150 + k * 52} L${22 + k * 4} ${-150 + k * 52} Z`} fill={snow} opacity={0.85} /></g>)}
  </g>
);
export const SKY = { dusk: ["#1a2450", "#5a4a8a", "#e8a0a0"], dawn: ["#3a5a9a", "#a8b8e0", "#ffe0c8"], night: ["#060a1c", "#12183a", "#2a2a50"] };
export const Mountains: React.FC<{ f: number; sky?: keyof typeof SKY; snow?: number; children?: React.ReactNode; fg?: React.ReactNode; cabinX?: number; avalanche?: number }> = ({ f, sky = "dusk", snow = 1, children, fg, cabinX = 1300, avalanche = -1 }) => {
  const [a, b, c] = SKY[sky], g = 880;
  return <>
    <Layer depth={0.15}>
      <defs><linearGradient id={`msk${sky}`} x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={a} /><stop offset="0.55" stopColor={b} /><stop offset="1" stopColor={c} /></linearGradient></defs>
      <rect x={-800} y={-500} width={W + 1600} height={H + 600} fill={`url(#msk${sky})`} />
      {sky === "night" && Array.from({ length: 120 }, (_, i) => <circle key={i} cx={-700 + rnd(i, 1) * 3300} cy={-400 + rnd(i, 2) * 800} r={1 + rnd(i, 3) * 1.8} fill="#fff" opacity={0.4 + rnd(i, 4) * 0.6} />)}
      <Glow x={1500} y={sky === "dawn" ? 520 : 620} r={700} color={sky === "night" ? "#5a6aaa" : "#ffd8b0"} o={0.45} />
    </Layer>
    <Layer depth={0.3}>
      {Array.from({ length: 6 }, (_, i) => { const x = -900 + i * 600, h = 520 + rnd(i, 5) * 260; return <g key={i}><path d={`M${x - 420} ${g} L${x} ${g - h} L${x + 420} ${g} Z`} fill={sky === "night" ? "#1a2040" : "#6a74a8"} /><path d={`M${x - 120} ${g - h + 150} L${x} ${g - h} L${x + 120} ${g - h + 150} L${x + 60} ${g - h + 120} L${x} ${g - h + 170} L${x - 60} ${g - h + 120} Z`} fill="#eef2ff" opacity={0.9} /></g>; })}
    </Layer>
    <Layer depth={0.55}>
      {/* the near slope (the avalanche runs down it) */}
      <path d={`M-900 ${g} L-200 ${g - 520} L500 ${g - 300} L1100 ${g} Z`} fill={sky === "night" ? "#2a3460" : "#c8d4f0"} />
      <Noise x={-900} y={g - 520} w={2000} h={520} freq={0.4} o={0.15} />
      {Array.from({ length: 26 }, (_, i) => <Pine key={i} x={-1000 + i * 140 + rnd(i, 9) * 60} y={g - 40 - rnd(i, 8) * 30} s={0.55 + rnd(i, 7) * 0.3} c={sky === "night" ? "#0e1e24" : "#24483e"} />)}
      {avalanche >= 0 && <g>
        <path d={`M-200 ${g - 520} Q${lerp(-200, 900, avalanche)} ${lerp(g - 520, g - 120, avalanche)} ${lerp(-200, 1300, avalanche)} ${g}`} stroke="#ffffff" strokeWidth={lerp(40, 260, avalanche)} fill="none" opacity={0.95} strokeLinecap="round" />
        {Array.from({ length: 30 }, (_, i) => { const u = sat(avalanche - rnd(i, 1) * 0.3); return <circle key={i} cx={lerp(-200, 1250, u) + rnd(i, 2) * 120} cy={lerp(g - 520, g - 40, u) - rnd(i, 3) * 160} r={40 + rnd(i, 4) * 90} fill="#f4f8ff" opacity={0.85 * (avalanche > 0 ? 1 : 0)} />; })}
      </g>}
    </Layer>
    <Layer depth={1}>
      <rect x={-900} y={g} width={W + 1800} height={600} fill={sky === "night" ? "#c8d0e8" : "#eef2fa"} /><Noise x={-900} y={g} w={W + 1800} h={600} freq={0.5} o={0.12} />
      <AO x={-900} y={g} w={W + 1800} h={60} dir="down" o={0.18} />
      {/* the cabin */}
      <g transform={`translate(${cabinX} ${g})`}>
        <rect x={-260} y={-320} width={520} height={320} fill="#5a3a2a" />{Array.from({ length: 8 }, (_, k) => <rect key={k} x={-260} y={-320 + k * 40} width={520} height={4} fill="#2a1a12" opacity={0.6} />)}
        <path d="M-320 -310 L0 -520 L320 -310 Z" fill="#3a2a2a" /><path d="M-330 -300 L0 -530 L330 -300 L300 -296 L0 -490 L-300 -296 Z" fill="#f4f8ff" />
        <rect x={140} y={-500} width={60} height={140} fill="#4a3a34" />
        {[-150, 60].map(x => <g key={x}><rect x={x} y={-230} width={110} height={110} fill="#ffcf7a" /><line x1={x + 55} y1={-230} x2={x + 55} y2={-120} stroke="#3a2418" strokeWidth={6} /><Glow x={x + 55} y={-175} r={200} color="#ffcf7a" o={0.5} /></g>)}
        <rect x={-40} y={-200} width={80} height={200} fill="#3a2418" /><rect x={-300} y={-8} width={600} height={14} fill="#4a3020" />
        {Array.from({ length: 10 }, (_, k) => { const t = ((f * 0.6 + k * 30) % 300) / 300; return <circle key={k} cx={170 + Math.sin(t * 6 + k) * 30 + t * 80} cy={-520 - t * 380} r={20 + t * 50} fill="#d8dce8" opacity={(1 - t) * 0.4} />; })}
      </g>
      {children}
    </Layer>
    {/* falling snow in front */}
    <Layer depth={1.2}>
      {snow > 0 && Array.from({ length: 160 }, (_, i) => { const y = ((rnd(i, 1) * 1400 + f * (2 + rnd(i, 2) * 3)) % 1400) - 200; return <circle key={i} cx={-500 + rnd(i, 3) * 2900 + Math.sin(f * 0.03 + i) * 30} cy={y} r={2 + rnd(i, 4) * 4} fill="#ffffff" opacity={0.7 * snow} />; })}
      {fg}
    </Layer>
  </>;
};
// a little car for the move
export const Car: React.FC<{ x: number; y: number; c?: string }> = ({ x, y, c = "#3a6aa8" }) => (
  <g transform={`translate(${x} ${y})`}><rect x={0} y={-120} width={380} height={90} rx={24} fill={c} /><path d="M70 -120 L120 -190 L270 -190 L320 -120 Z" fill={c} /><path d="M100 -126 L135 -180 L190 -180 L190 -126 Z M205 -126 L205 -180 L262 -180 L300 -126 Z" fill="#bfe0f0" opacity={0.8} />
    <rect x={160} y={-230} width={120} height={40} rx={6} fill="#c8a070" /><circle cx={90} cy={-30} r={34} fill="#1a1a1a" /><circle cx={300} cy={-30} r={34} fill="#1a1a1a" /><Glow x={380} y={-90} r={140} color="#fff2c0" o={0.6} /></g>
);
