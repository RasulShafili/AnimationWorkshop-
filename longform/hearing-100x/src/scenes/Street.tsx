// Rainy street at night: the hero's building, wet asphalt with reflections, an ambulance with red/blue lights,
// two paramedics wheeling the neighbour out on a stretcher.
import React from "react";
import { Layer, W, H, rnd, lerp, sat } from "../engine/core";
import { Glow, Rain, Shaft, Bokeh } from "../engine/fx";
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
      <rect x={-500} y={-200} width={1000} height={GROUND + 200} fill="#2a2234" />
      {Array.from({ length: 12 }, (_, i) => <rect key={i} x={-460 + (i % 4) * 230} y={0 + Math.floor(i / 4) * 230} width={130} height={150} fill={rnd(i, 7) > 0.5 ? "#3a2e48" : "#ffcf7a"} opacity={rnd(i, 7) > 0.5 ? 1 : 0.7} />)}
      <rect x={300} y={560} width={170} height={300} fill="#ffd89a" /><Glow x={385} y={720} r={320} color="#ffcf8a" o={0.5} />
      <Shaft pts={[[300, 860], [470, 860], [760, 1100], [180, 1100]]} color="#ffd89a" o={0.35} blur={16} from={[385, 860]} to={[385, 1100]} />
      {/* wet road with reflections */}
      <rect x={-800} y={GROUND} width={W + 1600} height={500} fill="#101222" />
      <rect x={-800} y={GROUND} width={W + 1600} height={500} fill={red ? "rgba(255,40,40,0.08)" : "rgba(40,90,255,0.08)"} />
      {Array.from({ length: 10 }, (_, i) => <rect key={i} x={-600 + i * 300} y={GROUND + 120} width={160} height={10} fill="#e8e4d0" opacity={0.25} />)}
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
