// Rainy street at night: the hero's building, wet asphalt with reflections, an ambulance with red/blue lights,
// two paramedics wheeling the neighbour out on a stretcher.
import React from "react";
import { Layer, W, H, rnd, lerp, sat } from "../engine/core";
import { Glow, Rain, Shaft, Bokeh } from "../engine/fx";
import { Bricks, Noise, AO } from "../engine/tex";
import { Character, walkPose } from "../chars/Rig";
import { HERO_PJ, MEDIC, NEIGHBOUR } from "../chars/cast";
const GROUND = 860;
export const talk = (f: number, on: boolean) => (on ? (["open", "flat", "o", "flat"] as const)[Math.floor(f / 3) % 4] : "flat");
const Ambulance: React.FC<{ x: number; f: number }> = ({ x, f }) => {
  const red = Math.floor(f / 6) % 2 === 0;
  return <g transform={`translate(${x} ${GROUND})`}>
    <rect x={0} y={-300} width={520} height={250} rx={18} fill="#e8e8ec" /><rect x={520} y={-220} width={170} height={170} rx={22} fill="#dcdce2" />
    <path d={`M540 -210 L640 -210 L680 -140 L540 -140 Z`} fill="#1a2a3a" />
    <rect x={0} y={-170} width={690} height={26} fill="#d82a2a" /><rect x={200} y={-260} width={60} height={60} fill="#d82a2a" /><rect x={170} y={-245} width={120} height={30} fill="#d82a2a" />
    <rect x={40} y={-326} width={120} height={26} rx={8} fill={red ? "#ff3a3a" : "#5a1a1a"} /><rect x={170} y={-326} width={120} height={26} rx={8} fill={red ? "#1a2a5a" : "#3a6aff"} />
    <circle cx={140} cy={-40} r={50} fill="#111" /><circle cx={560} cy={-40} r={50} fill="#111" /><circle cx={140} cy={-40} r={22} fill="#666" /><circle cx={560} cy={-40} r={22} fill="#666" />
    <Glow x={100} y={-314} r={360} color="#ff2a2a" o={red ? 0.7 : 0.1} /><Glow x={230} y={-314} r={360} color="#2a5aff" o={red ? 0.1 : 0.7} />
    <Glow x={690} y={-90} r={200} color="#fff4d0" o={0.6} />
  </g>;
};
export const Street: React.FC<{ f: number; stretcherU: number; medicTalk: boolean; heroMouth?: any; heroLook?: number[] }> = ({ f, stretcherU, medicTalk, heroMouth = "worried", heroLook = [1, 0] }) => {
  const red = Math.floor(f / 6) % 2 === 0, sx = lerp(560, 1080, stretcherU);
  return <>
    <Layer depth={0.5}>
      <rect x={-800} y={-400} width={W + 1600} height={H + 800} fill="#0b0d1c" />
      {Array.from({ length: 14 }, (_, i) => { const x = -700 + i * 260, h = 380 + rnd(i, 4) * 300; return <g key={i}><rect x={x} y={GROUND - h} width={220} height={h} fill="#14162a" />{Array.from({ length: 18 }, (_, k) => rnd(i * 40 + k, 2) > 0.6 ? <rect key={k} x={x + 20 + (k % 4) * 48} y={GROUND - h + 30 + Math.floor(k / 4) * 70} width={22} height={34} fill="#ffcf7a" opacity={0.6} /> : null)}</g>; })}
      <Bokeh x={-600} y={300} w={2900} h={400} n={30} seed={9} f={f} />
    </Layer>
    <Layer depth={1}>
      {/* building with the lit doorway on the left */}
      <Bricks x={-500} y={-200} w={1000} h={GROUND + 200} color="#3a2630" mortar="#1a1018" />
      <AO x={-500} y={GROUND - 140} w={1000} h={140} dir="up" o={0.6} />
      {Array.from({ length: 12 }, (_, i) => { const x = -460 + (i % 4) * 230, y = Math.floor(i / 4) * 230, lit = rnd(i, 7) < 0.5; return <g key={i}>
        <rect x={x - 8} y={y - 8} width={146} height={166} fill="#1a1018" /><rect x={x} y={y} width={130} height={150} fill={lit ? "#ffcf7a" : "#2a2440"} opacity={lit ? 0.75 : 1} />
        {lit && <rect x={x + 10} y={y + 30} width={50} height={120} fill="#7a3a4a" opacity={0.6} />}
        <line x1={x + 65} y1={y} x2={x + 65} y2={y + 150} stroke="#1a1018" strokeWidth={6} /><rect x={x - 12} y={y + 150} width={154} height={10} fill="#4a3440" />
        {i % 4 === 1 && <g><rect x={x - 20} y={y + 160} width={170} height={8} fill="#1a1018" />{Array.from({ length: 8 }, (_, k) => <line key={k} x1={x - 16 + k * 22} y1={y + 168} x2={x - 16 + k * 22} y2={y + 210} stroke="#1a1018" strokeWidth={4} />)}<line x1={x - 20} y1={y + 210} x2={x + 150} y2={y + 210} stroke="#1a1018" strokeWidth={5} /></g>}
        {i % 4 === 3 && <rect x={x + 30} y={y + 156} width={70} height={44} fill="#8a8a92" />}
      </g>; })}
      {/* door frame + steps + house number */}
      <rect x={286} y={546} width={198} height={14} fill="#1a1018" /><rect x={270} y={856} width={230} height={16} fill="#4a3a40" /><text x={292} y={540} fontFamily="Inter" fontWeight={800} fontSize={30} fill="#d8c8a0">27</text>
      <rect x={300} y={560} width={170} height={300} fill="#ffd89a" /><Glow x={385} y={720} r={320} color="#ffcf8a" o={0.5} />
      <Shaft pts={[[300, 860], [470, 860], [760, 1100], [180, 1100]]} color="#ffd89a" o={0.35} blur={16} from={[385, 860]} to={[385, 1100]} />
      {/* pharmacy neon + shop next door */}
      <rect x={520} y={300} width={520} height={560} fill="#1e1a26" /><rect x={560} y={600} width={440} height={240} fill="#0e2a24" opacity={0.9} />
      <text x={780} y={395} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={60} fill="#5aff9a" style={{ filter: "drop-shadow(0 0 12px #3aff7a)" }}>PHARMACY 24/7</text>
      <Glow x={780} y={380} r={420} color="#3aff7a" o={0.3} />
      <path d="M760 640 L800 640 L800 680 L840 680 L840 720 L800 720 L800 760 L760 760 L760 720 L720 720 L720 680 L760 680 Z" fill="#5aff9a" opacity={0.85} style={{ filter: "drop-shadow(0 0 10px #3aff7a)" }} />
      {/* street lamp */}
      <line x1={1060} y1={GROUND} x2={1060} y2={280} stroke="#141018" strokeWidth={12} /><path d="M1060 290 Q1080 260 1130 270" stroke="#141018" strokeWidth={10} fill="none" /><ellipse cx={1132} cy={280} rx={30} ry={10} fill="#ffe2a8" />
      <Glow x={1132} y={290} r={300} color="#ffcf8a" o={0.5} />
      <Shaft pts={[[1110, 290], [1154, 290], [1300, GROUND], [960, GROUND]]} color="#ffd89a" o={0.18} blur={18} from={[1132, 290]} to={[1132, GROUND]} />
      {/* tree + bins */}
      <rect x={-760} y={560} width={24} height={300} fill="#1a1210" /><circle cx={-750} cy={520} r={110} fill="#14241c" /><circle cx={-690} cy={480} r={80} fill="#1a2e22" /><circle cx={-810} cy={470} r={70} fill="#122018" />
      <rect x={-640} y={770} width={70} height={90} rx={6} fill="#2a3a2a" /><rect x={-560} y={780} width={64} height={80} rx={6} fill="#3a2a3a" />
      {/* wet road with reflections */}
      <rect x={-800} y={GROUND} width={W + 1600} height={500} fill="#101222" />
      <rect x={-800} y={GROUND} width={W + 1600} height={500} fill={red ? "rgba(255,40,40,0.08)" : "rgba(40,90,255,0.08)"} />
      {Array.from({ length: 10 }, (_, i) => <rect key={i} x={-600 + i * 300} y={GROUND + 120} width={160} height={10} fill="#e8e4d0" opacity={0.25} />)}
      <rect x={-800} y={GROUND} width={W + 1600} height={18} fill="#2a2632" /><Noise x={-800} y={GROUND} w={W + 1600} h={500} freq={0.7} o={0.4} seed={11} />
      {/* neon + lamp reflections stretched on the wet road, puddles with rings */}
      <g style={{ mixBlendMode: "screen", filter: "blur(6px)" }} opacity={0.5}><rect x={600} y={GROUND + 20} width={360} height={200} fill="#3aff7a" opacity={0.25} /><rect x={1110} y={GROUND + 20} width={44} height={240} fill="#ffcf8a" opacity={0.6} /><rect x={330} y={GROUND + 20} width={110} height={160} fill="#ffd89a" opacity={0.5} /></g>
      {[[200, GROUND + 70, 120], [900, GROUND + 150, 160], [1500, GROUND + 90, 110]].map(([x, y, r], i) => <g key={i}><ellipse cx={x} cy={y} rx={r} ry={r * 0.18} fill="#1a2040" opacity={0.7} />{[0, 1].map(k => { const tt = ((f + i * 13 + k * 9) % 24) / 24; return <ellipse key={k} cx={x + (k ? 30 : -20)} cy={y} rx={10 + tt * 40} ry={(10 + tt * 40) * 0.2} fill="none" stroke="#9ab0d8" strokeWidth={2} opacity={1 - tt} />; })}</g>)}
      <Ambulance x={1180} f={f} />
      <g opacity={0.25} transform={`translate(0 ${GROUND * 2}) scale(1 -1)`}><Ambulance x={1180} f={f} /></g>
      {/* stretcher with the neighbour, two medics */}
      <g transform={`translate(${sx} 0)`}>
        <rect x={-130} y={GROUND - 150} width={260} height={24} rx={8} fill="#d8dce4" /><line x1={-100} y1={GROUND - 126} x2={-100} y2={GROUND - 20} stroke="#8a8e98" strokeWidth={6} /><line x1={100} y1={GROUND - 126} x2={100} y2={GROUND - 20} stroke="#8a8e98" strokeWidth={6} />
        <circle cx={-100} cy={GROUND - 12} r={12} fill="#222" /><circle cx={100} cy={GROUND - 12} r={12} fill="#222" />
        <Character look={NEIGHBOUR} pose={{ eyes: 0.3, mouth: "worried", headSpin: 90, facing: 1 }} x={250} y={GROUND - 170} rot={-90} s={0.62} />
        <path d={`M-90 ${GROUND - 160} Q0 ${GROUND - 190} 128 ${GROUND - 158} L128 ${GROUND - 140} L-90 ${GROUND - 140} Z`} fill="#c8d8e8" />
        <Character look={MEDIC} pose={{ ...walkPose(f * 0.25, 0.8), aR: [38, 40], aL: [32, 40], mouth: "flat" }} x={-200} y={GROUND} rim={{ dx: 4, dy: -2, color: red ? "#ff6a6a" : "#7a9aff" }} />
        <Character look={MEDIC} pose={{ ...walkPose(f * 0.25 + 3, 0.8), aR: [-34, -40], aL: [-28, -40], mouth: talk(f, medicTalk), facing: -1, look: [1, 0] }} x={210} y={GROUND} rim={{ dx: -4, dy: -2, color: red ? "#ff6a6a" : "#7a9aff" }} />
      </g>
      {/* the hero in the doorway, pyjamas, headphones round the neck */}
      <Character look={HERO_PJ} pose={{ mouth: heroMouth, look: heroLook, brow: 0.6, aL: [10, 40], aR: [-10, 40] }} x={385} y={GROUND} rim={{ dx: 4, dy: -3, color: red ? "#ff6a6a" : "#7a9aff" }} />
      <Rain f={f} x={-800} y={-300} w={W + 1600} h={H + 400} n={260} o={0.35} />
    </Layer>
  </>;
};
