// Scene world: the hero's bedroom (x 0..1920) and, through the wall at x≈0, the neighbour's flat (x -1920..0).
// xray 0..1 turns the neighbour's flat into the "sound view" (cyan wireframe + a glowing heart).
import React from "react";
import { Layer, W, H, rnd, sat, lerp } from "../engine/core";
import { Glow, Shaft, Rain, PaneDrops, Bokeh } from "../engine/fx";
import { Character } from "../chars/Rig";
import { HERO_PJ, NEIGHBOUR } from "../chars/cast";

const FLOOR = 860;
const Skyline: React.FC<{ f: number }> = ({ f }) => (
  <g>
    <defs><linearGradient id="nightsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#0d1430" /><stop offset="0.6" stopColor="#2a2350" /><stop offset="1" stopColor="#6a3a58" /></linearGradient></defs>
    <rect x={1000} y={120} width={820} height={600} fill="url(#nightsky)" />
    <Glow x={1500} y={700} r={520} color="#ff8a5a" o={0.35} />
    {Array.from({ length: 16 }, (_, i) => { const x = 1000 + i * 54 + rnd(i, 1) * 20, h = 120 + rnd(i, 2) * 260, w = 40 + rnd(i, 3) * 40; return <g key={i}>
      <rect x={x} y={720 - h} width={w} height={h} fill={i % 2 ? "#141428" : "#1b1a34"} />
      {Array.from({ length: 12 }, (_, k) => rnd(i * 30 + k, 4) > 0.55 ? <rect key={k} x={x + 6 + (k % 3) * (w / 3.2)} y={720 - h + 12 + Math.floor(k / 3) * 26} width={7} height={11} fill={rnd(i * 30 + k, 5) > 0.5 ? "#ffcf7a" : "#9ec8ff"} opacity={0.85} /> : null)}
    </g>; })}
    <Bokeh x={1020} y={400} w={780} h={320} n={22} seed={3} f={f} />
    <Rain f={f} x={1000} y={120} w={820} h={600} n={140} o={0.28} />
  </g>
);

export const Bedroom: React.FC<{ f: number; eyes: number; look: number[]; brow?: number; mouth?: any; xray?: number; heart?: number; heartOn?: number; headTurn?: number; beats?: number[] }> = ({ f, eyes, look, brow = 0, mouth = "flat", xray = 0, heart = 0, heartOn = 1, headTurn = 0, beats = [] }) => {
  const rings = beats.filter(b => f >= b && f < b + 60).map(b => ({ r: 40 + (f - b) * 22, o: 1 - (f - b) / 60 }));
  const rim = { dx: 0, dy: -4, color: "#ffb36a" };
  const cyan = "#5ae0ff";
  return <>
    {/* far: the city through the window */}
    <Layer depth={0.82}><Skyline f={f} /></Layer>
    {/* the rooms */}
    <Layer depth={1}>
      <defs>
        <linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#1a1830" /><stop offset="1" stopColor="#2a2340" /></linearGradient>
        <linearGradient id="floorG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#2a1f2a" /><stop offset="1" stopColor="#120d14" /></linearGradient>
        <linearGradient id="nwall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#2a2220" /><stop offset="1" stopColor="#3a2e28" /></linearGradient>
      </defs>
      {/* hero room wall with window cut-out */}
      <path d={`M40 0 L${W} 0 L${W} ${FLOOR} L40 ${FLOOR} Z M1150 170 L1150 640 L1650 640 L1650 170 Z`} fill="url(#wall)" fillRule="evenodd" />
      {Array.from({ length: 24 }, (_, i) => <rect key={i} x={60 + i * 80} y={0} width={2} height={FLOOR} fill="#ffffff" opacity={0.025} />)}
      {/* window frame, mullions, sill, curtains */}
      <rect x={1140} y={160} width={520} height={490} fill="none" stroke="#0c0b16" strokeWidth={22} />
      <line x1={1400} y1={170} x2={1400} y2={640} stroke="#0c0b16" strokeWidth={14} /><line x1={1150} y1={400} x2={1650} y2={400} stroke="#0c0b16" strokeWidth={12} />
      <rect x={1120} y={640} width={560} height={22} fill="#15131f" />
      <PaneDrops f={f} x={1150} y={170} w={500} h={470} n={55} />
      <path d={`M1100 120 Q1130 400 1120 760 L1040 760 Q1070 420 1050 120 Z`} fill="#241c34" /><path d={`M1700 120 Q1680 420 1720 760 L1800 760 Q1760 400 1780 120 Z`} fill="#241c34" />
      <rect x={1030} y={110} width={790} height={16} rx={8} fill="#0e0c18" />
      {/* posters + shelf + plant */}
      <rect x={560} y={210} width={170} height={230} fill="#2c2a48" stroke="#0e0c18" strokeWidth={8} /><circle cx={645} cy={300} r={46} fill="#e86a4a" opacity={0.55} /><path d="M580 420 L645 330 L710 420 Z" fill="#3a6aa8" opacity={0.6} />
      <rect x={780} y={250} width={130} height={170} fill="#2c3a4a" stroke="#0e0c18" strokeWidth={8} /><path d="M800 400 Q845 300 890 400" stroke="#f0c040" strokeWidth={6} fill="none" opacity={0.6} />
      <rect x={180} y={300} width={300} height={14} fill="#14121e" />
      {[0, 1, 2, 3, 4, 5, 6].map(k => <rect key={k} x={190 + k * 26 + (k > 4 ? 30 : 0)} y={300 - 50 - (k % 3) * 8} width={20} height={50 + (k % 3) * 8} fill={["#3a2a4a", "#4a3a2a", "#2a3a4a"][k % 3]} />)}
      <path d="M440 300 Q430 240 460 220 Q470 260 455 300 Z M455 300 Q480 230 500 240 Q480 270 465 300 Z" fill="#1e3a2a" />
      {/* floor */}
      <rect x={40} y={FLOOR} width={W} height={H - FLOOR + 200} fill="url(#floorG)" />
      {Array.from({ length: 9 }, (_, i) => <line key={i} x1={40} y1={FLOOR + 14 + i * 26} x2={W} y2={FLOOR + 14 + i * 26} stroke="#000" strokeWidth={2} opacity={0.35} />)}
      {/* contact shadows */}
      <ellipse cx={680} cy={866} rx={430} ry={26} fill="#000" opacity={0.55} style={{ filter: "blur(10px)" }} />
      <ellipse cx={1145} cy={866} rx={80} ry={14} fill="#000" opacity={0.5} style={{ filter: "blur(8px)" }} />
      {/* bed */}
      <rect x={280} y={560} width={60} height={300} rx={14} fill="#1a1422" />
      <rect x={300} y={700} width={760} height={160} rx={10} fill="#1e1828" />
      <rect x={320} y={672} width={730} height={40} rx={16} fill="#3a3450" />
      <ellipse cx={420} cy={672} rx={95} ry={32} fill="#cfc8e0" /><ellipse cx={420} cy={664} rx={80} ry={18} fill="#e8e2f4" opacity={0.6} />
      {/* the hero, lying on his back, head on the pillow */}
      <g transform={`rotate(${headTurn} 410 668)`}><Character look={{ ...HERO_PJ, headphones: false }} pose={{ eyes, look, brow, mouth, lL: [0, 0], lR: [0, 0], aL: [10, 10], aR: [-4, 6], headSpin: 90 }} x={772} y={676} rot={-90} rim={rim} /></g>
      {/* blanket over the body */}
      <path d={`M470 640 Q520 610 600 625 Q700 600 820 618 Q940 600 1050 630 L1062 712 Q760 735 470 712 Z`} fill="#7a2e3e" />
      <path d={`M470 640 Q520 610 600 625 Q700 600 820 618 Q940 600 1050 630 L1052 646 Q930 620 820 636 Q700 618 600 642 Q520 628 476 656 Z`} fill="#b84a5a" opacity={0.7} />
      {[600, 760, 920].map(x => <path key={x} d={`M${x} ${628} Q${x + 30} 670 ${x + 10} 712`} stroke="#5a1e2c" strokeWidth={5} fill="none" opacity={0.6} />)}
      {/* nightstand, clock, headphones */}
      <rect x={1080} y={700} width={130} height={160} rx={6} fill="#1a1524" /><rect x={1094} y={760} width={102} height={6} fill="#0c0a12" />
      <rect x={1100} y={652} width={70} height={46} rx={8} fill="#0c0a12" />
      <text x={1135} y={684} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={24} fill="#ff3a3a">3:00</text>
      <Glow x={1135} y={676} r={70} color="#ff2a2a" o={0.35} />
      <path d="M1180 690 Q1196 640 1214 690" stroke="#2a2a34" strokeWidth={7} fill="none" /><ellipse cx={1180} cy={690} rx={10} ry={8} fill="#f0a83a" /><ellipse cx={1214} cy={690} rx={10} ry={8} fill="#f0a83a" />
      {/* light from the window: cool moon + warm street lamp shafts across the bed and floor */}
      <Shaft pts={[[1150, 180], [1650, 180], [900, 1040], [260, 1040]]} color="#8ab0ff" o={0.16} blur={26} from={[1400, 180]} to={[700, 1040]} />
      <Shaft pts={[[1150, 420], [1400, 420], [980, 900], [560, 900]]} color="#ffb36a" o={0.2} blur={20} from={[1270, 420]} to={[760, 900]} />
      <Glow x={1400} y={400} r={420} color="#9ab8ff" o={0.15} />
      {Array.from({ length: 40 }, (_, i) => { const t = (f * 0.4 + rnd(i, 1) * 400) % 400; return <circle key={i} cx={lerp(1350, 700, rnd(i, 2)) + Math.sin(f * 0.02 + i) * 12} cy={240 + rnd(i, 3) * 600 - t * 0.2} r={1.2 + rnd(i, 4) * 1.6} fill="#dfe8ff" opacity={0.25 + 0.3 * Math.sin(f * 0.05 + i)} />; })}

      {/* the dividing wall (bricks) */}
      <rect x={-40} y={0} width={80} height={FLOOR} fill="#16121c" />
      {/* the neighbour's flat */}
      <g opacity={1 - xray * 0.85}>
        <rect x={-1900} y={0} width={1860} height={FLOOR} fill="url(#nwall)" />
        {Array.from({ length: 30 }, (_, i) => <g key={i} opacity={0.08}><circle cx={-1880 + (i % 10) * 190} cy={80 + Math.floor(i / 10) * 260} r={14} fill="#c8a878" /></g>)}
        <rect x={-1900} y={FLOOR} width={1860} height={300} fill="#1a1412" />
        <rect x={-700} y={240} width={180} height={140} fill="#3a3028" stroke="#120e0c" strokeWidth={10} />
      </g>
      {/* neighbour bed + man (wireframe in the sound view) */}
      <g opacity={1}>
        <g opacity={1 - xray * 0.9}>
          <rect x={-300} y={560} width={56} height={300} rx={12} fill="#2a1e18" /><rect x={-1060} y={700} width={780} height={160} rx={10} fill="#2a201c" />
          <ellipse cx={-400} cy={672} rx={95} ry={32} fill="#d8ccb8" />
          <Character look={NEIGHBOUR} pose={{ eyes: 0.05, mouth: "flat", lL: [0, 0], lR: [0, 0], aL: [8, 8], aR: [-6, 6], facing: -1, headSpin: 90 }} x={-768} y={676} rot={90} />
          <path d={`M-470 640 Q-520 612 -600 626 Q-700 604 -820 620 Q-940 604 -1050 632 L-1062 712 Q-760 735 -470 712 Z`} fill="#4a5a6a" />
          <rect x={-1210} y={700} width={130} height={160} rx={6} fill="#2a201c" /><rect x={-1180} y={660} width={22} height={40} rx={4} fill="#a8d0e8" opacity={0.7} /><rect x={-1140} y={672} width={16} height={28} rx={3} fill="#e8a040" />
        </g>
        {xray > 0 && <g opacity={xray} style={{ filter: "drop-shadow(0 0 6px #5ae0ff)" }}>
          <rect x={-1900} y={0} width={1860} height={FLOOR + 220} fill="#06121e" opacity={0.85} />
          {Array.from({ length: 19 }, (_, i) => <line key={`v${i}`} x1={-1900 + i * 100} y1={0} x2={-1900 + i * 100} y2={FLOOR} stroke={cyan} strokeWidth={1} opacity={0.12} />)}
          {Array.from({ length: 9 }, (_, i) => <line key={`h${i}`} x1={-1900} y1={i * 100} x2={-40} y2={i * 100} stroke={cyan} strokeWidth={1} opacity={0.12} />)}
          <line x1={-1900} y1={FLOOR} x2={-40} y2={FLOOR} stroke={cyan} strokeWidth={2} opacity={0.5} />
          <rect x={-1060} y={700} width={780} height={160} rx={10} fill="none" stroke={cyan} strokeWidth={3} />
          <rect x={-300} y={560} width={56} height={300} rx={12} fill="none" stroke={cyan} strokeWidth={3} />
          <ellipse cx={-400} cy={672} rx={95} ry={32} fill="none" stroke={cyan} strokeWidth={3} />
          <path d={`M-470 640 Q-520 612 -600 626 Q-700 604 -820 620 Q-940 604 -1050 632 L-1062 712 Q-760 735 -470 712 Z`} fill="none" stroke={cyan} strokeWidth={3} />
          {/* the man as a glowing outline: head + shoulders above the blanket */}
          <circle cx={-406} cy={668} r={60} fill="none" stroke={cyan} strokeWidth={4} />
          <rect x={-1210} y={700} width={130} height={160} rx={6} fill="none" stroke={cyan} strokeWidth={3} />
        </g>}
        {heartOn > 0 && xray > 0 && rings.map((r, i) => <circle key={i} cx={-560} cy={656} r={r.r} fill="none" stroke={cyan} strokeWidth={3} opacity={r.o * xray} />)}
        {/* the heart: glowing pulse in his chest */}
        {heartOn > 0 && <g opacity={heartOn}>
          <Glow x={-560} y={660} r={90 + heart * 90} color="#ff3a5a" o={0.25 + heart * 0.55} />
          <path transform={`translate(-560 656) scale(${1 + heart * 0.35})`} d="M0 18 C -26 -2 -22 -26 -6 -24 C 0 -23 0 -18 0 -14 C 0 -18 0 -23 6 -24 C 22 -26 26 -2 0 18 Z" fill="#ff4a6a" />
        </g>}
      </g>
    </Layer>
  </>;
};
