// Title card (memory frames swirling into a gold tunnel), Loftus "smashed vs hit" data-viz, police station exterior.
import React from "react";
import { Layer, W, H, sat, ease, easeOut, rnd, lerp } from "../engine/core";
import { Glow, Rain, Bokeh, Shaft } from "../engine/fx";
import { Bricks, Noise, AO } from "../engine/tex";
import { Character, walkPose } from "../chars/Rig2";
import { LINA } from "../chars/cast";

const GOLD = "#ffc94a";
const SCENES = ["#5a7ab8", "#c87a5a", "#6ab08a", "#b85a8a", "#d8b05a", "#5ab0c8", "#8a6ac8", "#c85a5a"];
// a glowing memory frame with a tiny abstract scene inside
export const MemFrame: React.FC<{ x: number; y: number; w: number; r?: number; i: number; o?: number }> = ({ x, y, w, r = 0, i, o = 1 }) => {
  const h = w * 0.66, c = SCENES[i % SCENES.length];
  return <g transform={`translate(${x} ${y}) rotate(${r})`} opacity={o}>
    <rect x={-w / 2 - 6} y={-h / 2 - 6} width={w + 12} height={h + 12} rx={6} fill={GOLD} opacity={0.35} style={{ filter: "blur(5px)" }} />
    <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={4} fill="#fff6dc" />
    <rect x={-w / 2 + w * 0.05} y={-h / 2 + w * 0.05} width={w * 0.9} height={h - w * 0.1} fill={c} />
    <rect x={-w / 2 + w * 0.05} y={h * 0.12} width={w * 0.9} height={h * 0.3 - w * 0.05} fill="#000" opacity={0.25} />
    <circle cx={-w * 0.18 + rnd(i, 2) * w * 0.3} cy={-h * 0.02} r={w * 0.09} fill="#1f1c28" /><circle cx={w * 0.2} cy={-h * 0.2} r={w * 0.07} fill="#fff3c0" opacity={0.9} />
  </g>;
};

export const TitleCard: React.FC<{ f: number }> = ({ f }) => {
  const t = f / 30, k = easeOut(f / 25);
  return <svg width={W} height={H} style={{ position: "absolute" }}>
    <defs><radialGradient id="tbg" cx="0.5" cy="0.5" r="0.7"><stop offset="0" stopColor="#3a2a5a" /><stop offset="1" stopColor="#07060f" /></radialGradient></defs>
    <rect width={W} height={H} fill="url(#tbg)" />
    <Glow x={960} y={540} r={700} color="#ffb84a" o={0.25 + 0.05 * Math.sin(f / 6)} />
    {Array.from({ length: 46 }, (_, i) => { const a = rnd(i, 1) * Math.PI * 2 + t * (0.25 + rnd(i, 2) * 0.3), d = (((rnd(i, 3) + t * 0.12) % 1) ** 1.6) * 1100;
      const s = 0.3 + d / 900; return <MemFrame key={i} x={960 + Math.cos(a) * d} y={540 + Math.sin(a) * d * 0.62} w={120 * s} r={Math.sin(a) * 20} i={i} o={sat(d / 200) * 0.9} />; })}
    <g opacity={k} transform={`translate(960 540) scale(${0.92 + 0.08 * k})`}>
      <text x={0} y={-50} fontFamily="Inter" fontWeight={900} fontSize={84} fill="#fff" textAnchor="middle" style={{ filter: "drop-shadow(0 8px 0 rgba(0,0,0,.5))" }}>WHAT IF YOU COULD</text>
      <text x={0} y={60} fontFamily="Inter" fontWeight={900} fontSize={128} fill={GOLD} textAnchor="middle" style={{ filter: "drop-shadow(0 0 24px rgba(255,190,60,.7)) drop-shadow(0 8px 0 rgba(0,0,0,.5))" }}>NEVER FORGET</text>
      <text x={0} y={150} fontFamily="Inter" fontWeight={900} fontSize={84} fill="#fff" textAnchor="middle" style={{ filter: "drop-shadow(0 8px 0 rgba(0,0,0,.5))" }}>ANYTHING?</text>
    </g>
  </svg>;
};

// Loftus & Palmer 1974: the verb in the question changed the remembered speed (hit 34 mph vs smashed 41 mph)
const Gauge: React.FC<{ x: number; y: number; v: number; label: string; c: string; k: number }> = ({ x, y, v, label, c, k }) => {
  const a = -210 + (v / 60) * 240 * k, rad = (d: number) => d * Math.PI / 180;
  return <g transform={`translate(${x} ${y}) scale(0.82)`}>
    <circle r={250} fill="#141826" stroke="#2a3048" strokeWidth={14} />
    {Array.from({ length: 13 }, (_, i) => { const aa = rad(-210 + i * 20); return <g key={i}><line x1={Math.cos(aa) * 200} y1={Math.sin(aa) * 200} x2={Math.cos(aa) * 230} y2={Math.sin(aa) * 230} stroke="#8a94b0" strokeWidth={i % 2 ? 3 : 6} />
      {i % 2 === 0 && <text x={Math.cos(aa) * 168} y={Math.sin(aa) * 168 + 10} fontFamily="Inter" fontWeight={800} fontSize={28} fill="#8a94b0" textAnchor="middle">{i * 5}</text>}</g>; })}
    <line x1={0} y1={0} x2={Math.cos(rad(a)) * 200} y2={Math.sin(rad(a)) * 200} stroke={c} strokeWidth={12} strokeLinecap="round" />
    <circle r={20} fill={c} />
    <text y={120} fontFamily="Inter" fontWeight={900} fontSize={72} fill="#fff" textAnchor="middle">{Math.round(v * k)} <tspan fontSize={36} fill="#8a94b0">mph</tspan></text>
    <text y={-300} fontFamily="Inter" fontWeight={900} fontSize={64} fill={c} textAnchor="middle">"{label}"</text>
  </g>;
};
export const Loftus: React.FC<{ f: number }> = ({ f }) => <svg width={W} height={H} style={{ position: "absolute" }}>
  <rect width={W} height={H} fill="#0b0e18" />
  <Glow x={500} y={600} r={600} color="#4a8aff" o={0.18} /><Glow x={1420} y={600} r={600} color="#ff5a4a" o={0.18} />
  <text x={960} y={110} fontFamily="Inter" fontWeight={800} fontSize={40} fill="#c8d0e4" textAnchor="middle">"How fast were the cars going when they ___ each other?"</text>
  <line x1={960} y1={200} x2={960} y2={1000} stroke="#2a3048" strokeWidth={4} />
  <Gauge x={520} y={500} v={34} label="HIT" c="#5aa8ff" k={ease((f - 10) / 40)} />
  <Gauge x={1400} y={500} v={41} label="SMASHED" c="#ff5a4a" k={ease((f - 30) / 40)} />
</svg>;

// police station exterior at night; Lina walks out of the door into the rain (walk from x0 by speed)
export const Exterior: React.FC<{ f: number; linaX: number; walking: boolean; frames?: number }> = ({ f, linaX, walking, frames = 0 }) => <>
  <Layer depth={0.4}>
    <rect x={-800} y={-400} width={3520} height={1100} fill="#0c1120" />
    {Array.from({ length: 10 }, (_, i) => <rect key={i} x={-800 + i * 380} y={140 - ((i * 53) % 160)} width={300} height={700} fill="#121a2e" />)}
    <Bokeh x={-600} y={100} w={3100} h={500} n={40} colors={["#ff4a6a", "#4a9aff", "#ffd08a"]} seed={9} f={f} />
  </Layer>
  <Layer depth={1}>
    <Bricks x={-400} y={40} w={2720} h={680} color="#2a3044" mortar="#11141e" o={0.6} />
    <rect x={760} y={330} width={400} height={390} fill="#0e1424" /><rect x={780} y={350} width={170} height={370} fill="#ffe7b0" opacity={0.85} /><rect x={970} y={350} width={170} height={370} fill="#ffe7b0" opacity={0.85} />
    <Glow x={960} y={540} r={420} color="#ffd890" o={0.4} />
    <rect x={720} y={190} width={480} height={110} rx={12} fill="#0e1f44" /><text x={960} y={270} fontFamily="Inter" fontWeight={900} fontSize={76} fill="#9ad0ff" textAnchor="middle" letterSpacing={12} style={{ filter: "drop-shadow(0 0 16px #4aa8ff)" }}>POLICE</text>
    <Glow x={960} y={245} r={360} color="#4aa8ff" o={0.35} />
    {[[200, 360], [1440, 360]].map(([x, y], i) => <g key={i}>
      <rect x={x - 14} y={y - 14} width={288} height={228} fill="#1a2030" />
      <rect x={x} y={y} width={260} height={200} fill={i ? "#3a4a6a" : "#ffd890"} opacity={i ? 0.9 : 0.55} />
      {!i && <><rect x={x} y={y} width={260} height={200} fill="url(#winL)" /><circle cx={x + 170} cy={y + 120} r={26} fill="#2a2030" opacity={0.6} /><rect x={x + 146} y={y + 146} width={48} height={54} fill="#2a2030" opacity={0.6} /></>}
      <line x1={x + 130} y1={y} x2={x + 130} y2={y + 200} stroke="#1a2030" strokeWidth={10} /><line x1={x} y1={y + 100} x2={x + 260} y2={y + 100} stroke="#1a2030" strokeWidth={10} />
      <rect x={x - 22} y={y + 210} width={304} height={14} fill="#3a4258" /></g>)}
    <defs><radialGradient id="winL" cx="0.4" cy="0.3" r="0.8"><stop offset="0" stopColor="#fff2c8" stopOpacity={0.7} /><stop offset="1" stopColor="#c88a3a" stopOpacity={0.2} /></radialGradient></defs>
    <rect x={-400} y={720} width={2720} height={500} fill="#141a28" />
    <rect x={-400} y={720} width={2720} height={500} fill="url(#wet)" opacity={0.5} />
    <defs><linearGradient id="wet" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#ffd890" stopOpacity={0.25} /><stop offset="1" stopColor="#000" stopOpacity={0} /></linearGradient></defs>
    <ellipse cx={960} cy={780} rx={300} ry={30} fill="#ffd890" opacity={0.18} />
    {/* police car with lights */}
    <g transform="translate(1500 880)"><path d="M0 0 L20 -90 Q40 -130 140 -140 L320 -140 Q400 -130 440 -80 L520 -60 L520 0 Z" fill="#e8ecf2" /><rect x={20} y={-80} width={500} height={30} fill="#1a2a5a" />
      <rect x={180} y={-160} width={120} height={22} rx={6} fill="#222" /><rect x={182} y={-158} width={56} height={18} fill={f % 16 < 8 ? "#ff3a3a" : "#3a1010"} /><rect x={242} y={-158} width={56} height={18} fill={f % 16 >= 8 ? "#3a7aff" : "#10183a"} />
      <circle cx={110} cy={0} r={40} fill="#111" /><circle cx={420} cy={0} r={40} fill="#111" /></g>
    <Glow x={1740} y={730} r={500} color={f % 16 < 8 ? "#ff3a3a" : "#3a7aff"} o={0.35} />
    <Character look={LINA} pose={walking ? { ...walkPose((linaX - 960) / 290 * Math.PI * 2), facing: 1, gold: frames > 0 ? 0.6 : 0, look: [0.8, -0.2], mouth: "smile" } : { facing: 1, gold: frames > 0 ? 0.6 : 0, look: [0.9, -0.35], mouth: "smile" }} x={linaX} y={800} s={1.05} f={f} seed={1} rim={{ dx: 4, dy: -3, color: "#ffd890" }} />
    {frames > 0 && Array.from({ length: 9 }, (_, i) => { const a = i / 9 * Math.PI * 2 + f * 0.03, rx = 130, ry = 40;
      const z = Math.sin(a); return <MemFrame key={i} x={linaX + Math.cos(a) * rx} y={800 - 545 + z * 34} w={70 + 20 * (z + 1)} r={Math.cos(a) * 12} i={i} o={frames * (0.55 + 0.45 * (z + 1) / 2)} />; })}
    <Rain f={f} x={-400} y={-200} w={2720} h={1300} n={260} o={0.4} />
  </Layer>
</>;
