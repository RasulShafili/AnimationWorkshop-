// Chapter 5 sets: Grandma Ayla's warm apartment (kitchen on the left, living room with a record player on the right,
// family photos everywhere), the doctor's office with a brain-scan light box, inserts (keys in the fridge, a missed
// birthday), and the two minds side by side (Lina's doors glow, Ayla's go dark one by one).
import React from "react";
import { Layer, rnd, W, H, sat, lerp, ease } from "../engine/core";
import { Glow, Shaft } from "../engine/fx";
import { Noise, Wood, Wallpaper, AO } from "../engine/tex";
import { Character, Pose, SIT } from "../chars/Rig2";
import { LINA, AYLA, HALE } from "../chars/cast";
import { Door, dateOf } from "./Palace";

const GOLD = "#ffc94a";
const Frame: React.FC<{ x: number; y: number; w: number; h: number; c: string; i: number }> = ({ x, y, w, h, c, i }) => <g>
  <rect x={x} y={y} width={w} height={h} fill="#7a5230" /><rect x={x + 6} y={y + 6} width={w - 12} height={h - 12} fill={c} />
  <circle cx={x + w * 0.4} cy={y + h * 0.5} r={w * 0.12} fill="#2e2a38" /><circle cx={x + w * 0.62} cy={y + h * 0.56} r={w * 0.1} fill="#2e2a38" />
  {i % 2 === 0 && <circle cx={x + w * 0.62} cy={y + h * 0.44} r={w * 0.07} fill="#d8d6e2" />}
</g>;

// whole apartment, 4000 px wide: kitchen (x -900..900), living room (x 1000..2900)
export const Apartment: React.FC<{ f: number; ayla: Pose & { x?: number; sit?: boolean }; lina: Pose & { x?: number; small?: boolean; sit?: boolean } | null; warm?: number; flour?: number; cards?: boolean; record?: boolean; dim?: number }> = ({ f, ayla, lina, warm = 1, flour = 0, cards = false, record = true, dim = 0 }) => {
  const ax = ayla.x ?? 300, lx = lina?.x ?? 560;
  return <>
  <Layer depth={0.75}>
    <rect x={-1200} y={-500} width={4600} height={1300} fill="#5a3a3a" />
    <Wallpaper x={-1200} y={-500} w={4600} h={1100} base="#e8c89a" ink="#b8784a" kind="floral" o={0.16} />
    {/* kitchen: cupboards, window with afternoon sun, shelves with jars */}
    <rect x={-900} y={120} width={1700} height={190} fill="#8a5a3a" />{[0, 1, 2, 3, 4].map(i => <rect key={i} x={-880 + i * 340} y={135} width={320} height={160} rx={8} fill="#9a6a44" stroke="#6a4024" strokeWidth={4} />)}
    <rect x={-300} y={340} width={420} height={300} fill="#ffe2a8" /><rect x={-310} y={330} width={440} height={320} fill="none" stroke="#f4ecdc" strokeWidth={16} /><line x1={-90} y1={340} x2={-90} y2={640} stroke="#f4ecdc" strokeWidth={10} />
    <Glow x={-90} y={480} r={500} color="#ffd890" o={0.6 * warm} />
    {[0, 1, 2, 3, 4, 5].map(i => <rect key={i} x={240 + i * 70} y={360} width={50} height={70} rx={10} fill={["#e8a46a", "#c8302c", "#6ab05a", "#e8d07a", "#a86a4a", "#d87a9a"][i]} opacity={0.85} />)}
    <rect x={220} y={430} width={460} height={12} fill="#6a4024" />
    {/* living room: photo wall, lamp, record player on a cabinet */}
    <Frame x={1150} y={180} w={170} h={140} c="#e8a46a" i={0} /><Frame x={1350} y={150} w={140} h={180} c="#6ab0d8" i={1} /><Frame x={1520} y={200} w={200} h={150} c="#d87a9a" i={2} />
    <Frame x={1200} y={360} w={150} h={120} c="#8ac87a" i={3} /><Frame x={1390} y={370} w={190} h={140} c="#c8a0e8" i={4} /><Frame x={1620} y={390} w={130} h={110} c="#e8d07a" i={5} />
    <rect x={2000} y={150} width={500} height={460} fill="#ffe2a8" opacity={0.8} /><rect x={1990} y={140} width={520} height={480} fill="none" stroke="#f4ecdc" strokeWidth={16} />
    <Glow x={2250} y={380} r={600} color="#ffd890" o={0.5 * warm} />
  </Layer>
  <Layer depth={1}>
    <Wood x={-1300} y={760} w={4800} h={600} color="#7a4a2a" rows={10} />
    <AO x={-1300} y={760} w={4800} h={70} dir="up" o={0.4} />
    <Shaft pts={[[-300, 340], [120, 340], [500, 1100], [-200, 1100]]} color="#ffe2a8" o={0.22 * warm} />
    {/* the record player (spinning) on a cabinet in the living room */}
    <rect x={2600} y={600} width={300} height={260} fill="#6a4024" /><rect x={2610} y={570} width={280} height={40} rx={6} fill="#3a2418" />
    {record && <g><ellipse cx={2720} cy={572} rx={100} ry={18} fill="#111" /><ellipse cx={2720} cy={572} rx={70} ry={12} fill="none" stroke="#2a2a2a" strokeWidth={2} /><ellipse cx={2720} cy={572} rx={30} ry={6} fill="#c8302c" />
      {/* a highlight sweeping around the flat record = it spins */}<path d={`M2720 572 L${2720 + Math.cos(f * 0.35) * 96} ${572 + Math.sin(f * 0.35) * 17}`} stroke="#fff" strokeOpacity={0.35} strokeWidth={4} /></g>}
    <line x1={2850} y1={566} x2={2760} y2={572} stroke="#c8c8c8" strokeWidth={5} />
    {/* card table in the living room */}
    {cards && <><rect x={1500} y={680} width={460} height={18} rx={6} fill="#3a6a4a" /><rect x={1520} y={698} width={14} height={160} fill="#3a2418" /><rect x={1926} y={698} width={14} height={160} fill="#3a2418" />
      {[0, 1, 2].map(i => <rect key={i} x={1640 + i * 40} y={666} width={34} height={14} rx={2} fill="#fdfbf4" />)}</>}
    {ayla.sit && <><rect x={ax - 70} y={560} width={18} height={220} rx={6} fill="#6a3a3a" /><rect x={ax - 70} y={770} width={130} height={16} rx={5} fill="#8a4a4a" /></>}
    {lina?.sit && <><rect x={lx + 54} y={560} width={18} height={220} rx={6} fill="#6a3a3a" /><rect x={lx - 60} y={770} width={130} height={16} rx={5} fill="#8a4a4a" /></>}
    <Character look={AYLA} pose={ayla.sit ? { ...SIT, facing: 1, ...ayla } : { facing: 1, ...ayla }} x={ax} y={860} f={f} seed={4} rim={{ dx: 4, dy: -3, color: "#ffe2a8" }} />
    {lina && <Character look={lina.small ? { ...LINA, scale: 0.72 } : LINA} pose={lina.sit ? { ...SIT, facing: -1, ...lina } : { facing: -1, ...lina }} x={lx} y={860} f={f} seed={1} rim={{ dx: -4, dy: -3, color: "#ffe2a8" }} />}
    {/* kitchen counter with flour, rolling pin, a tray of baklava */}
    <rect x={-60} y={660} width={760} height={30} rx={6} fill="#e8dcc8" /><rect x={-40} y={690} width={720} height={170} fill="#9a6a44" />
    {[0, 1, 2].map(i => <rect key={i} x={-20 + i * 240} y={710} width={220} height={130} rx={6} fill="#8a5a3a" stroke="#6a4024" strokeWidth={3} />)}
    {flour > 0 && <ellipse cx={330} cy={658} rx={140 * flour} ry={12} fill="#fff" opacity={0.85} />}
    <rect x={-30} y={640} width={200} height={20} rx={4} fill="#c8a03a" />{Array.from({ length: 8 }, (_, i) => <path key={i} d={`M${-20 + i * 24} 640 l12 -14 l12 14 Z`} fill="#e8b04a" stroke="#a8742a" strokeWidth={2} />)}
    <rect x={140} y={646} width={180} height={14} rx={7} fill="#c89a62" />
    <Glow x={600} y={500} r={1200} color="#ffcf8a" o={0.2 * warm} />
  </Layer>
  {dim > 0 && <Layer depth={1}><rect x={-1500} y={-600} width={5000} height={2000} fill="#1a2030" opacity={dim * 0.45} /></Layer>}
  </>;
};

export const DoctorOffice: React.FC<{ f: number; hale: Pose; lina: Pose; ayla: Pose | null; scan?: number }> = ({ f, hale, lina, ayla, scan = 1 }) => <>
  <Layer depth={0.75}>
    <rect x={-1000} y={-500} width={3920} height={1300} fill="#dfe8ec" /><Noise x={-1000} y={-500} w={3920} h={1300} freq={0.7} o={0.1} />
    <rect x={1300} y={120} width={520} height={380} rx={10} fill="#1a2a3a" /><rect x={1316} y={136} width={488} height={348} fill="#cfe8ff" opacity={0.35 + 0.6 * scan} />
    {[0, 1].map(k => <g key={k} transform={`translate(${1420 + k * 230} 310)`}><ellipse cx={0} cy={0} rx={90} ry={110} fill="#2a3a4a" opacity={0.85} /><path d="M0 -100 Q-10 0 0 100" stroke="#cfe8ff" strokeWidth={4} fill="none" />
      {Array.from({ length: 8 }, (_, i) => <path key={i} d={`M${-70 + (i % 4) * 36} ${-60 + Math.floor(i / 4) * 70} q14 -16 28 0 t28 0`} stroke="#9ac8ff" strokeWidth={3} fill="none" />)}
      {k === 1 && <ellipse cx={20} cy={30} rx={34} ry={22} fill="#ff6a5a" opacity={0.55 * scan} />}</g>)}
    <rect x={200} y={160} width={300} height={220} fill="#fff" stroke="#9aa8b4" strokeWidth={8} /><rect x={240} y={200} width={220} height={20} fill="#9aa8b4" /><rect x={240} y={240} width={160} height={14} fill="#c8d0d8" /><rect x={240} y={270} width={190} height={14} fill="#c8d0d8" />
    <rect x={-400} y={200} width={160} height={400} fill="#b8d0b8" /><circle cx={-320} cy={180} r={80} fill="#6ab05a" />
  </Layer>
  <Layer depth={1}>
    <rect x={-1000} y={760} width={3920} height={600} fill="#c8d4d8" />
    {Array.from({ length: 20 }, (_, i) => <line key={i} x1={-1000 + i * 220} y1={760} x2={-1200 + i * 220} y2={1360} stroke="#000" strokeOpacity={0.05} strokeWidth={3} />)}
    {/* Hale standing by the light box; Ayla and Lina seated in front of the desk */}
    <Character look={HALE} pose={{ facing: -1, ...hale }} x={1260} y={870} f={f} seed={6} rim={{ dx: -4, dy: -3, color: "#cfe8ff" }} />
    <rect x={500} y={560} width={18} height={220} rx={6} fill="#5a6a7a" /><rect x={500} y={770} width={130} height={16} rx={5} fill="#6a7a8a" />
    <rect x={760} y={560} width={18} height={220} rx={6} fill="#5a6a7a" /><rect x={760} y={770} width={130} height={16} rx={5} fill="#6a7a8a" />
    {ayla && <Character look={AYLA} pose={{ ...SIT, facing: 1, ...ayla }} x={570} y={860} f={f} seed={4} />}
    <Character look={LINA} pose={{ ...SIT, facing: 1, ...lina }} x={830} y={860} f={f} seed={1} />
    <rect x={940} y={690} width={260} height={20} rx={4} fill="#8a9aa8" /><rect x={950} y={710} width={240} height={150} fill="#6a7a88" />
  </Layer>
</>;

export const FridgeInsert: React.FC<{ f: number }> = ({ f }) => { const open = ease(f / 14);
  return <svg width={W} height={H} style={{ position: "absolute" }}>
    <rect width={W} height={H} fill="#e8c89a" />
    <rect x={560} y={60} width={800} height={1020} rx={30} fill="#e8eef0" />
    <rect x={600} y={100} width={720} height={940} rx={10} fill="#fffef4" />
    <Glow x={960} y={300} r={600} color="#fffbe0" o={0.7 * open} />
    {[300, 520, 740].map(y => <rect key={y} x={610} y={y} width={700} height={12} fill="#cfd8dc" />)}
    <rect x={660} y={200} width={120} height={100} rx={12} fill="#e8b04a" /><rect x={820} y={180} width={80} height={120} rx={10} fill="#fff" stroke="#9ab" strokeWidth={4} />
    <rect x={1100} y={420} width={160} height={100} rx={10} fill="#c8302c" opacity={0.8} />
    {/* the keys, on the shelf, next to the butter */}
    <g transform="translate(900 470)"><circle r={34} fill="none" stroke="#c8a03a" strokeWidth={10} /><rect x={20} y={-10} width={110} height={20} rx={6} fill="#d8b04a" /><rect x={100} y={10} width={14} height={22} fill="#d8b04a" /><rect x={-150} y={-30} width={110} height={60} rx={10} fill="#f4e08a" /></g>
    <Glow x={960} y={480} r={160} color={GOLD} o={0.5} />
    <rect x={560} y={60} width={800 * (1 - open) + 20} height={1020} rx={30} fill="#d8e0e4" />
  </svg>; };

export const MissedBirthday: React.FC<{ f: number }> = ({ f }) => <svg width={W} height={H} style={{ position: "absolute" }}>
  <rect width={W} height={H} fill="#e8c89a" />
  <g transform="translate(560 140)">
    <rect x={0} y={0} width={800} height={800} rx={20} fill="#fbf8f0" /><rect x={0} y={0} width={800} height={130} rx={20} fill="#c8302c" />
    <text x={400} y={92} fontFamily="Inter" fontWeight={900} fontSize={70} fill="#fff" textAnchor="middle" letterSpacing={10}>OCTOBER</text>
    {Array.from({ length: 31 }, (_, i) => { const x = 40 + (i % 7) * 104, y = 180 + Math.floor(i / 7) * 120; return <g key={i}><rect x={x} y={y} width={94} height={104} fill="none" stroke="#e0dcd0" strokeWidth={2} />
      <text x={x + 12} y={y + 36} fontFamily="Inter" fontWeight={800} fontSize={28} fill="#666">{i + 1}</text>
      {i === 11 && <><circle cx={x + 47} cy={y + 52} r={44} fill="none" stroke="#e84a8a" strokeWidth={6} /><text x={x + 47} y={y + 92} fontFamily="Inter" fontWeight={900} fontSize={16} fill="#e84a8a" textAnchor="middle">MOM ♥</text></>}
      {i < 18 && <path d={`M${x + 14} ${y + 20} L${x + 80} ${y + 90} M${x + 80} ${y + 20} L${x + 14} ${y + 90}`} stroke="#2a2a3a" strokeWidth={4} opacity={i === 11 ? 0 : 0.5} />}</g>; })}
  </g>
  {f > 18 && <g transform={`translate(1000 560) rotate(-12) scale(${1 + 0.3 * Math.exp(-(f - 18) / 4)})`}><text fontFamily="Inter" fontWeight={900} fontSize={110} fill="#c8302c" textAnchor="middle" opacity={0.9}>FORGOT</text></g>}
</svg>;

// two minds side by side: Lina's doors all glowing; Ayla's going dark one by one (k 0..1)
export const TwoMinds: React.FC<{ f: number; k: number }> = ({ f, k }) => <svg width={W} height={H} style={{ position: "absolute" }}>
  <rect width={W} height={H} fill="#0e0b1a" />
  <line x1={960} y1={80} x2={960} y2={1000} stroke="#2a2440" strokeWidth={4} />
  {[0, 1].map(side => { const ox = side ? 1000 : 40; return <g key={side}>
    <Glow x={ox + 460} y={520} r={500} color={side ? "#9a8ac8" : GOLD} o={side ? 0.2 * (1 - k) : 0.3} />
    {Array.from({ length: 12 }, (_, i) => { const col = i % 4, row = Math.floor(i / 4); const dark = side === 1 && rnd(i, 9) < k;
      return <Door key={i} x={ox + 60 + col * 210} y={150 + row * 270} w={150} h={210} i={side * 50 + i + (side ? 7 : 0)} open={dark ? 0 : 0.6} glow={dark ? 0 : 1} dark={dark} />; })}
    <text x={ox + 460} y={990} fontFamily="Inter" fontWeight={900} fontSize={54} fill={side ? "#b8a8e8" : GOLD} textAnchor="middle" letterSpacing={6}>{side ? "GRANDMA AYLA" : "YOU"}</text>
  </g>; })}
</svg>;
