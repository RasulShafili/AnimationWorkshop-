// Chapter 5: TV news in the living room, the collapsed-building rescue site (with the sound view under the rubble),
// and the "Human Sonar" headline.
import React from "react";
import { Layer, W, H, rnd, lerp, sat } from "../engine/core";
import { Glow, Shaft, Bokeh } from "../engine/fx";
import { Noise, AO, Wallpaper, Wood, Bricks } from "../engine/tex";
import { Character, walkPose } from "../chars/Rig";
import { HERO, HERO_HP, DAD, RESCUER, CHIEF, GIRL } from "../chars/cast";
import { talkM } from "./School";
const DUSK = { dx: 4, dy: -3, color: "#ffb86a" };

export const LivingRoom: React.FC<{ f: number }> = ({ f }) => {
  const g = 880, shake = Math.sin(f * 2.1) * 6;
  return <>
    <Layer depth={0.8}>
      <Wallpaper x={-600} y={-300} w={W + 1200} h={g + 300} base="#2a2a3a" ink="#4a4a6a" kind="stripe" o={0.12} />
      <AO x={-600} y={-300} w={W + 1200} h={400} dir="down" o={0.6} />
      <g transform="translate(-380 0)"><rect x={560} y={260} width={800} height={460} rx={14} fill="#0a0a0e" /><rect x={580} y={280} width={760} height={420} fill="#2a3a5a" />
      {/* the news footage: shaking buildings + ticker */}
      <g transform={`translate(${shake} 0)`}><clipPath id="tvc"><rect x={580} y={280} width={760} height={420} /></clipPath><g clipPath="url(#tvc)">
        <rect x={580} y={280} width={760} height={420} fill="#c8a07a" />{Array.from({ length: 7 }, (_, i) => <rect key={i} x={600 + i * 110} y={420 + (i % 3) * 30} width={90} height={300} fill="#6a5a50" transform={`rotate(${(i % 2 ? 6 : -5) * sat(f / 40)} ${645 + i * 110} 700)`} />)}
        <rect x={580} y={560} width={760} height={140} fill="#8a7a6a" opacity={0.6} /><Noise x={580} y={280} w={760} h={420} freq={0.9} o={0.35} />
      </g></g>
      <rect x={580} y={600} width={760} height={100} fill="#c81e1e" /><text x={600} y={665} fontFamily="Inter" fontWeight={900} fontSize={46} fill="#fff">BREAKING: 6.9 EARTHQUAKE</text>
      <Glow x={960} y={490} r={700} color="#8ab0ff" o={0.35} />
      <rect x={700} y={720} width={520} height={160} fill="#1a1414" /></g>
      <rect x={1800} y={400} width={140} height={360} fill="#2a1e18" /><path d="M1770 400 L1970 400 L1920 300 L1820 300 Z" fill="#c8a870" /><Glow x={1870} y={380} r={260} color="#ffd08a" o={0.3} />
    </Layer>
    <Layer depth={1}>
      <Wood x={-600} y={g} w={W + 1200} h={400} color="#2a1e1a" rows={6} />
      {/* sofa from behind + the two of them watching */}
      {/* sofa seen from the side, facing the TV on the left */}
      <rect x={1160} y={560} width={70} height={320} rx={26} fill="#3a2030" />
      <path d="M1180 700 L1640 700 L1640 880 L1180 880 Z" fill="#4a2a3a" /><rect x={1600} y={640} width={80} height={240} rx={30} fill="#3a2030" />
      <Character look={DAD} pose={{ lL: [80, 80], lR: [76, 76], mouth: "o", brow: 0.8, look: [1, 0], facing: -1, aR: [40, 50] }} x={1300} y={g - 10} rim={{ dx: -4, dy: -3, color: "#9ec8ff" }} />
      <Character look={HERO} pose={{ lL: [80, 80], lR: [76, 76], mouth: "worried", brow: 0.6, look: [1, 0], facing: -1, aR: [30, 60] }} x={1520} y={g - 10} rim={{ dx: -4, dy: -3, color: "#9ec8ff" }} />
      <path d="M1180 700 L1640 700 L1640 730 L1180 730 Z" fill="#6a3a50" />
    </Layer>
  </>;
};

// collapsed buildings at dusk; xray shows the survivors' heartbeats under the slabs
export const Rubble: React.FC<{ f: number; freeze: number; xray: number; beat: number; dig: number; girl: number; chiefTalk: boolean; heroKneel: number; cheer: number }> = ({ f, freeze, xray, beat, dig, girl, chiefTalk, heroKneel, cheer }) => {
  const g = 860, cyan = "#5ae0ff", moving = 1 - freeze;
  const slabs = Array.from({ length: 14 }, (_, i) => ({ x: -300 + i * 190 + rnd(i, 1) * 60, y: g - 120 - rnd(i, 2) * 220, w: 220 + rnd(i, 3) * 120, h: 40 + rnd(i, 4) * 30, r: (rnd(i, 5) - 0.5) * 50 }));
  const survivors = [[560, g + 150], [980, g + 190], [1360, g + 140]];
  return <>
    <Layer depth={0.35}>
      <defs><linearGradient id="dsk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#4a3a6a" /><stop offset="0.6" stopColor="#e88a5a" /><stop offset="1" stopColor="#ffc88a" /></linearGradient></defs>
      <rect x={-1000} y={-400} width={W + 2000} height={g + 400} fill="url(#dsk)" />
      <Glow x={1400} y={g - 100} r={600} color="#ffd890" o={0.6} />
      {Array.from({ length: 10 }, (_, i) => <path key={i} d={`M${-800 + i * 330} ${g} L${-800 + i * 330} ${g - 300 - rnd(i, 7) * 200} L${-700 + i * 330} ${g - 260 - rnd(i, 8) * 160} L${-560 + i * 330} ${g - 330 - rnd(i, 9) * 120} L${-540 + i * 330} ${g} Z`} fill="#5a3a4a" opacity={0.7} />)}
    </Layer>
    <Layer depth={0.7}>
      {/* standing ruined facade with empty windows + an excavator + floodlights */}
      <path d="M-200 860 L-200 300 L120 260 L200 420 L340 380 L360 860 Z" fill="#6a5a58" /><Bricks x={-200} y={260} w={560} h={600} color="#6a5a58" mortar="#3a3030" o={0.35} />
      {[0, 1, 2].map(k => <rect key={k} x={-150 + k * 160} y={480} width={90} height={110} fill="#1a1416" />)}
      <g transform="translate(1600 860)"><rect x={0} y={-140} width={260} height={110} rx={10} fill="#e8b82a" /><rect x={30} y={-230} width={120} height={100} fill="#e8b82a" /><rect x={45} y={-215} width={90} height={60} fill="#3a5a7a" /><path d={`M150 -170 L360 ${-300 + moving * Math.sin(f * 0.06) * 30} L420 -120`} stroke="#d8a82a" strokeWidth={24} fill="none" /><rect x={-10} y={-40} width={290} height={40} rx={20} fill="#2a2a2a" /></g>
      {[[-500, 300], [2300, 260]].map(([x, h], i) => <g key={i}><line x1={x} y1={860} x2={x} y2={860 - h} stroke="#1a1a1a" strokeWidth={10} /><rect x={x - 50} y={860 - h - 40} width={100} height={50} fill="#1a1a1a" /><Glow x={x} y={860 - h - 10} r={500} color="#fff2d0" o={0.45} /></g>)}
    </Layer>
    <Layer depth={1}>
      {/* ground + rubble slabs */}
      <rect x={-1000} y={g} width={W + 2000} height={600} fill="#4a3e3a" /><Noise x={-1000} y={g} w={W + 2000} h={600} freq={0.6} o={0.5} />
      {slabs.map((s, i) => <g key={i} transform={`rotate(${s.r} ${s.x + s.w / 2} ${s.y + s.h / 2})`}><rect x={s.x} y={s.y} width={s.w} height={s.h} fill={["#8a8078", "#7a706a", "#968c84"][i % 3]} /><line x1={s.x + 20} y1={s.y + s.h / 2} x2={s.x + s.w - 30} y2={s.y + s.h / 2 + 6} stroke="#5a504a" strokeWidth={3} />{i % 3 === 0 && <line x1={s.x + s.w - 40} y1={s.y} x2={s.x + s.w - 10} y2={s.y - 50} stroke="#6a4a3a" strokeWidth={6} />}</g>)}
      <path d={`M-400 ${g} Q200 ${g - 160} 700 ${g - 60} Q1100 ${g - 190} 1500 ${g - 50} Q1900 ${g - 140} 2400 ${g} L2400 ${g + 600} L-400 ${g + 600} Z`} fill="#6a5e56" />
      <Noise x={-400} y={g - 200} w={2800} h={800} freq={0.9} o={0.4} />
      {/* the sound view under the rubble */}
      {xray > 0 && <g opacity={xray}>
        <rect x={-400} y={g - 40} width={2800} height={600} fill="#04101c" opacity={0.85} />
        {Array.from({ length: 12 }, (_, i) => <path key={i} d={`M${-300 + i * 230} ${g + 20 + (i % 3) * 60} l${180} ${(i % 2 ? 40 : -30)}`} stroke={cyan} strokeWidth={3} opacity={0.4} />)}
        {survivors.map(([x, y], i) => { const b = Math.max(0, Math.sin((f + i * 11) * 0.25)) ** 6 * beat; return <g key={i}>
          <circle cx={x} cy={y} r={40} fill="none" stroke={cyan} strokeWidth={3} /><path d={`M${x - 60} ${y + 70} q60 -50 120 0`} stroke={cyan} strokeWidth={3} fill="none" />
          <Glow x={x} y={y + 40} r={80 + b * 80} color="#ff3a5a" o={0.3 + b * 0.6} />
          <path transform={`translate(${x} ${y + 40}) scale(${0.9 + b * 0.5})`} d="M0 18 C -26 -2 -22 -26 -6 -24 C 0 -23 0 -18 0 -14 C 0 -18 0 -23 6 -24 C 22 -26 26 -2 0 18 Z" fill="#ff4a6a" />
          {[0, 1].map(k => { const t = ((f + i * 9 + k * 15) % 30) / 30; return <circle key={k} cx={x} cy={y + 40} r={40 + t * 260} fill="none" stroke={cyan} strokeWidth={2.5} opacity={(1 - t) * 0.8} />; })}
        </g>; })}
      </g>}
      {/* rescuers (they freeze for the silence), the chief, the hero */}
      {[[-60, 1], [1170, -1], [1290, -1], [1600, -1]].map(([x, fc], i) => { const walk = walkPose(f * 0.2 * moving + i, 0.6 * moving); const digK = dig > 0 && (i === 1 || i === 2); return <Character key={i} look={RESCUER} pose={{ ...walk, facing: fc as 1 | -1, mouth: cheer > 0.5 ? "grin" : "flat", look: [1, 0.3], ...(digK ? { lean: 30, aL: [90 + Math.sin(f * 0.5) * 30, 40], aR: [80 + Math.sin(f * 0.5 + 1) * 30, 40] } : {}), ...(cheer > 0.5 ? { aL: [170, 10], aR: [165, 10], hands: "open" as const } : {}) }} x={x} y={g - 40 + (i % 2) * 20} rim={DUSK} s={0.85} />; })}
      <Character look={CHIEF} pose={{ mouth: chiefTalk ? talkM(f, true) : "flat", aR: freeze > 0.2 ? [170, 20] : [10, 20], hands: "fist", look: [1, 0], brow: -0.4 }} x={180} y={g - 60} rim={DUSK} s={0.95} />
      <Character look={HERO} pose={heroKneel > 0 ? { lL: [95, 150], lR: [40, 120], bob: 78 * heroKneel, lean: 18, aL: [60, 40], aR: [30, 50], mouth: "flat", look: [0.6, 1], brow: 0.5 } : { mouth: "flat", look: [1, 0.3] }} x={720} y={g - 70} rim={DUSK} />
      {/* the girl being pulled out */}
      {girl > 0 && <g><Glow x={1000} y={g - 40} r={220} color="#fff2c8" o={0.5 * girl} /><Character look={GIRL} pose={{ aR: [170, 10], aL: [150, 20], hands: "open", mouth: girl > 0.8 ? "smile" : "o", look: [0, -1] }} x={1000} y={g + 260 - girl * 300} s={0.9} rim={DUSK} /></g>}
      {/* dust drifting (stops in the silence) */}
      {Array.from({ length: 60 }, (_, i) => { const tt = (f * (0.3 + 0.7 * moving) + rnd(i, 1) * 600) % 600; return <circle key={i} cx={-300 + rnd(i, 2) * 2600 + tt * 0.3} cy={g - 60 - rnd(i, 3) * 600 - tt * 0.15} r={2 + rnd(i, 4) * 3} fill="#ffe0b8" opacity={0.35} />; })}
      <rect x={-1000} y={-400} width={W + 2000} height={H + 800} fill="#e8b890" opacity={0.08} style={{ mixBlendMode: "screen" }} />
    </Layer>
  </>;
};

export const Headline: React.FC<{ f: number }> = ({ f }) => {
  const k = sat(f / 20), spin = (1 - k) * 25;
  return <svg width={W} height={H} style={{ position: "absolute" }}>
    <rect width={W} height={H} fill="#1a1a22" /><Glow x={960} y={540} r={800} color="#ffd8a0" o={0.25} />
    <g transform={`translate(960 540) rotate(${-4 + spin}) scale(${0.6 + k * 0.45}) translate(-560 -360)`}>
      <rect width={1120} height={720} fill="#f4efe2" /><Noise x={0} y={0} w={1120} h={720} freq={0.9} o={0.2} />
      <text x={560} y={80} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={44} fill="#1a1a1a" letterSpacing={6}>THE DAILY ECHO</text>
      <line x1={40} y1={104} x2={1080} y2={104} stroke="#1a1a1a" strokeWidth={4} />
      <text x={560} y={220} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={110} fill="#1a1a1a">THE HUMAN SONAR</text>
      <text x={560} y={290} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={36} fill="#3a3a3a">Teen hears three survivors under the rubble</text>
      <rect x={60} y={330} width={460} height={330} fill="#c8c0b0" /><g transform="translate(290 650) scale(0.75)"><Character look={HERO_HP} pose={{ mouth: "smile", look: [0, 0] }} x={0} y={0} /></g>
      {[0, 1, 2, 3, 4, 5, 6, 7].map(k => <rect key={k} x={560} y={350 + k * 38} width={500 - (k % 3) * 60} height={14} fill="#5a5a5a" opacity={0.6} />)}
    </g>
  </svg>;
};
