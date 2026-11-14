// Chapter 6 pieces: a goodbye at the front door (a figure leaves with a suitcase, the door closes), burning a note in
// the sink (the words float back up out of the smoke in gold), the pill bottle sliding across the doctor's desk.
import React from "react";
import { Layer, rnd, W, H, sat, lerp, ease, easeOut } from "../engine/core";
import { Glow, Shaft } from "../engine/fx";
import { Noise, Wood, Wallpaper, AO } from "../engine/tex";
import { Character, walkPose } from "../chars/Rig2";
import { LINA, EXTRAS } from "../chars/cast";
import { Sleeve } from "./Inserts";

const GOLD = "#ffc94a";
export const BAD_FILTER = (k: number) => `saturate(${1 - 0.6 * k}) sepia(${0.3 * k}) hue-rotate(${180 * k}deg) contrast(${1 + 0.15 * k})`;

// goodbye: little Lina in the hallway, a grown-up with a suitcase walks out of the bright doorway; the door closes
export const Goodbye: React.FC<{ f: number }> = ({ f }) => {
  const walk = Math.min(f, 50), gx = 1150 + walk * 7, close = sat((f - 50) / 20);
  return <>
    <Layer depth={0.8}>
      <rect x={-800} y={-400} width={3520} height={1200} fill="#4a3a4a" /><Wallpaper x={-800} y={-400} w={3520} h={1100} base="#5a4858" ink="#7a6478" kind="stripe" o={0.15} />
      <rect x={1100} y={160} width={420} height={600} fill="#fff4dc" /><Glow x={1310} y={460} r={600} color="#fff4dc" o={0.6 * (1 - close)} />
      <rect x={1100} y={160} width={420 * close} height={600} fill="#6a4a3a" /><circle cx={1100 + 420 * close - 40} cy={480} r={12} fill={GOLD} opacity={close > 0.1 ? 1 : 0} />
      <rect x={1080} y={140} width={460} height={630} fill="none" stroke="#3a2a24" strokeWidth={24} />
    </Layer>
    <Layer depth={1}>
      <Wood x={-900} y={760} w={3720} h={600} color="#5a3a2a" rows={10} />
      <Shaft pts={[[1100, 760], [1520, 760], [1800, 1100], [700, 1100]]} color="#fff4dc" o={0.35 * (1 - close)} />
      {close < 0.95 && <g opacity={1 - close}><Character look={{ ...EXTRAS[0], top: "#5a5a6a", style: "coat", hair: "short", scale: 1.12 }} pose={{ ...walkPose((gx - 1150) / 290 * Math.PI * 2), facing: 1, aR: [10, 10] }} x={gx} y={860} f={f} seed={30} />
        <rect x={gx + 30} y={740} width={70} height={100} rx={10} fill="#3a3a4a" /></g>}
      <Character look={{ ...LINA, scale: 0.72 }} pose={{ facing: 1, look: [0.9, -0.3], mouth: "sad", browIn: 0.8, aR: [40, 60] }} x={700} y={860} f={f} seed={1} />
    </Layer>
  </>;
};

// burning the doctor's words in the kitchen sink: the paper curls into flame, smoke rises, the words reform in gold
export const SinkBurn: React.FC<{ f: number }> = ({ f }) => {
  const burn = sat((f - 12) / 40), rise = sat((f - 40) / 50);
  return <svg width={W} height={H} style={{ position: "absolute", transform: `scale(${1 + f * 0.0011})`, transformOrigin: "960px 420px" }}>
    <rect width={W} height={H} fill="#1a1e2a" /><Glow x={960} y={760} r={600} color="#ff8a3a" o={0.45 * sat(burn * 3) * (1 - rise * 0.5)} />
    <rect x={260} y={700} width={1400} height={400} fill="#9aa4b0" /><ellipse cx={960} cy={760} rx={460} ry={90} fill="#5a6470" /><ellipse cx={960} cy={772} rx={420} ry={70} fill="#3a424c" />
    <rect x={900} y={520} width={40} height={190} fill="#c8d0d8" /><path d="M920 520 Q920 470 1000 470 L1060 470" stroke="#c8d0d8" strokeWidth={36} fill="none" />
    {/* the paper (shrinks/curls as it burns) */}
    <g transform={`translate(960 750) scale(${1 - burn * 0.8}) rotate(${-8 + burn * 20})`} opacity={1 - burn * 0.9}>
      <rect x={-200} y={-60} width={400} height={120} fill="#f4f0e2" /><text x={0} y={-8} fontFamily="Inter" fontWeight={800} fontSize={30} fill="#333" textAnchor="middle">"IT'S ALZHEIMER'S."</text>
      <text x={0} y={34} fontFamily="Inter" fontWeight={700} fontSize={22} fill="#555" textAnchor="middle">"…it will get worse."</text>
      <rect x={-200 + 400 * (1 - burn)} y={-60} width={400 * burn} height={120} fill="#2a1a10" />
    </g>
    {/* flames */}
    {burn > 0 && burn < 1 && Array.from({ length: 14 }, (_, i) => { const x = 820 + rnd(i, 1) * 280, h = 60 + rnd(i, 2) * 120 * (0.6 + 0.4 * Math.sin(f * 0.6 + i));
      return <path key={i} d={`M${x - 18} 760 Q${x - 10} ${760 - h * 0.6} ${x} ${760 - h} Q${x + 10} ${760 - h * 0.6} ${x + 18} 760 Z`} fill={i % 2 ? "#ffb03a" : "#ff6a2a"} opacity={0.85 * (1 - burn * 0.6)} />; })}
    {/* smoke */}
    {Array.from({ length: 16 }, (_, i) => { const t = ((f * 0.8 + i * 9) % 90) / 90; return <circle key={i} cx={960 + Math.sin(t * 6 + i) * 60} cy={720 - t * 520} r={30 + t * 80} fill="#8a92a0" opacity={0.25 * (1 - t) * sat(burn * 2)} />; })}
    {/* the words come back, in gold, out of the smoke */}
    {rise > 0 && <g opacity={rise} transform={`translate(960 ${lerp(600, 300, easeOut(rise))})`} style={{ filter: `drop-shadow(0 0 18px ${GOLD})` }}>
      <text x={0} y={0} fontFamily="Inter" fontWeight={900} fontSize={76} fill={GOLD} textAnchor="middle">"IT'S ALZHEIMER'S."</text>
      <text x={0} y={70} fontFamily="Inter" fontWeight={800} fontSize={44} fill={GOLD} textAnchor="middle" opacity={0.85}>"…it will get worse."</text>
    </g>}
  </svg>;
};

// the pill bottle slides across the desk to Lina (insert)
export const PillSlide: React.FC<{ f: number }> = ({ f }) => { const x = lerp(1500, 900, easeOut(f / 24));
  return <svg width={W} height={H} style={{ position: "absolute" }}>
    <rect width={W} height={H} fill="#cfd8dc" /><rect y={540} width={W} height={540} fill="#8a9aa8" /><Noise x={0} y={540} w={W} h={540} freq={0.04} stretch={20} o={0.2} />
    <Glow x={960} y={400} r={800} color="#e8f4ff" o={0.4} />
    <ellipse cx={x} cy={712} rx={110} ry={20} fill="#000" opacity={0.3} />
    <g transform={`translate(${x} 710)`}>
      <rect x={-80} y={-260} width={160} height={260} rx={22} fill="#e8a33a" opacity={0.92} /><rect x={-60} y={-240} width={30} height={200} rx={12} fill="#fff" opacity={0.25} />
      <rect x={-90} y={-310} width={180} height={64} rx={12} fill="#f4f4f4" /><rect x={-70} y={-180} width={140} height={110} rx={6} fill="#fbfaf6" />
      <text x={0} y={-140} fontFamily="Inter" fontWeight={900} fontSize={22} fill="#333" textAnchor="middle">TRIAL · MX-7</text><text x={0} y={-108} fontFamily="Inter" fontWeight={700} fontSize={16} fill="#666" textAnchor="middle">experimental</text>
    </g>
    {/* Hale's hand letting go (white coat sleeve from the right) */}
    <g opacity={1 - sat((f - 20) / 10)}><Sleeve x0={W + 260} y0={600} x1={x + 110} y1={668} w0={210} w1={120} c="#eef0f4" cuff="#c8ccd6" dark="#9aa0ac" /><circle cx={x + 80} cy={672} r={50} fill="#2a2634" /><circle cx={x + 66} cy={656} r={14} fill="#fff" opacity={0.15} /></g>
  </svg>; };
