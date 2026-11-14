// Chapter 7 sets: the care home room (window with seasons: snow / blossom / summer), Ayla in an armchair, Lina on a
// chair beside her; inserts: the wedding photo, Ayla's fingers tapping the rhythm, pills poured into the sink, the
// calendar of weekly visits.
import React from "react";
import { Layer, rnd, W, H, sat, lerp, ease, easeOut } from "../engine/core";
import { Glow, Shaft } from "../engine/fx";
import { Noise, Wood, Wallpaper, AO } from "../engine/tex";
import { Character, Pose, SIT } from "../chars/Rig2";
import { LINA, AYLA } from "../chars/cast";
import { Sleeve } from "./Inserts";

const GOLD = "#ffc94a";
export type Season = "snow" | "spring" | "summer";
const WindowView: React.FC<{ f: number; x: number; y: number; w: number; h: number; season: Season }> = ({ f, x, y, w, h, season }) => <g>
  <rect x={x} y={y} width={w} height={h} fill={season === "snow" ? "#b8c4d4" : season === "spring" ? "#bfe0f4" : "#8ec8f0"} />
  <rect x={x} y={y + h * 0.7} width={w} height={h * 0.3} fill={season === "snow" ? "#eef2f6" : season === "spring" ? "#9ad08a" : "#6ab05a"} />
  {[0, 1, 2].map(i => <g key={i}><rect x={x + 60 + i * 150} y={y + h * 0.4} width={14} height={h * 0.32} fill="#5a4a3a" />
    <circle cx={x + 67 + i * 150} cy={y + h * 0.38} r={56} fill={season === "snow" ? "#e8eef4" : season === "spring" ? "#f4b8d0" : "#4a9a4a"} /></g>)}
  {season === "snow" && Array.from({ length: 40 }, (_, i) => <circle key={i} cx={x + rnd(i, 1) * w} cy={y + ((rnd(i, 2) * h + f * (0.8 + rnd(i, 3))) % h)} r={2 + rnd(i, 4) * 3} fill="#fff" opacity={0.9} />)}
  {season === "spring" && Array.from({ length: 16 }, (_, i) => <ellipse key={i} cx={x + ((rnd(i, 1) * w + f * 1.2) % w)} cy={y + ((rnd(i, 2) * h + f * 0.7) % h)} rx={4} ry={2.5} fill="#f8c8dc" />)}
  {season === "summer" && <circle cx={x + w * 0.8} cy={y + h * 0.18} r={40} fill="#fff4c0" />}
  <rect x={x - 12} y={y - 12} width={w + 24} height={h + 24} fill="none" stroke="#f0ece4" strokeWidth={20} /><line x1={x + w / 2} y1={y} x2={x + w / 2} y2={y + h} stroke="#f0ece4" strokeWidth={12} />
</g>;

// warmth 0..1: grey winter light → golden "she's back" light
export const CareHome: React.FC<{ f: number; ayla: Pose; lina: Pose | null; warmth?: number; season?: Season; holdHands?: boolean }> = ({ f, ayla, lina, warmth = 0, season = "snow", holdHands = false }) => <>
  <Layer depth={0.75}>
    <rect x={-1000} y={-500} width={3920} height={1300} fill="#c8c4bc" />
    <Wallpaper x={-1000} y={-500} w={3920} h={1100} base="#d8d0c4" ink="#a89c8c" kind="floral" o={0.1} />
    <WindowView f={f} x={980} y={160} w={480} h={420} season={season} />
    <Glow x={1220} y={370} r={600} color={warmth > 0.5 ? "#ffd890" : "#dfe8f4"} o={0.4 + 0.3 * warmth} />
    <rect x={200} y={200} width={200} height={160} fill="#7a5230" /><rect x={212} y={212} width={176} height={136} fill="#e8a46a" opacity={0.8} />
    <rect x={-60} y={500} width={200} height={20} fill="#8a6a4a" /><rect x={0} y={420} width={60} height={80} rx={10} fill="#e8d8c0" /><circle cx={30} cy={410} r={30} fill="#d87a9a" opacity={0.8} />
  </Layer>
  <Layer depth={1}>
    <Wood x={-1100} y={760} w={4120} h={600} color="#9a8068" rows={10} />
    <AO x={-1100} y={760} w={4120} h={70} dir="up" o={0.35} />
    <Shaft pts={[[990, 170], [1450, 170], [1300, 1100], [500, 1100]]} color={warmth > 0.5 ? "#ffe2a8" : "#e8f0ff"} o={0.2 + 0.25 * warmth} />
    {/* armchair (back + seat) behind Ayla, armrest in front */}
    <path d="M760 860 L760 520 Q760 470 820 470 L960 470 Q1010 470 1010 520 L1010 860 Z" fill="#8a5a6a" />
    <rect x={740} y={760} width={290} height={100} rx={20} fill="#9a6a7a" />
    <Character look={AYLA} pose={{ ...SIT, facing: -1, ...ayla }} x={880} y={860} f={f} seed={4} rim={{ dx: -4, dy: -3, color: warmth > 0.5 ? "#ffe2a8" : "#e8f0ff" }} />
    <rect x={740} y={690} width={70} height={170} rx={20} fill="#9a6a7a" />
    {lina && <><rect x={460} y={560} width={18} height={220} rx={6} fill="#6a5a5a" /><rect x={460} y={770} width={130} height={16} rx={5} fill="#7a6a6a" />
      <Character look={LINA} pose={{ ...SIT, facing: 1, ...lina }} x={530} y={860} f={f} seed={1} rim={{ dx: 4, dy: -3, color: warmth > 0.5 ? "#ffe2a8" : "#e8f0ff" }} /></>}
    <Glow x={820} y={560} r={900} color="#ffc070" o={0.35 * warmth} />
  </Layer>
</>;

export const WeddingPhoto: React.FC<{ f: number }> = ({ f }) => <svg width={W} height={H} style={{ position: "absolute", transform: `scale(${1 + f * 0.0015})`, transformOrigin: "960px 540px" }}>
  <rect width={W} height={H} fill="#e8c89a" /><Glow x={960} y={500} r={700} color="#ffe2a8" o={0.5} />
  <g transform="rotate(-3 960 540)">
    <rect x={560} y={200} width={800} height={640} fill="#c8a03a" /><rect x={590} y={230} width={740} height={580} fill="#efe6d4" />
    <rect x={620} y={260} width={680} height={520} fill="#d8c8a8" />
    {/* young Ayla in a white dress + husband, sepia */}
    <path d="M820 780 L860 520 Q880 470 920 470 Q960 470 980 520 L1010 780 Z" fill="#fbf6ea" /><circle cx={915} cy={430} r={58} fill="#3a2e28" /><path d="M860 400 Q900 340 960 380 Q930 360 880 420 Z" fill="#2a201c" />
    <path d="M1020 780 L1040 520 Q1060 480 1100 480 Q1140 480 1160 520 L1180 780 Z" fill="#3a3430" /><circle cx={1100} cy={440} r={56} fill="#3a2e28" />
    <path d="M1090 520 L1100 560 L1110 520 Z" fill="#fff" />{[0, 1, 2].map(i => <circle key={i} cx={900 + i * 14} cy={600 - i * 8} r={12} fill="#e88aa8" />)}
    <text x={960} y={800} fontFamily="Inter" fontWeight={800} fontSize={30} fill="#7a6040" textAnchor="middle" fontStyle="italic">Ayla & Kerem · 1971</text>
  </g>
</svg>;

// Ayla's fingers on the armrest start tapping the rhythm (beat every 13 frames)
export const TappingHands: React.FC<{ f: number }> = ({ f }) => { const tap = f > 10 ? Math.max(0, Math.sin((f % 13) / 13 * Math.PI)) : 0;
  return <svg width={W} height={H} style={{ position: "absolute" }}>
    <rect width={W} height={H} fill="#6a4a50" /><rect y={560} width={W} height={520} fill="#9a6a7a" /><rect y={560} width={W} height={18} fill="#b88a98" />
    <Sleeve x0={W + 320} y0={420} x1={1250} y1={540} w0={240} w1={150} c="#a58bc9" cuff="#f0e8dc" dark="#5a4878" />
    <g transform={`translate(1160 ${520 - tap * 40}) rotate(${-tap * 8})`}><ellipse cx={0} cy={0} rx={120} ry={95} fill="#2e2a38" /><ellipse cx={-40} cy={-40} rx={40} ry={22} fill="#fff" opacity={0.12} /><ellipse cx={-110} cy={30} rx={40} ry={30} fill="#2e2a38" /></g>
    {tap > 0.8 && <g opacity={0.8}>{[0, 1, 2].map(i => <path key={i} d={`M${1000 - i * 30} ${600 + i * 10} q-20 -10 -40 0`} stroke="#ffe2a8" strokeWidth={5} fill="none" />)}</g>}
    {Array.from({ length: 6 }, (_, i) => { const t = ((f + i * 14) % 80) / 80; return <text key={i} x={1100 + Math.sin(t * 7 + i) * 120} y={460 - t * 360} fontFamily="Inter" fontWeight={900} fontSize={60} fill={GOLD} opacity={sat(f / 20) * (1 - t)}>♪</text>; })}
  </svg>; };

export const PillsSink: React.FC<{ f: number }> = ({ f }) => { const tilt = ease(f / 16);
  return <svg width={W} height={H} style={{ position: "absolute" }}>
    <rect width={W} height={H} fill="#2a3040" /><rect x={260} y={640} width={1400} height={440} fill="#9aa4b0" /><ellipse cx={960} cy={720} rx={460} ry={100} fill="#5a6470" /><ellipse cx={960} cy={734} rx={420} ry={78} fill="#3a424c" />
    <ellipse cx={960} cy={744} rx={34} ry={10} fill="#111" />
    {/* swirling water + pills spiraling into the drain */}
    {Array.from({ length: 3 }, (_, i) => <ellipse key={i} cx={960} cy={744} rx={60 + i * 50} ry={14 + i * 10} fill="none" stroke="#bcd0e4" strokeWidth={3} opacity={0.4} strokeDasharray="40 30" transform={`rotate(${f * (4 + i)} 960 744)`} />)}
    {Array.from({ length: 16 }, (_, i) => { const t = sat((f - 12 - i * 2) / 30); if (t <= 0) return null; const a = t * 8 + i, r = (1 - t) * 260;
      return <ellipse key={i} cx={960 + Math.cos(a) * r} cy={744 + Math.sin(a) * r * 0.25 - (1 - t) * 120 * (t < 0.3 ? 1 : 0)} rx={12 * (1 - t * 0.6)} ry={6 * (1 - t * 0.6)} fill={i % 2 ? "#f4f4f4" : "#e8a33a"} />; })}
    {/* Lina's hand tips the open bottle over the drain */}
    <g transform={`translate(1100 ${420 + tilt * 40}) rotate(${-tilt * 120})`}>
      <rect x={-60} y={-180} width={120} height={180} rx={18} fill="#e8a33a" opacity={0.92} /><rect x={-40} y={-160} width={24} height={140} rx={10} fill="#fff" opacity={0.25} />
      <Sleeve x0={420} y0={-420} x1={70} y1={-80} w0={230} w1={130} c="#1f6f78" cuff="#134a52" dark="#0c3238" />
      <ellipse cx={40} cy={-90} rx={78} ry={70} fill="#2a2536" /><ellipse cx={-30} cy={-70} rx={34} ry={26} fill="#2a2536" /><ellipse cx={10} cy={-120} rx={24} ry={14} fill="#fff" opacity={0.15} />
    </g>
  </svg>; };

// weekly visits: a calendar strip of months with a heart every week (k 0..1 reveals)
export const Visits: React.FC<{ f: number; k: number }> = ({ f, k }) => <svg width={W} height={H} style={{ position: "absolute" }}>
  <rect width={W} height={H} fill="#f4ead8" /><Glow x={960} y={540} r={900} color="#ffd890" o={0.35} />
  {["JAN", "FEB", "MAR", "APR", "MAY", "JUN"].map((mname, mi) => <g key={mi} transform={`translate(${130 + mi * 285} 260)`}>
    <rect x={0} y={0} width={250} height={420} rx={14} fill="#fffaf0" stroke="#e0d4c0" strokeWidth={3} /><rect x={0} y={0} width={250} height={60} rx={14} fill="#d87a9a" />
    <text x={125} y={42} fontFamily="Inter" fontWeight={900} fontSize={32} fill="#fff" textAnchor="middle">{mname}</text>
    {[0, 1, 2, 3].map(w => { const idx = mi * 4 + w, on = idx / 24 < k; return <g key={w} transform={`translate(125 ${110 + w * 85})`}>
      <rect x={-100} y={-34} width={200} height={68} rx={10} fill={on ? "#fde8ee" : "#f4efe6"} />
      {on && <text x={0} y={18} fontFamily="Inter" fontWeight={900} fontSize={48} fill="#e84a7a" textAnchor="middle">♥</text>}</g>; })}
  </g>)}
  <text x={960} y={830} fontFamily="Inter" fontWeight={900} fontSize={56} fill="#7a5a4a" textAnchor="middle" letterSpacing={4}>EVERY SUNDAY</text>
</svg>;
