// School sets for chapter 3: bright classroom (warm morning light, rows of desks, many students with depth blur),
// hallway with lockers, cafeteria. Characters are passed in so each shot can pose them.
import React from "react";
import { Layer, rnd } from "../engine/core";
import { Glow, Shaft } from "../engine/fx";
import { Noise, Wood, AO } from "../engine/tex";
import { Character, Pose, SIT } from "../chars/Rig2";
import { LINA, SAM, EXTRAS } from "../chars/cast";

export const DESK_Y = 690;          // desk top in the classroom (seated characters: root 860)
const Desk: React.FC<{ x: number; y: number; w?: number }> = ({ x, y, w = 260 }) => <g>
  <rect x={x} y={y} width={w} height={18} rx={4} fill="#c89a62" /><rect x={x} y={y} width={w} height={5} fill="#f0c890" opacity={0.7} />
  <rect x={x + 10} y={y + 18} width={w - 20} height={34} fill="#9a7244" />
  <rect x={x + 16} y={y + 52} width={12} height={860 - y - 52} fill="#5a5a66" /><rect x={x + w - 28} y={y + 52} width={12} height={860 - y - 52} fill="#5a5a66" />
</g>;
const Chair: React.FC<{ x: number; y: number }> = ({ x, y }) => <g>
  <rect x={x - 70} y={y - 300} width={16} height={214} rx={5} fill="#3a6aa8" /><rect x={x - 70} y={y - 92} width={124} height={14} rx={5} fill="#4a7ab8" />
  <line x1={x - 62} y1={y - 78} x2={x - 62} y2={y} stroke="#3a3a46" strokeWidth={7} /><line x1={x + 44} y1={y - 78} x2={x + 44} y2={y} stroke="#3a3a46" strokeWidth={7} />
</g>;

// classroom: back row (depth 0.85, small, blurred), Lina's row (depth 1), foreground desk/student (depth 1.3, blurred)
export const Classroom: React.FC<{ f: number; lina: Pose; sam: Pose; extras?: Pose; stand?: boolean; book?: number }> = ({ f, lina, sam, extras = {}, stand = false }) => <>
  <Layer depth={0.6}>
    <rect x={-800} y={-400} width={3520} height={1200} fill="#f0dcb8" />
    <Noise x={-800} y={-400} w={3520} h={1200} freq={0.7} o={0.12} />
    {/* windows with morning sky + trees */}
    {[0, 1, 2].map(i => { const x = 1200 + i * 380; return <g key={i}><rect x={x} y={60} width={320} height={420} fill="#bfe2f4" /><circle cx={x + 120} cy={360} r={110} fill="#8ac87a" opacity={0.8} /><circle cx={x + 230} cy={400} r={90} fill="#6ab05a" opacity={0.8} />
      <rect x={x - 12} y={50} width={344} height={440} fill="none" stroke="#fff" strokeWidth={18} /><line x1={x + 160} y1={60} x2={x + 160} y2={480} stroke="#fff" strokeWidth={10} /></g>; })}
    {/* chalkboard + posters */}
    <rect x={-300} y={90} width={980} height={380} rx={10} fill="#2f5a46" stroke="#a0784a" strokeWidth={16} />
    <text x={-240} y={190} fontFamily="Inter" fontWeight={800} fontSize={44} fill="#e8f0e0" opacity={0.85}>CHAPTER 6 · THE CELL</text>
    <path d="M-220 260 q60 -40 120 0 t120 0 M-220 330 L200 330 M-220 390 L80 390" stroke="#e8f0e0" strokeWidth={6} fill="none" opacity={0.6} />
    <rect x={760} y={120} width={150} height={200} fill="#e85a4a" /><rect x={940} y={140} width={150} height={190} fill="#4aa8d8" />
    <circle cx={1060} cy={-10} r={44} fill="#fff" stroke="#333" strokeWidth={6} />
    <AO x={-800} y={560} w={3520} h={120} dir="down" o={0.3} />
  </Layer>
  <Layer depth={0.85} blur={2.5}>
    <rect x={-800} y={660} width={3520} height={600} fill="#b88a5a" />
    {[-300, 100, 500, 900, 1300, 1700].map((x, i) => <g key={i}>
      <Character look={EXTRAS[i % EXTRAS.length]} pose={{ ...SIT, facing: 1, look: [0.6, 0], ...extras }} x={x + 120} y={722} s={0.66} f={f} seed={10 + i} />
      <rect x={x + 150} y={606} width={180} height={12} rx={3} fill="#c89a62" /><rect x={x + 156} y={618} width={168} height={24} fill="#9a7244" /></g>)}
  </Layer>
  <Layer depth={1}>
    <Wood x={-900} y={760} w={3720} h={600} color="#b88a5a" rows={10} />
    <AO x={-900} y={760} w={3720} h={80} dir="up" o={0.35} />
    <Shaft pts={[[1260, 60], [1560, 60], [1100, 1100], [600, 1100]]} color="#fff2c8" o={0.28} />
    <Shaft pts={[[1640, 60], [1940, 60], [1500, 1100], [1000, 1100]]} color="#fff2c8" o={0.22} />
    {!stand && <Chair x={700} y={860} />}<Chair x={1200} y={860} />
    <Character look={LINA} pose={stand ? { facing: 1, ...lina } : { ...SIT, facing: 1, ...lina }} x={700} y={860} f={f} seed={1} rim={{ dx: 4, dy: -3, color: "#fff2c8" }} />
    <Character look={SAM} pose={{ ...SIT, facing: -1, ...sam }} x={1200} y={860} f={f} seed={3} rim={{ dx: -4, dy: -3, color: "#fff2c8" }} />
    <Desk x={560} y={DESK_Y} w={300} /><Desk x={1060} y={DESK_Y} w={300} />
    <Glow x={1300} y={500} r={900} color="#fff2c8" o={0.25} />
  </Layer>
</>;

// hallway with lockers (for the argument); Lina left facing right, Sam right facing left
export const Hallway: React.FC<{ f: number; lina: Pose; sam: Pose; samX?: number }> = ({ f, lina, sam, samX = 1200 }) => <>
  <Layer depth={0.7}>
    <rect x={-800} y={-400} width={3520} height={1200} fill="#e8e0d0" />
    {Array.from({ length: 26 }, (_, i) => <g key={i}><rect x={-700 + i * 130} y={180} width={120} height={520} fill={i % 2 ? "#3a7ab8" : "#3570aa"} />
      <rect x={-690 + i * 130} y={200} width={100} height={8} fill="#2a5a88" /><rect x={-690 + i * 130} y={220} width={100} height={8} fill="#2a5a88" /><rect x={-690 + i * 130} y={240} width={100} height={8} fill="#2a5a88" />
      <rect x={-600 + i * 130} y={420} width={10} height={40} rx={4} fill="#c8d0dc" /></g>)}
    <rect x={-800} y={130} width={3520} height={50} fill="#d84a3a" />
    {[200, 900, 1600].map((x, i) => <rect key={i} x={x} y={-60} width={360} height={30} rx={10} fill="#fffbe8" />)}
  </Layer>
  <Layer depth={1}>
    <rect x={-900} y={700} width={3720} height={600} fill="#cfc6b4" />
    {Array.from({ length: 30 }, (_, i) => <line key={i} x1={-900 + i * 140} y1={700} x2={-900 + i * 140 - 200} y2={1300} stroke="#000" strokeOpacity={0.06} strokeWidth={3} />)}
    <AO x={-900} y={700} w={3720} h={60} dir="up" o={0.3} />
    <Character look={LINA} pose={{ facing: 1, ...lina }} x={720} y={860} f={f} seed={1} rim={{ dx: 4, dy: -3, color: "#fff" }} />
    <Character look={SAM} pose={{ facing: -1, ...sam }} x={samX} y={860} f={f} seed={3} rim={{ dx: -4, dy: -3, color: "#fff" }} />
  </Layer>
</>;

// cafeteria: long table, trays; used for the card trick and the remembered pizza day
export const Cafeteria: React.FC<{ f: number; lina?: Pose; sam: Pose; showLina?: boolean; showSam?: boolean; pizza?: boolean; rain?: boolean }> = ({ f, lina = {}, sam, showLina = true, showSam = true, pizza = false, rain = false }) => <>
  <Layer depth={0.6}>
    <rect x={-800} y={-400} width={3520} height={1200} fill="#d8e4dc" />
    <rect x={-800} y={380} width={3520} height={300} fill="#c0d0c4" />
    {Array.from({ length: 12 }, (_, i) => <g key={i}><rect x={-700 + i * 300} y={120} width={220} height={200} fill={rain ? "#6a7c94" : "#9ad0e8"} stroke="#fff" strokeWidth={12} />
      {rain && Array.from({ length: 14 }, (_, k) => { const yy = 120 + ((k * 37 + f * (6 + (k % 3))) % 200); return <line key={k} x1={-690 + i * 300 + (k * 53) % 200} y1={yy} x2={-694 + i * 300 + (k * 53) % 200} y2={Math.min(320, yy + 22)} stroke="#c8d8ec" strokeWidth={2} opacity={0.7} />; })}</g>)}
    <rect x={200} y={420} width={700} height={140} fill="#9aa6b2" /><rect x={220} y={440} width={660} height={40} fill="#c8d4dc" />
    <text x={550} y={410} fontFamily="Inter" fontWeight={900} fontSize={48} fill="#d84a3a" textAnchor="middle">LUNCH</text>
  </Layer>
  <Layer depth={0.85} blur={3}>
    {[-200, 300, 1500, 2000].map((x, i) => <Character key={i} look={EXTRAS[(i + 2) % EXTRAS.length]} pose={{ ...SIT, facing: i % 2 ? -1 : 1 }} x={x} y={760} s={0.8} f={f} seed={20 + i} />)}
    <rect x={-800} y={650} width={3520} height={24} fill="#e8eef0" />
  </Layer>
  <Layer depth={1}>
    <rect x={-900} y={760} width={3720} height={600} fill="#b8c4bc" />
    <Chair x={720} y={860} /><Chair x={1220} y={860} />
    {showLina && <Character look={LINA} pose={{ ...SIT, facing: 1, ...lina }} x={720} y={860} f={f} seed={1} rim={{ dx: 4, dy: -3, color: "#fff" }} />}
    {showSam && <Character look={SAM} pose={{ ...SIT, facing: -1, ...sam }} x={1220} y={860} f={f} seed={3} rim={{ dx: -4, dy: -3, color: "#fff" }} />}
    <rect x={520} y={DESK_Y} width={900} height={20} rx={6} fill="#e8eef0" /><rect x={540} y={DESK_Y + 20} width={860} height={40} fill="#a8b4bc" />
    <rect x={560} y={DESK_Y + 60} width={14} height={110} fill="#5a6470" /><rect x={1366} y={DESK_Y + 60} width={14} height={110} fill="#5a6470" />
    {/* trays */}
    <rect x={800} y={DESK_Y - 10} width={120} height={12} rx={4} fill="#e86a4a" /><rect x={1040} y={DESK_Y - 10} width={120} height={12} rx={4} fill="#4a9ad8" />
    {pizza && <path d={`M1060 ${DESK_Y - 12} L1140 ${DESK_Y - 12} L1100 ${DESK_Y - 40} Z`} fill="#f0c050" stroke="#c8902e" strokeWidth={3} />}
    {pizza && [0, 1, 2].map(i => <circle key={i} cx={1085 + i * 14} cy={DESK_Y - 20 - (i % 2) * 6} r={4} fill="#f0e060" />)}
    <Glow x={960} y={300} r={1000} color="#fffbe8" o={0.2} />
  </Layer>
</>;
