// Police interview room at night: cold fluorescent lamp over a metal table, rain on the blinds, city bokeh,
// a cork board with case photos. Lina sits left (facing right), Detective Okafor stands right, leaning on the table.
import React from "react";
import { Layer } from "../engine/core";
import { Glow, Shaft, Rain, PaneDrops, Bokeh } from "../engine/fx";
import { Noise, AO } from "../engine/tex";
import { Character, Pose, SIT } from "../chars/Rig2";
import { LINA, OKAFOR } from "../chars/cast";

export const TABLE_Y = 712;              // table top
export const LINA_X = 700, LINA_ROOT = 860, OK_X = 1230, OK_ROOT = 860;
export const LINA_HEAD = [LINA_X + 6, LINA_ROOT - 280];
export const OK_HEAD = [OK_X - 20, OK_ROOT - 362 * 1.1];

const Blinds: React.FC<{ f: number; x: number; y: number; w: number; h: number }> = ({ f, x, y, w, h }) => <g>
  <rect x={x - 14} y={y - 14} width={w + 28} height={h + 28} fill="#1a2030" />
  <rect x={x} y={y} width={w} height={h} fill="#0b1224" />
  {/* city at night through the window */}
  {Array.from({ length: 9 }, (_, i) => { const bx = x + i * (w / 9), bh = 120 + ((i * 97) % 160); return <g key={i}><rect x={bx} y={y + h - bh} width={w / 9 - 6} height={bh} fill="#141c33" />
    {Array.from({ length: 12 }, (_, k) => <rect key={k} x={bx + 6 + (k % 3) * 16} y={y + h - bh + 10 + Math.floor(k / 3) * 26} width={8} height={12} fill={(i * 7 + k * 3) % 5 === 0 ? "#ffd08a" : "#2a3458"} opacity={0.9} />)}</g>; })}
  <Bokeh x={x} y={y + 40} w={w} h={h - 60} n={22} colors={["#ff6a6a", "#ffd08a", "#7ab8ff"]} seed={3} f={f} />
  <Rain f={f} x={x} y={y} w={w} h={h} n={70} o={0.35} />
  <PaneDrops f={f} x={x} y={y} w={w} h={h} n={36} />
  {/* blinds: slats with gaps */}
  {Array.from({ length: 16 }, (_, i) => <g key={i}><rect x={x} y={y + i * (h / 16)} width={w} height={h / 16 * 0.55} fill="#c9d3e3" opacity={0.85} />
    <rect x={x} y={y + i * (h / 16) + h / 16 * 0.45} width={w} height={3} fill="#000" opacity={0.3} /></g>)}
  <line x1={x + 40} y1={y} x2={x + 40} y2={y + h + 40} stroke="#d8e0ec" strokeWidth={2} />
</g>;

const Board: React.FC<{ x: number; y: number }> = ({ x, y }) => <g>
  <rect x={x} y={y} width={420} height={280} fill="#8a6a44" stroke="#3a2a1c" strokeWidth={10} />
  <Noise x={x} y={y} w={420} h={280} freq={0.6} o={0.35} />
  {[[30, 30, -4], [160, 50, 3], [290, 26, -2], [60, 160, 5], [230, 150, -3]].map(([dx, dy, r], i) =>
    <g key={i} transform={`rotate(${r} ${x + dx + 50} ${y + dy + 40})`}><rect x={x + dx} y={y + dy} width={100} height={80} fill="#f2eee4" /><rect x={x + dx + 6} y={y + dy + 6} width={88} height={56} fill={["#5a6378", "#6a5a52", "#4a5a6a", "#7a6a5a", "#56606e"][i]} /><circle cx={x + dx + 50} cy={y + dy + 4} r={6} fill="#d83a3a" /></g>)}
  <path d={`M${x + 80} ${y + 34} L${x + 210} ${y + 54} L${x + 340} ${y + 30} M${x + 210} ${y + 54} L${x + 110} ${y + 164} L${x + 280} ${y + 154}`} stroke="#d83a3a" strokeWidth={3} fill="none" />
</g>;

// organic coffee puddle on the table top (seen at a low angle → squashed), grows with k 0..1, drips over the front edge
export const SpillPuddle: React.FC<{ x: number; y: number; k: number }> = ({ x, y, k }) => {
  const R = 70 * Math.min(1, k), pts = Array.from({ length: 40 }, (_, i) => { const a = i / 40 * Math.PI * 2;
    const r = R * (1 + 0.14 * Math.sin(3 * a + 1) + 0.08 * Math.sin(5 * a + 2) + 0.05 * Math.sin(9 * a)); return [x + Math.cos(a) * r * 1.3 + R * 0.6, y + Math.sin(a) * r * 0.1]; });
  const d = "M" + pts.map(p => p.map(v => v.toFixed(1)).join(" ")).join(" L") + " Z";
  return <g><path d={d} fill="#4a2810" /><path d={d} fill="none" stroke="#7a4a22" strokeWidth={2} opacity={0.8} />
    <ellipse cx={x + R * 0.2} cy={y - 2} rx={R * 0.4} ry={2.5} fill="#fff" opacity={0.25} />
    {k > 0.7 && [0, 1].map(i => <line key={i} x1={x + 70 + i * 34} y1={y + 2} x2={x + 70 + i * 34} y2={y + 2 + Math.min(22, (k - 0.7) * 90 * (1 - i * 0.3))} stroke="#4a2810" strokeWidth={3} strokeLinecap="round" />)}
  </g>;
};

export const PoliceRoom: React.FC<{ f: number; lina: Pose; ok: Pose; cupTip?: number; photo?: boolean; lamp?: number; hide?: "lina" | "ok" | null; cupHeld?: boolean; splash?: number; spill?: number }> = ({ f, lina, ok, cupTip = 0, photo = true, lamp = 1, hide = null, cupHeld = false, splash = -1, spill = 0 }) => {
  const flick = f % 97 === 3 || f % 97 === 5 ? 0.7 : 1;      // fluorescent flicker
  const L = lamp * flick;
  return <>
    <Layer depth={0.85}>
      <rect x={-400} y={-300} width={2720} height={1120} fill="#26324a" />
      <Noise x={-400} y={-300} w={2720} h={1120} freq={0.7} o={0.3} />
      <rect x={-400} y={700} width={2720} height={30} fill="#1c2436" />
      <Board x={120} y={170} />
      <Blinds f={f} x={1260} y={110} w={560} h={420} />
      {/* filing cabinet + clock */}
      <rect x={-300} y={420} width={220} height={320} fill="#4a566c" /><line x1={-300} y1={530} x2={-80} y2={530} stroke="#2a3244" strokeWidth={4} /><line x1={-300} y1={640} x2={-80} y2={640} stroke="#2a3244" strokeWidth={4} />
      <circle cx={760} cy={130} r={46} fill="#e8e4da" stroke="#1a1e28" strokeWidth={8} /><line x1={760} y1={130} x2={760} y2={98} stroke="#111" strokeWidth={5} /><line x1={760} y1={130} x2={782} y2={140} stroke="#111" strokeWidth={4} />
      <AO x={-400} y={560} w={2720} h={170} dir="down" o={0.5} />
    </Layer>
    <Layer depth={1}>
      {/* floor */}
      <rect x={-600} y={730} width={3120} height={700} fill="#1b2130" />
      {Array.from({ length: 14 }, (_, i) => <line key={i} x1={-600 + i * 260} y1={730} x2={-1400 + i * 420} y2={1430} stroke="#000" strokeOpacity={0.25} strokeWidth={3} />)}
      <AO x={-600} y={730} w={3120} h={90} dir="up" o={0.55} />
      {/* hanging lamp + cone */}
      <line x1={960} y1={-300} x2={960} y2={20} stroke="#11151f" strokeWidth={4} />
      <path d="M880 60 Q960 10 1040 60 Z" fill="#2a3346" /><ellipse cx={960} cy={60} rx={80} ry={10} fill="#eaf6ff" />
      <Glow x={960} y={62} r={140} color="#eaf6ff" o={0.8 * L} />
      <Shaft pts={[[900, 40], [1020, 40], [1440, 880], [480, 880]]} color="#d6ecff" o={0.32 * L} blur={22} />
      <Glow x={960} y={620} r={520} color="#cfe6ff" o={0.35 * L} />
      {/* Lina's chair (behind her) */}
      <rect x={LINA_X - 70} y={LINA_ROOT - 300} width={18} height={220} rx={6} fill="#3a4256" />
      <rect x={LINA_X - 70} y={LINA_ROOT - 92} width={130} height={16} rx={5} fill="#4a536a" />
      <line x1={LINA_X - 60} y1={LINA_ROOT - 80} x2={LINA_X - 60} y2={LINA_ROOT} stroke="#2a3040" strokeWidth={8} /><line x1={LINA_X + 48} y1={LINA_ROOT - 80} x2={LINA_X + 48} y2={LINA_ROOT} stroke="#2a3040" strokeWidth={8} />
      {hide !== "lina" && <Character look={LINA} pose={{ ...SIT, facing: 1, ...lina }} x={LINA_X} y={LINA_ROOT} f={f} seed={1} rim={{ dx: 4, dy: -3, color: "#bfe2ff" }} />}
      {hide !== "ok" && <Character look={OKAFOR} pose={{ facing: -1, lean: 18, aL: [37, 0], aR: [42, 16], ...ok }} x={OK_X} y={OK_ROOT} f={f} seed={2} rim={{ dx: -4, dy: -3, color: "#bfe2ff" }} />}
      {/* table (in front of both) */}
      <rect x={520} y={TABLE_Y} width={880} height={26} rx={4} fill="#9aa6ba" />
      <rect x={520} y={TABLE_Y} width={880} height={6} rx={3} fill="#e4ecf8" opacity={0.7} />
      <rect x={540} y={TABLE_Y + 26} width={840} height={40} fill="#5a647a" />
      <rect x={560} y={TABLE_Y + 66} width={22} height={LINA_ROOT - TABLE_Y - 66} fill="#454e62" /><rect x={1338} y={TABLE_Y + 66} width={22} height={LINA_ROOT - TABLE_Y - 66} fill="#454e62" />
      <AO x={540} y={TABLE_Y + 66} w={840} h={60} dir="down" o={0.5} />
      {/* on the table: case photo + cup */}
      {photo && <g transform={`rotate(-6 960 ${TABLE_Y})`}><rect x={900} y={TABLE_Y - 8} width={130} height={10} fill="#f2eee4" /></g>}
      {/* the cup (x 1100–1128), right next to Okafor's resting hand; tips over to the right around its base corner */}
      {spill > 0 && <SpillPuddle x={1160} y={TABLE_Y - 1} k={spill} />}
      {!cupHeld && <g transform={`translate(1100 ${TABLE_Y}) rotate(${cupTip * 90} 28 0)`}>
        <path d="M0 -44 L28 -44 L24 0 L4 0 Z" fill="#f2efe6" /><rect x={-1} y={-48} width={30} height={7} rx={2} fill="#3a3530" opacity={cupTip > 0.5 ? 0 : 1} /><rect x={2} y={-30} width={24} height={10} fill="#b0623a" />
      </g>}
      {cupTip > 0.5 && <rect x={1184} y={TABLE_Y - 9} width={28} height={7} rx={2} fill="#3a3530" transform={`rotate(${20 + cupTip * 30} 1198 ${TABLE_Y - 5})`} />}
      {splash >= 0 && splash < 22 && Array.from({ length: 12 }, (_, i) => { const a = -Math.PI * (0.15 + 0.7 * ((i * 37) % 12) / 12), v = 3 + ((i * 53) % 7) * 0.7, t = splash;
        return <circle key={i} cx={1114 + Math.cos(a) * v * t * 1.4} cy={TABLE_Y - 44 + Math.sin(a) * v * t + 0.55 * t * t} r={2.2 + (i % 3)} fill="#5a3218" opacity={1 - t / 22} />; })}
    </Layer>
  </>;
};
