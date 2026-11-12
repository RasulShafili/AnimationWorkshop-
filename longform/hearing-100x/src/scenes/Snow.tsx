// Chapter 7: the avalanche field (rescuers, probes, a hovering helicopter blasting snow), the sound view under the
// snow, and the hospital room.
import React from "react";
import { Layer, W, H, rnd, lerp, sat } from "../engine/core";
import { Glow, Shaft } from "../engine/fx";
import { Noise, AO, Wallpaper } from "../engine/tex";
import { Character } from "../chars/Rig";
import { HERO_SNOW, MIA_SNOW, LEO, RESCUER, CHIEF, HERO, MIA } from "../chars/cast";
import { HeartIcon } from "./Poker";
import { talkM } from "./School";
const COLD = { dx: -4, dy: -3, color: "#cfe4ff" };
export const Heli: React.FC<{ x: number; y: number; f: number; spin?: number }> = ({ x, y, f, spin = 1 }) => (
  <g transform={`translate(${x} ${y})`}>
    <ellipse cx={0} cy={0} rx={200} ry={90} fill="#c82a2a" /><path d="M150 -20 L520 -40 L520 0 L160 30 Z" fill="#c82a2a" /><rect x={500} y={-90} width={20} height={110} fill="#a82222" />
    <path d="M-150 -30 Q-60 -80 60 -60 L60 20 L-170 20 Z" fill="#9ad0ff" opacity={0.85} /><rect x={-150} y={70} width={320} height={10} rx={5} fill="#2a2a2a" /><rect x={-100} y={60} width={10} height={20} fill="#2a2a2a" /><rect x={80} y={60} width={10} height={20} fill="#2a2a2a" />
    <text x={20} y={30} fontFamily="Inter" fontWeight={900} fontSize={36} fill="#fff">RESCUE</text>
    <rect x={-6} y={-130} width={12} height={40} fill="#2a2a2a" />
    <ellipse cx={0} cy={-132} rx={380} ry={10 + 6 * Math.abs(Math.sin(f * 1.3 * spin))} fill="#2a2a2a" opacity={0.25 + 0.5 * (1 - spin)} />
    <circle cx={510} cy={-40} r={46} fill="#2a2a2a" opacity={0.25} />
  </g>
);
export const Field7: React.FC<{ f: number; heliX?: number; heliY: number; wash: number; freeze: number; hearts: number; under: number; dig: number; leo: number; heroPose: any; heroHp: boolean; mia: any; mud?: number }> = ({ f, heliX = 1300, heliY, wash, freeze, hearts, under, dig, leo, heroPose, heroHp, mia }) => {
  const g = 840, move = 1 - freeze, leoX = 1180;
  return <>
    <Layer depth={0.2}>
      <defs><linearGradient id="dawn7" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#5a7ac0" /><stop offset="1" stopColor="#ffe8d0" /></linearGradient></defs>
      <rect x={-900} y={-500} width={W + 1800} height={H + 600} fill="url(#dawn7)" />
      {Array.from({ length: 6 }, (_, i) => { const x = -900 + i * 620, h = 540 + rnd(i, 5) * 240; return <g key={i}><path d={`M${x - 440} ${g} L${x} ${g - h} L${x + 440} ${g} Z`} fill="#8a96c8" /><path d={`M${x - 140} ${g - h + 170} L${x} ${g - h} L${x + 140} ${g - h + 170} Z`} fill="#f4f6ff" /></g>; })}
    </Layer>
    <Layer depth={0.6}>
      <path d={`M-900 ${g} Q0 ${g - 260} 900 ${g - 120} Q1700 ${g - 260} 2900 ${g} Z`} fill="#dfe6f6" />
      {Array.from({ length: 22 }, (_, i) => <g key={i} transform={`translate(${-900 + i * 180} ${g - 100 - rnd(i, 3) * 60}) scale(${0.5 + rnd(i, 4) * 0.2})`}><path d="M0 -200 L-60 -40 L60 -40 Z M0 -140 L-72 20 L72 20 Z" fill="#2a4a40" /><path d="M0 -200 L-20 -150 L20 -150 Z" fill="#fff" /></g>)}
    </Layer>
    <Layer depth={1}>
      <rect x={-900} y={g} width={W + 1800} height={600} fill="#f2f6fc" /><Noise x={-900} y={g} w={W + 1800} h={600} freq={0.5} o={0.12} />
      {/* avalanche debris: lumps of snow */}
      {Array.from({ length: 24 }, (_, i) => <ellipse key={i} cx={-500 + i * 130 + rnd(i, 1) * 60} cy={g + 10 + rnd(i, 2) * 80} rx={60 + rnd(i, 3) * 70} ry={24 + rnd(i, 4) * 26} fill={i % 2 ? "#e4ecf8" : "#d6e0f2"} />)}
      {/* the sound view under the snow: Leo, curled up, one slow heartbeat */}
      {under > 0 && <g opacity={under}>
        <rect x={-900} y={g + 40} width={W + 1800} height={600} fill="#06142a" opacity={0.85} />
        <ellipse cx={leoX} cy={g + 240} rx={120} ry={70} fill="none" stroke="#5ae0ff" strokeWidth={3} />
        <circle cx={leoX - 60} cy={g + 220} r={34} fill="none" stroke="#5ae0ff" strokeWidth={3} />
        {(() => { const b = Math.max(0, Math.sin(f * 0.12)) ** 10; return <g><Glow x={leoX} y={g + 240} r={70 + b * 90} color="#ff3a5a" o={0.3 + b * 0.6} /><path transform={`translate(${leoX} ${g + 240}) scale(${0.8 + b * 0.5})`} d="M0 18 C -26 -2 -22 -26 -6 -24 C 0 -23 0 -18 0 -14 C 0 -18 0 -23 6 -24 C 22 -26 26 -2 0 18 Z" fill="#ff4a6a" />{[0, 1].map(k => { const t = ((f + k * 26) % 52) / 52; return <circle key={k} cx={leoX} cy={g + 240} r={30 + t * 340} fill="none" stroke="#5ae0ff" strokeWidth={3} opacity={(1 - t) * 0.7} />; })}</g>; })()}
      </g>}
      {/* helicopter + rotor wash (behind the people) */}
      <Heli x={heliX} y={heliY} f={f} spin={heliY > g - 200 ? 0.5 : 1} />
      {wash > 0 && Array.from({ length: 90 }, (_, i) => { const t = ((f * 3 + rnd(i, 1) * 300) % 300) / 300; const dir = rnd(i, 2) > 0.5 ? 1 : -1; return <circle key={i} cx={heliX + dir * t * 1400} cy={g - 20 - rnd(i, 3) * 260 * (1 - t)} r={4 + rnd(i, 4) * 8} fill="#ffffff" opacity={wash * (1 - t) * 0.9} />; })}
      {/* rescuers with probes (freeze in the silence), hearts above them when the sound opens up */}
      {[-400, -120, 300, 1520, 2150].map((x, i) => <g key={i}>
        <Character look={i === 2 ? CHIEF : RESCUER} pose={{ aR: [40 + Math.sin(f * 0.15 * move + i) * 20, 30], aL: [30, 40], lean: 10 + Math.sin(f * 0.15 * move + i) * 6, look: [1, 0.4], mouth: "flat", facing: (i % 2 ? -1 : 1) as 1 | -1 }} x={x} y={g + 40} rim={COLD} s={0.85} />
        <line x1={x + (i % 2 ? -50 : 50)} y1={g - 180} x2={x + (i % 2 ? -70 : 70)} y2={g + 70} stroke="#3a3a44" strokeWidth={5} />
        {hearts > 0 && <HeartIcon x={x} y={g - 420} f={f + i * 5} bpm={95 + i * 6} on={hearts} />}
      </g>)}
      {/* Mia */}
      <Character look={MIA_SNOW} pose={mia} x={520} y={g + 40} rim={COLD} s={0.92} />
      {mia.mouth !== "smile" && mia.tears && [0, 1].map(k => <circle key={k} cx={520 + 24 + k * 30} cy={g + 40 - 330 + ((f * 3 + k * 20) % 40)} r={5} fill="#9ad0ff" />)}
      {/* the hero */}
      <Character look={{ ...HERO_SNOW, headphones: heroHp ? "head" : "neck" }} pose={heroPose} x={dig > 0 ? leoX - 140 : 900} y={g + 40} rim={COLD} />
      {/* Leo dug out */}
      {leo > 0 && <g><Glow x={leoX} y={g} r={200} color="#fff6e0" o={0.5 * leo} /><Character look={LEO} pose={{ eyes: leo > 0.7 ? 1 : 0.2, mouth: leo > 0.7 ? "o" : "flat", aR: [150, 20], look: [-1, -0.5], facing: -1 }} x={leoX} y={g + 220 - leo * 200} rim={COLD} /></g>}
      {dig > 0 && Array.from({ length: 16 }, (_, i) => { const t = ((f * 2 + i * 7) % 40) / 40; return <circle key={i} cx={leoX - 60 + (rnd(i, 1) - 0.3) * 200 * t} cy={g - 20 - Math.sin(t * Math.PI) * 140} r={8 + rnd(i, 2) * 10} fill="#fff" opacity={1 - t} />; })}

    </Layer>
  </>;
};
export const Hospital: React.FC<{ f: number }> = ({ f }) => {
  const g = 880;
  return <>
    <Layer depth={0.75}>
      <Wallpaper x={-600} y={-300} w={W + 1200} h={g + 300} base="#cfe0dc" ink="#a8c8c0" kind="stripe" o={0.1} />
      <rect x={1180} y={180} width={520} height={420} fill="#e8f0ff" stroke="#f8f8f8" strokeWidth={18} /><line x1={1440} y1={180} x2={1440} y2={600} stroke="#f8f8f8" strokeWidth={10} />
      {Array.from({ length: 30 }, (_, i) => <circle key={i} cx={1190 + rnd(i, 1) * 500} cy={190 + ((rnd(i, 2) * 400 + f * 1.5) % 400)} r={3} fill="#fff" />)}
      <Shaft pts={[[1180, 200], [1700, 200], [1300, 1100], [500, 1100]]} color="#fff8e8" o={0.35} blur={24} from={[1440, 200]} to={[900, 1100]} />
      <rect x={200} y={260} width={70} height={120} rx={10} fill="#8a9aa8" /><path d="M235 380 L235 600" stroke="#8a9aa8" strokeWidth={4} /><rect x={160} y={600} width={150} height={10} fill="#8a9aa8" />
      <AO x={-600} y={g - 120} w={W + 1200} h={120} dir="up" o={0.25} />
    </Layer>
    <Layer depth={1}>
      <rect x={-600} y={g} width={W + 1200} height={400} fill="#b8c8c4" /><Noise x={-600} y={g} w={W + 1200} h={400} freq={0.6} o={0.15} />
      <rect x={380} y={700} width={720} height={60} rx={14} fill="#f4f6f8" /><rect x={360} y={760} width={760} height={30} fill="#8a9aa8" /><rect x={380} y={790} width={14} height={90} fill="#6a7a88" /><rect x={1086} y={790} width={14} height={90} fill="#6a7a88" />
      <rect x={360} y={560} width={40} height={200} rx={10} fill="#8a9aa8" />
      <Character look={{ ...HERO, bandage: true, headphones: false }} pose={{ lL: [90, 90], lR: [86, 86], mouth: f > 250 ? "smile" : "flat", look: [1, 0], brow: 0.2, aR: [20, 40] }} x={700} y={868} rim={{ dx: 4, dy: -3, color: "#fff4e0" }} />
      <Character look={MIA} pose={{ mouth: "smile", look: [-1, 0], facing: -1, aL: [30, 40] }} x={1300} y={g} rim={{ dx: -4, dy: -3, color: "#fff4e0" }} />
      <Character look={{ ...LEO, scale: 0.66 }} pose={{ mouth: "grin", look: [-1, -0.3], facing: -1, aR: [150, 30], hands: "open" }} x={1480} y={g} rim={{ dx: -4, dy: -3, color: "#fff4e0" }} />
    </Layer>
  </>;
};
