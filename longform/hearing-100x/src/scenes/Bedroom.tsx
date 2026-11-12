// Scene world: the hero's bedroom (x 0..1920) and, through the wall at x≈0, the neighbour's flat (x -1920..0).
// xray 0..1 turns the neighbour's flat into the "sound view" (cyan wireframe + a glowing heart).
import React from "react";
import { Layer, W, H, rnd, sat, lerp } from "../engine/core";
import { Glow, Shaft, Rain, PaneDrops, Bokeh } from "../engine/fx";
import { Wood, Wallpaper, AO, Noise } from "../engine/tex";
import { Character } from "../chars/Rig";
import { HERO_PJ, NEIGHBOUR } from "../chars/cast";

const FLOOR = 860;
const Skyline: React.FC<{ f: number; day?: number }> = ({ f, day = 0 }) => (
  <g>
    <defs><linearGradient id="nightsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#0d1430" /><stop offset="0.6" stopColor="#2a2350" /><stop offset="1" stopColor="#6a3a58" /></linearGradient></defs>
    <defs><linearGradient id="daysky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#6a9ad8" /><stop offset="0.6" stopColor="#f0b890" /><stop offset="1" stopColor="#ffd8a0" /></linearGradient></defs>
    <rect x={1000} y={120} width={820} height={600} fill="url(#nightsky)" />
    <rect x={1000} y={120} width={820} height={600} fill="url(#daysky)" opacity={day} />
    {day > 0 && <Glow x={1560} y={560} r={360} color="#fff0c0" o={0.9 * day} />}
    <Glow x={1500} y={700} r={520} color="#ff8a5a" o={0.35} />
    {Array.from({ length: 16 }, (_, i) => { const x = 1000 + i * 54 + rnd(i, 1) * 20, h = 120 + rnd(i, 2) * 260, w = 40 + rnd(i, 3) * 40; return <g key={i}>
      <rect x={x} y={720 - h} width={w} height={h} fill={i % 2 ? "#141428" : "#1b1a34"} />
      {Array.from({ length: 12 }, (_, k) => rnd(i * 30 + k, 4) > 0.55 ? <rect key={k} x={x + 6 + (k % 3) * (w / 3.2)} y={720 - h + 12 + Math.floor(k / 3) * 26} width={7} height={11} fill={rnd(i * 30 + k, 5) > 0.5 ? "#ffcf7a" : "#9ec8ff"} opacity={0.85} /> : null)}
    </g>; })}
    <Bokeh x={1020} y={400} w={780} h={320} n={22} seed={3} f={f} />
    <Rain f={f} x={1000} y={120} w={820} h={600} n={140} o={0.28 * (1 - day)} />
  </g>
);

export const Bedroom: React.FC<{ f: number; eyes: number; look: number[]; brow?: number; mouth?: any; xray?: number; heart?: number; heartOn?: number; headTurn?: number; beats?: number[]; day?: number; lying?: boolean; children?: React.ReactNode; clock?: string; selfScan?: number; heroHp?: boolean }> = ({ f, eyes, look, brow = 0, mouth = "flat", xray = 0, heart = 0, heartOn = 1, headTurn = 0, beats = [], day = 0, lying = true, children, clock, selfScan = 0, heroHp = false }) => {
  const rings = beats.filter(b => f >= b && f < b + 60).map(b => ({ r: 40 + (f - b) * 22, o: 1 - (f - b) / 60 }));
  const rim = { dx: 0, dy: -4, color: "#ffb36a" };
  const cyan = "#5ae0ff";
  return <>
    {/* far: the city through the window */}
    <Layer depth={0.82}><Skyline f={f} day={day} /></Layer>
    {/* the rooms */}
    <Layer depth={1}>
      <defs>
        <linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#1a1830" /><stop offset="1" stopColor="#2a2340" /></linearGradient>
        <linearGradient id="floorG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#2a1f2a" /><stop offset="1" stopColor="#120d14" /></linearGradient>
        <linearGradient id="nwall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#2a2220" /><stop offset="1" stopColor="#3a2e28" /></linearGradient>
      </defs>
      {/* hero room wall with window cut-out */}
      <mask id="winmask"><rect x={0} y={0} width={W} height={H} fill="#fff" /><rect x={1150} y={170} width={500} height={470} fill="#000" /></mask>
      <g mask="url(#winmask)">
        <Wallpaper x={40} y={0} w={W} h={FLOOR} base="#1c1932" ink="#3e3868" kind="diamond" o={0.22} />
        <AO x={40} y={0} w={W} h={90} dir="down" o={0.55} />
        <AO x={40} y={FLOOR - 120} w={W} h={120} dir="up" o={0.5} />
        <AO x={40} y={0} w={120} h={FLOOR} dir="right" o={0.5} />
        {/* projected window light on the back wall left of the window (moonlight through the panes) */}
        <g style={{ mixBlendMode: "screen", filter: "blur(6px)" }} opacity={0.09}><path d="M760 520 L1080 470 L1080 830 L760 860 Z" fill="#8ab0ff" /><path d="M915 497 L925 496 L925 845 L915 846 Z M760 690 L1080 650 L1080 660 L760 700 Z" fill="#000" /></g>
      </g>
      {/* crown + skirting */}
      <rect x={40} y={0} width={W} height={18} fill="#14122a" /><rect x={40} y={FLOOR - 26} width={W} height={26} fill="#15132a" /><rect x={40} y={FLOOR - 28} width={W} height={4} fill="#3a3460" />
      {/* ceiling lamp */}
      <line x1={760} y1={0} x2={760} y2={60} stroke="#0a0912" strokeWidth={4} /><path d="M710 60 L810 60 L790 100 L730 100 Z" fill="#0f0d1a" />
      {/* fairy lights along the top */}
      <path d={`M90 70 Q300 120 520 74 Q760 128 1000 78`} stroke="#0a0912" strokeWidth={2} fill="none" />
      {Array.from({ length: 18 }, (_, i) => { const u = i / 17, xx = 90 + u * 910, yy = 76 + Math.sin(u * Math.PI * 4) * 22 + 10; const on = 0.55 + 0.45 * Math.sin(f * 0.07 + i * 1.7); return <g key={i}><circle cx={xx} cy={yy} r={5} fill="#ffd38a" opacity={on} /><Glow x={xx} y={yy} r={34} color="#ffb84a" o={0.35 * on} /></g>; })}
      {/* window frame, mullions, sill, curtains */}
      <rect x={1140} y={160} width={520} height={490} fill="none" stroke="#0c0b16" strokeWidth={22} /><rect x={1151} y={171} width={498} height={468} fill="none" stroke="#3a3660" strokeWidth={2} opacity={0.8} />
      <line x1={1400} y1={170} x2={1400} y2={640} stroke="#0c0b16" strokeWidth={14} /><line x1={1150} y1={400} x2={1650} y2={400} stroke="#0c0b16" strokeWidth={12} />
      <rect x={1120} y={640} width={560} height={22} fill="#15131f" />
      <PaneDrops f={f} x={1150} y={170} w={500} h={470} n={55} />
      <path d={`M1100 120 Q1130 400 1120 760 L1040 760 Q1070 420 1050 120 Z`} fill="#2c2240" /><path d={`M1700 120 Q1680 420 1720 760 L1800 760 Q1760 400 1780 120 Z`} fill="#2c2240" />
      {[1062, 1084, 1712, 1740, 1764].map((x, i) => <path key={i} d={`M${x} 130 Q${x + 8} 440 ${x + (i < 2 ? 4 : 6)} 750`} stroke="#18122a" strokeWidth={6} fill="none" opacity={0.7} />)}
      <AO x={1040} y={120} w={90} h={640} dir="left" o={0.35} />
      <rect x={1030} y={110} width={790} height={16} rx={8} fill="#0e0c18" />
      {/* desk corner (right) */}
      <rect x={1700} y={560} width={260} height={18} fill="#2a2030" /><rect x={1712} y={578} width={14} height={282} fill="#1a1420" /><rect x={1930} y={578} width={14} height={282} fill="#1a1420" />
      <path d="M1730 560 L1840 560 L1830 470 L1740 470 Z" fill="#14121c" /><path d="M1736 474 L1834 474 L1830 548 L1740 548 Z" fill="#1e2a3a" />
      <circle cx={1820} cy={540} r={3} fill="#5aff8a" opacity={0.4 + 0.6 * (Math.floor(f / 20) % 2)} />
      <path d="M1880 560 L1880 440 L1920 400" stroke="#14121c" strokeWidth={8} fill="none" /><path d="M1900 380 L1950 410 L1930 440 L1880 412 Z" fill="#1a1622" />
      <rect x={1860} y={530} width={30} height={30} rx={4} fill="#c86a4a" /><path d="M1890 538 Q1902 545 1890 552" stroke="#c86a4a" strokeWidth={4} fill="none" />
      <path d="M1760 640 Q1770 600 1800 600 L1830 600 L1830 760 L1770 760 Z" fill="#1a1622" /><path d="M1772 610 Q1800 580 1828 612 L1826 700 Q1800 690 1774 700 Z" fill="#c8862a" opacity={0.85} />
      {/* guitar leaning on the wall (left) */}
      <g transform="translate(120 860) rotate(-14)"><ellipse cx={0} cy={-90} rx={62} ry={74} fill="#8a4a2a" /><ellipse cx={0} cy={-170} rx={46} ry={52} fill="#8a4a2a" /><circle cx={0} cy={-130} r={16} fill="#1a0e0a" /><rect x={-9} y={-420} width={18} height={250} fill="#2a1a12" /><rect x={-14} y={-450} width={28} height={40} rx={4} fill="#1a100c" />{[-4, 0, 4].map(k => <line key={k} x1={k} y1={-440} x2={k} y2={-60} stroke="#d8d0c0" strokeWidth={1} opacity={0.6} />)}</g>
      {/* cork board with notes */}
      <rect x={960} y={260} width={150} height={110} fill="#6a4a2a" stroke="#1a1218" strokeWidth={6} />
      {[[975, 275, "#f0e08a"], [1030, 285, "#8ad0f0"], [990, 320, "#f0a0b8"], [1050, 325, "#ffffff"]].map(([x, y, c], i) => <g key={i}><rect x={+x} y={+y} width={42} height={34} fill={c as string} transform={`rotate(${(i % 2 ? 6 : -5)} ${+x + 20} ${+y + 16})`} /><circle cx={+x + 21} cy={+y + 3} r={3} fill="#d83a3a" /></g>)}
      {/* window sill plants + curtain folds */}
      <rect x={1180} y={600} width={46} height={40} rx={4} fill="#a85a3a" /><path d="M1203 600 Q1180 550 1196 520 Q1206 560 1203 600 Z M1203 600 Q1226 548 1214 528 Q1206 570 1203 600 Z" fill="#2a5a3a" />
      <rect x={1580} y={606} width={40} height={34} rx={4} fill="#d8d0c0" /><circle cx={1600} cy={588} r={22} fill="#3a6a4a" /><circle cx={1588} cy={596} r={14} fill="#2a5a3a" />
      {/* posters + shelf + plant */}
      <rect x={560} y={210} width={170} height={230} fill="#2c2a48" stroke="#0e0c18" strokeWidth={8} /><circle cx={645} cy={300} r={46} fill="#e86a4a" opacity={0.55} /><path d="M580 420 L645 330 L710 420 Z" fill="#3a6aa8" opacity={0.6} />
      <rect x={780} y={250} width={130} height={170} fill="#2c3a4a" stroke="#0e0c18" strokeWidth={8} /><path d="M800 400 Q845 300 890 400" stroke="#f0c040" strokeWidth={6} fill="none" opacity={0.6} />
      <rect x={180} y={300} width={300} height={14} fill="#14121e" />
      {[0, 1, 2, 3, 4, 5, 6].map(k => <rect key={k} x={190 + k * 26 + (k > 4 ? 30 : 0)} y={300 - 50 - (k % 3) * 8} width={20} height={50 + (k % 3) * 8} fill={["#3a2a4a", "#4a3a2a", "#2a3a4a"][k % 3]} />)}
      <path d="M440 300 Q430 240 460 220 Q470 260 455 300 Z M455 300 Q480 230 500 240 Q480 270 465 300 Z" fill="#1e3a2a" />
      {/* floor */}
      <Wood x={40} y={FLOOR} w={W} h={H - FLOOR + 200} color="#2a1c1e" rows={9} />
      <AO x={40} y={FLOOR} w={W} h={70} dir="down" o={0.6} />
      <ellipse cx={700} cy={960} rx={560} ry={70} fill="#3a2a4a" /><ellipse cx={700} cy={960} rx={520} ry={58} fill="none" stroke="#5a4a6a" strokeWidth={6} strokeDasharray="18 10" /><ellipse cx={700} cy={960} rx={440} ry={44} fill="none" stroke="#2a1e36" strokeWidth={10} />
      {/* window light patch on the floor */}
      <g style={{ mixBlendMode: "screen" }} opacity={0.22}><path d="M1050 880 L1500 880 L1380 1060 L780 1060 Z" fill="#9ab8ff" /><path d="M1270 880 L1282 880 L1100 1060 L1086 1060 Z M920 960 L1450 960 L1440 975 L905 975 Z" fill="#000" /></g>
      {/* sneakers, clothes on the floor */}
      <g transform="translate(1250 900)"><path d="M0 0 Q30 -26 70 -10 L76 8 L0 10 Z" fill="#e8e4dc" /><rect x={0} y={6} width={78} height={8} rx={4} fill="#c83a3a" /><path d="M90 6 Q120 -20 160 -4 L166 14 L90 16 Z" fill="#dcd8d0" /><rect x={90} y={12} width={78} height={8} rx={4} fill="#c83a3a" /></g>
      <path d="M140 905 Q200 870 280 900 Q320 925 250 935 Q170 945 140 905 Z" fill="#3a5a7a" />
      {/* contact shadows */}
      <ellipse cx={680} cy={866} rx={430} ry={26} fill="#000" opacity={0.55} style={{ filter: "blur(10px)" }} />
      <ellipse cx={1145} cy={866} rx={80} ry={14} fill="#000" opacity={0.5} style={{ filter: "blur(8px)" }} />
      {/* bed */}
      <rect x={280} y={560} width={60} height={300} rx={14} fill="#1a1422" />
      <rect x={300} y={700} width={760} height={160} rx={10} fill="#1e1828" />
      <rect x={320} y={672} width={730} height={40} rx={16} fill="#3a3450" />
      <ellipse cx={420} cy={672} rx={95} ry={32} fill="#cfc8e0" /><ellipse cx={420} cy={664} rx={80} ry={18} fill="#e8e2f4" opacity={0.6} />
      {/* the hero, lying on his back, head on the pillow */}
      {lying && <g transform={`rotate(${headTurn} 410 668)`}><Character look={{ ...HERO_PJ, headphones: heroHp ? "head" : false }} pose={{ eyes, look, brow, mouth, lL: [0, 0], lR: [0, 0], aL: [10, 10], aR: [-4, 6], headSpin: 90 }} x={772} y={676} rot={-90} rim={rim} /></g>}
      {!lying && <path d={`M470 690 Q600 660 760 676 Q900 650 1050 676 L1062 712 Q760 735 470 712 Z`} fill="#7a2e3e" />}
      {children}
      {/* blanket over the body */}
      {lying && <g>
      <path d={`M470 640 Q520 610 600 625 Q700 600 820 618 Q940 600 1050 630 L1062 712 Q760 735 470 712 Z`} fill="#7a2e3e" />
      <path d={`M470 640 Q520 610 600 625 Q700 600 820 618 Q940 600 1050 630 L1052 646 Q930 620 820 636 Q700 618 600 642 Q520 628 476 656 Z`} fill="#b84a5a" opacity={0.7} />
      {[600, 760, 920].map(x => <path key={x} d={`M${x} ${628} Q${x + 30} 670 ${x + 10} 712`} stroke="#5a1e2c" strokeWidth={5} fill="none" opacity={0.6} />)}
      </g>}
      {/* the hero hearing his own body: an x-ray of heart, vessels and joints under the blanket */}
      {selfScan > 0 && <g opacity={selfScan} style={{ filter: "drop-shadow(0 0 6px #5ae0ff)" }}>
        <path d="M470 660 L780 660 M470 676 L780 676" stroke="#5ae0ff" strokeWidth={2} opacity={0.5} />
        {[[520, 650, 760, 640], [520, 690, 760, 700], [560, 668, 1000, 650], [560, 668, 1000, 690]].map(([x1, y1, x2, y2], i) => <path key={i} d={`M${x1} ${y1} Q${(x1 + x2) / 2} ${y1 + (i % 2 ? 14 : -14)} ${x2} ${y2}`} stroke="#ff4a6a" strokeWidth={4} fill="none" strokeDasharray="14 10" strokeDashoffset={-f * 3} opacity={0.8} />)}
        {[[760, 650], [900, 668], [1000, 660]].map(([x, y], i) => <circle key={i} cx={x} cy={y} r={11} fill="none" stroke="#5ae0ff" strokeWidth={3} opacity={0.6 + 0.4 * Math.sin(f * 0.3 + i)} />)}
        {(() => { const b = Math.max(0, Math.sin(f * 0.22)) ** 8; return <g><Glow x={555} y={668} r={70 + b * 60} color="#ff3a5a" o={0.4 + b * 0.5} /><path transform={`translate(555 668) scale(${0.8 + b * 0.4})`} d="M0 18 C -26 -2 -22 -26 -6 -24 C 0 -23 0 -18 0 -14 C 0 -18 0 -23 6 -24 C 22 -26 26 -2 0 18 Z" fill="#ff4a6a" /></g>; })()}
      </g>}
      {/* nightstand, clock, headphones */}
      <rect x={1080} y={700} width={130} height={160} rx={6} fill="#1a1524" /><rect x={1094} y={760} width={102} height={6} fill="#0c0a12" />
      <rect x={1100} y={652} width={70} height={46} rx={8} fill="#0c0a12" />
      <text x={1135} y={684} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={24} fill="#ff3a3a">{clock ?? (day > 0.5 ? "7:12" : "3:00")}</text>
      <Glow x={1135} y={676} r={70} color="#ff2a2a" o={0.35} />
      <rect x={1100} y={700} width={10} height={4} fill="#5affb0" opacity={0.6} />
      <path d="M1180 690 Q1196 640 1214 690" stroke="#2a2a34" strokeWidth={7} fill="none" /><ellipse cx={1180} cy={690} rx={10} ry={8} fill="#f0a83a" /><ellipse cx={1214} cy={690} rx={10} ry={8} fill="#f0a83a" />
      {/* light from the window: cool moon + warm street lamp shafts across the bed and floor */}
      <Shaft pts={[[1150, 180], [1650, 180], [900, 1040], [260, 1040]]} color="#8ab0ff" o={0.16} blur={26} from={[1400, 180]} to={[700, 1040]} />
      <Shaft pts={[[1150, 420], [1400, 420], [980, 900], [560, 900]]} color="#ffb36a" o={0.2} blur={20} from={[1270, 420]} to={[760, 900]} />
      <Glow x={1400} y={400} r={420} color="#9ab8ff" o={0.15} />
      {day > 0 && <g opacity={day}><Shaft pts={[[1150, 170], [1650, 170], [1100, 1060], [300, 1060]]} color="#ffd8a0" o={0.45} blur={24} from={[1400, 170]} to={[700, 1060]} /><rect x={-2000} y={-200} width={4200} height={1500} fill="#ffb070" opacity={0.12} style={{ mixBlendMode: "screen" }} /></g>}
      {Array.from({ length: 40 }, (_, i) => { const t = (f * 0.4 + rnd(i, 1) * 400) % 400; return <circle key={i} cx={lerp(1350, 700, rnd(i, 2)) + Math.sin(f * 0.02 + i) * 12} cy={240 + rnd(i, 3) * 600 - t * 0.2} r={1.2 + rnd(i, 4) * 1.6} fill="#dfe8ff" opacity={0.25 + 0.3 * Math.sin(f * 0.05 + i)} />; })}

      {/* the dividing wall (bricks) */}
      <rect x={-40} y={0} width={80} height={FLOOR} fill="#16121c" />
      {/* the neighbour's flat */}
      <g opacity={1 - xray * 0.85}>
        <Wallpaper x={-1900} y={0} w={1860} h={FLOOR} base="#2e2420" ink="#6a5038" kind="floral" o={0.25} />
        <AO x={-1900} y={0} w={1860} h={90} dir="down" o={0.5} /><AO x={-1900} y={FLOOR - 120} w={1860} h={120} dir="up" o={0.5} />
        <Wood x={-1900} y={FLOOR} w={1860} h={300} color="#2a1a14" rows={8} seed={5} />
        {[[-700, 240, 180, 140], [-480, 270, 110, 90], [-860, 290, 90, 120]].map(([x, y, w, h], i) => <g key={i}><rect x={x} y={y} width={w} height={h} fill="#3a3028" stroke="#a88a50" strokeWidth={6} /><circle cx={x + w / 2 - 14} cy={y + h / 2} r={14} fill="#1a1412" /><circle cx={x + w / 2 + 14} cy={y + h / 2 + 4} r={12} fill="#1a1412" /></g>)}
        {/* armchair, dresser with radio, standing lamp */}
        <path d="M-1700 860 L-1700 700 Q-1700 640 -1640 640 L-1500 640 Q-1440 640 -1440 700 L-1440 860 Z" fill="#5a2e2a" /><rect x={-1730} y={720} width={70} height={140} rx={20} fill="#4a2420" /><rect x={-1480} y={720} width={70} height={140} rx={20} fill="#4a2420" />
        <rect x={-1380} y={680} width={220} height={180} fill="#3a2418" /><rect x={-1360} y={640} width={110} height={44} rx={8} fill="#6a4a2a" /><circle cx={-1330} cy={662} r={12} fill="#2a1a10" /><rect x={-1310} y={652} width={50} height={20} fill="#c8a870" opacity={0.6} />
        <line x1={-1100} y1={860} x2={-1100} y2={560} stroke="#1a120c" strokeWidth={6} /><path d="M-1150 560 L-1050 560 L-1070 500 L-1130 500 Z" fill="#a87a4a" />
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
