// FRESHWAY supermarket — our main location. Side-view aisle, the glass front seen from inside (crowd outside),
// staff room with whiteboard, loading-dock door, shopping cart, product shelves. Lighting modes: day (fluorescent),
// night (freezer glow only), dark (power gone, lantern/torch).
import React from "react";
import { rnd } from "../engine/core";
import { Glow, Shaft } from "../engine/fx";
import { Noise, AO } from "../engine/tex";
import { Character, Pose, Look } from "../chars/Rig2";
import { ZOMBIES, zombiePose } from "../chars/cast";

export type Light = "day" | "night" | "dark";
const PROD = ["#d8402e", "#f2b632", "#3a7ad8", "#4ab06a", "#e8742a", "#9a5ad0", "#f4f1e6", "#2e9a9a", "#e85a8a"];

// one shelf unit (gondola) with 4 rows of products, x,y = bottom-left, w,h
export const Shelf: React.FC<{ x: number; y: number; w: number; h?: number; seed?: number; dim?: number; empty?: number }> = ({ x, y, w, h = 520, seed = 1, dim = 1, empty = 0 }) => {
  const rows = 4, rh = (h - 60) / rows;
  return <g>
    <rect x={x} y={y - h} width={w} height={h} fill="#c9ccd2" /><rect x={x} y={y - h} width={w} height={h} fill="#000" opacity={0.35 * (1 - dim) + 0.05} />
    <rect x={x + 6} y={y - h + 30} width={w - 12} height={h - 50} fill="#8a909c" opacity={0.6} />
    {Array.from({ length: rows }, (_, r) => { const yy = y - 40 - r * rh; let cx = x + 12; const items: React.ReactNode[] = []; let k = 0;
      while (cx < x + w - 30) { const pw = 26 + rnd(k + r * 31, seed) * 34, ph = rh * (0.5 + rnd(k + r * 17, seed + 1) * 0.38), col = PROD[Math.floor(rnd(k + r * 7, seed + 2) * PROD.length)];
        if (rnd(k + r * 13, seed + 3) > empty) items.push(<g key={k}><rect x={cx} y={yy - ph} width={pw - 4} height={ph} rx={3} fill={col} /><rect x={cx} y={yy - ph} width={pw - 4} height={ph * 0.22} fill="#fff" opacity={0.28} /><rect x={cx + (pw - 4) * 0.2} y={yy - ph * 0.62} width={(pw - 4) * 0.6} height={ph * 0.22} rx={2} fill="#fff" opacity={0.55} /></g>);
        cx += pw; k++; }
      return <g key={r}>{items}<rect x={x + 4} y={yy} width={w - 8} height={12} fill="#e8eaee" /><rect x={x + 4} y={yy + 12} width={w - 8} height={6} fill="#5a606a" />
        {Array.from({ length: Math.floor(w / 90) }, (_, i) => <rect key={i} x={x + 20 + i * 90} y={yy + 1} width={30} height={9} fill={i % 3 ? "#f6d84a" : "#fff"} />)}</g>; })}
    <rect x={x} y={y - h} width={w} height={30} fill="#2f8a4e" /><rect x={x} y={y - h} width={w} height={6} fill="#fff" opacity={0.25} />
    <rect x={x} y={y - 14} width={w} height={14} fill="#3a3e48" />
    {dim < 1 && <rect x={x} y={y - h} width={w} height={h} fill="#0a0e1a" opacity={(1 - dim) * 0.55} />}
  </g>;
};
export const Cart: React.FC<{ x: number; y: number; s?: number; full?: boolean; flip?: boolean }> = ({ x, y, s = 1, full, flip }) => (
  <g transform={`translate(${x} ${y}) scale(${(flip ? -1 : 1) * s} ${s})`}>
    <ellipse cx={0} cy={4} rx={130} ry={12} fill="#000" opacity={0.3} />
    {full && <>{[[-90, -250, "#d8402e"], [-40, -262, "#3a7ad8"], [10, -248, "#f2b632"], [60, -258, "#4ab06a"], [-70, -290, "#e8742a"], [20, -292, "#f4f1e6"]].map(([px, py, c], i) => <rect key={i} x={px as number} y={py as number} width={56} height={50} rx={4} fill={c as string} />)}</>}
    <path d="M-120 -240 L110 -240 L90 -110 L-100 -110 Z" fill="none" stroke="#b8bec8" strokeWidth={7} strokeLinejoin="round" />
    {Array.from({ length: 9 }, (_, i) => <line key={i} x1={-112 + i * 26} y1={-240} x2={-96 + i * 22} y2={-110} stroke="#b8bec8" strokeWidth={3} />)}
    {[0, 1, 2].map(i => <line key={i} x1={-116 + i * 2} y1={-200 + i * 40} x2={104 - i * 6} y2={-200 + i * 40} stroke="#b8bec8" strokeWidth={3} />)}
    <path d="M110 -240 L150 -290" stroke="#b8bec8" strokeWidth={7} strokeLinecap="round" /><rect x={138} y={-300} width={34} height={14} rx={6} fill="#d8402e" />
    <path d="M-100 -110 L-90 -30 L90 -30 L90 -110" stroke="#9aa0aa" strokeWidth={6} fill="none" />
    {[-80, 80].map(wx => <g key={wx}><circle cx={wx} cy={-14} r={14} fill="#26262c" /><circle cx={wx} cy={-14} r={5} fill="#8a8a94" /></g>)}
  </g>);

// side-view aisle: back wall with glowing freezers, shelves, floor. width covers x -700..2700 for camera pans.
export const StoreAisle: React.FC<{ f: number; light?: Light; children?: React.ReactNode; sign?: string; empty?: number }> = ({ f, light = "night", children, sign = "AISLE 4 · CEREAL", empty = 0 }) => {
  const day = light === "day", dark = light === "dark";
  return <g>
    <rect x={-800} y={-200} width={3600} height={1500} fill={day ? "#b9c4cc" : dark ? "#0b0d14" : "#141c2a"} />
    {/* ceiling + lights */}
    <rect x={-800} y={-200} width={3600} height={300} fill={day ? "#d6dde2" : "#0c1018"} />
    {Array.from({ length: 9 }, (_, i) => <g key={i}><rect x={-600 + i * 420} y={60} width={220} height={18} rx={4} fill={day ? "#fbfff4" : light === "night" && i % 3 === 1 ? "#d8eaff" : "#2a2e38"} />
      {day && <Shaft pts={[[-600 + i * 420, 78], [-380 + i * 420, 78], [-300 + i * 420, 800], [-680 + i * 420, 800]]} color="#ffffff" o={0.12} />}</g>)}
    {/* back wall freezers */}
    {Array.from({ length: 8 }, (_, i) => { const x = -700 + i * 460; return <g key={i}>
      <rect x={x} y={180} width={440} height={430} fill="#2a3240" />
      {[0, 1, 2].map(d => <g key={d}><rect x={x + 14 + d * 142} y={196} width={130} height={396} fill={dark ? "#121820" : day ? "#bfe6ff" : "#5a86a8"} opacity={dark ? 1 : 0.85} />
        {!dark && [0, 1, 2, 3].map(r => <g key={r}>{[0, 1, 2, 3].map(c => <rect key={c} x={x + 22 + d * 142 + c * 30} y={226 + r * 92} width={24} height={50} rx={3} fill={PROD[(i * 7 + d * 3 + r + c) % PROD.length]} opacity={day ? 0.75 : 0.4} />)}<rect x={x + 18 + d * 142} y={280 + r * 92} width={122} height={6} fill="#eaf6ff" /></g>)}
        <rect x={x + 18 + d * 142} y={200} width={20} height={388} fill="#fff" opacity={0.18} /><rect x={x + 120 + d * 142} y={360} width={6} height={60} rx={3} fill="#d8dee6" /></g>)}
      {!dark && <Glow x={x + 220} y={420} r={360} color="#8ad0ff" o={day ? 0.08 : 0.35} />}
    </g>; })}
    <rect x={-800} y={600} width={3600} height={40} fill="#3a404c" />
    {/* hanging aisle sign */}
    <g transform="translate(860 150)"><line x1={-90} y1={-90} x2={-90} y2={0} stroke="#555" strokeWidth={3} /><line x1={90} y1={-90} x2={90} y2={0} stroke="#555" strokeWidth={3} />
      <rect x={-170} y={0} width={340} height={56} rx={8} fill="#2f8a4e" /><text x={0} y={38} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={28} fill="#fff">{sign}</text></g>
    {/* floor */}
    <rect x={-800} y={640} width={3600} height={700} fill={day ? "#d8d6cf" : dark ? "#14161c" : "#1e2634"} />
    {Array.from({ length: 30 }, (_, i) => <line key={i} x1={-800 + i * 130} y1={640} x2={-1400 + i * 170} y2={1300} stroke="#000" strokeOpacity={0.12} strokeWidth={3} />)}
    {[700, 780, 900, 1060].map(y => <line key={y} x1={-800} y1={y} x2={2800} y2={y} stroke="#000" strokeOpacity={0.12} strokeWidth={3} />)}
    {!dark && <rect x={-800} y={650} width={3600} height={120} fill={day ? "#fff" : "#8ad0ff"} opacity={day ? 0.12 : 0.08} />}
    <AO x={-800} y={640} w={3600} h={60} dir="down" o={0.5} />
    {/* side shelves (the aisle we're standing in, seen as end caps) */}
    <Shelf x={-640} y={900} w={520} seed={3} dim={day ? 1 : 0.55} empty={empty} />
    <Shelf x={1980} y={900} w={560} seed={8} dim={day ? 1 : 0.55} empty={empty} />
    {children}
    <Noise x={-800} y={-200} w={3600} h={1500} freq={0.7} o={0.12} />
  </g>;
};

// a crowd of infected, depth-sorted. rows: far→near. glass=true makes the nearest press against a window line.
export const Crowd: React.FC<{ f: number; x0: number; x1: number; y: number; n: number; s?: number; seed?: number; run?: number; dir?: 1 | -1; speed?: number; o?: number; dark?: number }> = ({ f, x0, x1, y, n, s = 0.6, seed = 1, run = 0, dir = -1, speed = 0, o = 1, dark = 0 }) => <g opacity={o}>
  {Array.from({ length: n }, (_, i) => { const xx = x0 + rnd(i, seed) * (x1 - x0) + speed * f * dir, yy = y + rnd(i, seed + 1) * 30; return { i, xx, yy }; })
    .sort((a, b) => a.yy - b.yy).map(({ i, xx, yy }) => <g key={i}><Character look={ZOMBIES[(i + seed) % ZOMBIES.length]} pose={{ facing: (rnd(i, seed + 4) > 0.8 ? -dir : dir) as 1 | -1, ...zombiePose(f, i + seed, run) }} x={xx} y={yy} s={s * (0.92 + rnd(i, seed + 2) * 0.16)} f={f} seed={i} />
      {dark > 0 && <ellipse cx={xx} cy={yy - 200 * s} rx={70 * s} ry={230 * s} fill="#05070c" opacity={dark} />}</g>)}
</g>;

// glass storefront seen from INSIDE at night: parking lot, lamp, crowd, hands on glass, cart barricade.
export const StoreFront: React.FC<{ f: number; crowd?: number; hands?: number; press?: number; cart?: boolean; lamp?: boolean; inside?: React.ReactNode; light?: Light; part?: "out" | "in" }> = ({ f, crowd = 30, hands = 0, press = 0, cart = true, lamp = true, inside, light = "night", part }) => {
  const flick = lamp ? (rnd(Math.floor(f / 3), 5) > 0.12 ? 1 : 0.35) : 0;
  const OUT = part !== "in", IN = part !== "out";
  return <g>
    {OUT && <g>
    {/* outside */}
    <rect x={-400} y={0} width={2720} height={1080} fill="#0a1020" />
    <rect x={-400} y={560} width={2720} height={520} fill="#121822" />
    {Array.from({ length: 10 }, (_, i) => <line key={i} x1={-200 + i * 260} y1={600} x2={-400 + i * 300} y2={820} stroke="#e8e4d0" strokeOpacity={0.18} strokeWidth={5} />)}
    {/* far city glow + smoke */}
    <rect x={-400} y={380} width={2720} height={180} fill="#1a2234" />
    {Array.from({ length: 16 }, (_, i) => <rect key={i} x={-380 + i * 170} y={330 + rnd(i, 3) * 120} width={120} height={300} fill="#141a28" />)}
    <Glow x={1500} y={460} r={500} color="#ff6a3a" o={0.18} />
    {lamp && <g><rect x={1310} y={150} width={12} height={480} fill="#3a3e48" /><path d="M1316 150 L1400 150" stroke="#3a3e48" strokeWidth={10} /><rect x={1380} y={146} width={60} height={14} rx={4} fill={flick > 0.5 ? "#fff3c8" : "#5a564a"} />
      <path d="M1380 160 L1440 160 L1640 640 L1180 640 Z" fill="#fff0b0" opacity={0.12 * flick} /><Glow x={1410} y={160} r={160} color="#ffe8a0" o={0.5 * flick} /></g>}
    {/* parked car silhouettes */}
    {[[-200, 600], [420, 610], [1700, 600]].map(([cx, cy], i) => <g key={i}><path d={`M${cx} ${cy} q20 -70 110 -80 h120 q80 10 110 80 v40 h-340 Z`} fill="#1a2030" /><circle cx={cx + 60} cy={cy + 40} r={22} fill="#0a0c12" /><circle cx={cx + 280} cy={cy + 40} r={22} fill="#0a0c12" /></g>)}
    <Crowd f={f} x0={-300} x1={2200} y={560} n={Math.round(crowd * 0.5)} s={0.32} seed={5} dark={0.25} />
    <Crowd f={f} x0={-300} x1={2200} y={660} n={Math.round(crowd * 0.35)} s={0.48} seed={9} dark={0.12} />
    <Crowd f={f} x0={-100} x1={2000} y={1000 + press * 30} n={Math.round(crowd * 0.25)} s={0.95} seed={13} />
    <rect x={-400} y={0} width={2720} height={1080} fill="#05080f" opacity={part === "out" ? 0.3 : 0} />
    </g>}
    {IN && <g>
    {/* window frame (inside): glass y 110..700, sill wall below */}
    <rect x={-400} y={0} width={2720} height={120} fill="#1c222e" />
    <rect x={-400} y={700} width={2720} height={200} fill="#262e3c" /><rect x={-400} y={700} width={2720} height={10} fill="#4a5262" />
    {Array.from({ length: 14 }, (_, i) => <rect key={i} x={-380 + i * 200} y={730} width={180} height={150} fill="#2c3444" />)}
    {/* glass door in the middle (chain + padlock on the push bars) */}
    <rect x={820} y={110} width={420} height={790} fill="#000" opacity={0} />
    {Array.from({ length: 8 }, (_, i) => <rect key={i} x={-300 + i * 330} y={110} width={26} height={600} fill="#2a303c" />)}
    <rect x={-400} y={110} width={2720} height={14} fill="#3a404c" />
    {Array.from({ length: 7 }, (_, i) => <path key={i} d={`M${-250 + i * 330} 124 l90 0 l-160 576 l-90 0 Z`} fill="#fff" opacity={0.035} />)}
    {/* hands on glass */}
    {Array.from({ length: hands }, (_, i) => { const hx = 80 + rnd(i, 21) * 1760, hy = 380 + rnd(i, 22) * 300, sc = 0.8 + rnd(i, 23) * 0.5, sl = Math.sin(f * 0.2 + i) * 3;
      return <g key={i} transform={`translate(${hx} ${hy + sl}) scale(${sc}) rotate(${(rnd(i, 24) - 0.5) * 40})`}>
        <ellipse cx={0} cy={0} rx={30} ry={36} fill="#6b8068" />{[-22, -8, 6, 20].map((fx, k) => <rect key={k} x={fx - 6} y={-74 + Math.abs(k - 1.5) * 6} width={13} height={44} rx={6} fill="#6b8068" />)}<rect x={26} y={-14} width={12} height={34} rx={6} fill="#6b8068" transform="rotate(30 30 0)" />
        <ellipse cx={0} cy={4} rx={36} ry={42} fill="#c8ffd0" opacity={0.05} /></g>; })}
    {/* interior floor + lighting */}
    <rect x={-400} y={890} width={2720} height={240} fill={light === "dark" ? "#0e1016" : "#1a2230"} />
    <AO x={-400} y={890} w={2720} h={40} dir="down" o={0.6} />
    {[-240, 1360].map(x => <g key={x}><rect x={x} y={300} width={14} height={300} fill="#2a303c" /></g>)}
    {cart && <><Cart x={820} y={1000} s={1.0} full /><Cart x={1120} y={1010} s={1.0} full flip /></>}
    <rect x={-400} y={0} width={2720} height={1080} fill="#4a8ac8" opacity={light === "dark" ? 0 : 0.06} style={{ mixBlendMode: "screen" }} />
    {inside}
    </g>}
  </g>;
};

// staff room: lockers, table, whiteboard (content as children inside board coords 0..760 x 0..440), lantern
export const StaffRoom: React.FC<{ f: number; board?: React.ReactNode; lantern?: number; children?: React.ReactNode; light?: Light }> = ({ f, board, lantern = 1, children, light = "dark" }) => {
  const fl = 0.9 + 0.1 * Math.sin(f * 0.7) * Math.sin(f * 0.31);
  return <g>
    <rect x={-600} y={-200} width={3200} height={1500} fill={light === "day" ? "#9aa49a" : "#24282e"} />
    <rect x={-600} y={-200} width={3200} height={860} fill={light === "day" ? "#a8b4a6" : "#3a3f48"} /><Noise x={-600} y={-200} w={3200} h={860} freq={0.6} o={0.2} />
    <rect x={-600} y={640} width={3200} height={20} fill="#1e221e" />
    {/* lockers */}
    {Array.from({ length: 5 }, (_, i) => <g key={i}><rect x={-420 + i * 110} y={180} width={104} height={460} fill="#5a6a7a" /><rect x={-410 + i * 110} y={200} width={84} height={14} fill="#3a4450" />{[0, 1, 2].map(k => <rect key={k} x={-404 + i * 110} y={226 + k * 8} width={70} height={3} fill="#3a4450" />)}<rect x={-340 + i * 110} y={400} width={8} height={30} rx={3} fill="#c8ccd4" /></g>)}
    <g transform="translate(140 200)"><rect x={0} y={0} width={160} height={210} fill="#f4efe0" /><rect x={14} y={14} width={132} height={60} fill="#2f8a4e" /><text x={80} y={54} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={22} fill="#fff">FRESHWAY</text>{[0, 1, 2, 3, 4].map(i => <rect key={i} x={20} y={96 + i * 20} width={120 - i * 12} height={8} fill="#9a9a90" />)}</g>
    <g transform="translate(1900 230)"><circle cx={0} cy={0} r={46} fill="#f4f4f0" stroke="#2a2a2a" strokeWidth={6} /><line x1={0} y1={0} x2={0} y2={-30} stroke="#2a2a2a" strokeWidth={5} /><line x1={0} y1={0} x2={22} y2={10} stroke="#2a2a2a" strokeWidth={5} /></g>
    {/* whiteboard */}
    <g transform="translate(560 120)"><rect x={-14} y={-14} width={788} height={468} rx={6} fill="#9aa0a8" /><rect x={0} y={0} width={760} height={440} fill="#f2f4f2" /><rect x={0} y={0} width={760} height={440} fill="url(#none)" />
      <path d="M20 20 L740 20" stroke="#000" strokeOpacity={0.04} strokeWidth={30} />{board}<rect x={200} y={446} width={360} height={14} rx={4} fill="#7a808a" /></g>
    {/* window with boards */}
    <g transform="translate(1520 150)"><rect x={0} y={0} width={300} height={260} fill="#0a1222" /><rect x={-10} y={-10} width={320} height={280} fill="none" stroke="#4a4e48" strokeWidth={14} />
      {[[-20, 40, -6], [-20, 120, 4], [-20, 200, -3]].map(([x, y, r], i) => <rect key={i} x={x} y={y} width={340} height={40} fill="#8a6a44" transform={`rotate(${r} 150 ${y})`} />)}</g>
    {/* floor */}
    <rect x={-600} y={660} width={3200} height={700} fill="#26291f" /><AO x={-600} y={660} w={3200} h={50} dir="down" o={0.5} />
    {/* table */}
    <rect x={300} y={720} width={1100} height={26} fill="#6a4e36" /><rect x={300} y={746} width={1100} height={8} fill="#3a2a1e" /><rect x={340} y={746} width={20} height={200} fill="#4a3626" /><rect x={1340} y={746} width={20} height={200} fill="#4a3626" />
    {/* clutter on the table: cans, map, first-aid box */}
    <rect x={420} y={680} width={120} height={40} rx={4} fill="#e8e4da" /><rect x={466} y={688} width={28} height={24} fill="#d8323a" /><rect x={474} y={694} width={12} height={12} fill="#fff" />
    {[0, 1, 2].map(i => <rect key={i} x={600 + i * 34} y={684} width={28} height={36} rx={3} fill={["#d8402e", "#f2b632", "#3a7ad8"][i]} />)}
    <path d="M820 712 L960 700 L1040 716 L900 726 Z" fill="#efe4c6" />
    {/* water bottles stack */}
    {Array.from({ length: 18 }, (_, i) => <rect key={i} x={1760 + (i % 6) * 34} y={880 - Math.floor(i / 6) * 70} width={28} height={66} rx={8} fill="#8ac8f0" opacity={0.75} />)}
    {children}
    {lantern > 0 && <g><rect x={1180} y={640} width={50} height={80} rx={8} fill="#2a2a2a" /><rect x={1188} y={652} width={34} height={56} rx={6} fill="#ffd88a" /><path d="M1186 640 Q1205 610 1224 640" stroke="#2a2a2a" strokeWidth={5} fill="none" />
      <Glow x={1205} y={680} r={900 * fl} color="#ffb84a" o={0.32 * lantern} /><Glow x={1205} y={680} r={160} color="#fff0c0" o={0.6 * lantern} /></g>}
  </g>;
};

// loading-dock door from inside (steel door with a peephole + roll-up shutter beside it); knock = shake
export const DockDoor: React.FC<{ f: number; knock?: number; open?: number; outside?: React.ReactNode; day?: boolean }> = ({ f, knock = 0, open = 0, outside, day = true }) => {
  const sh = knock ? Math.sin(f * 2.2) * 4 : 0;
  return <g>
    <rect x={-600} y={-200} width={3200} height={1500} fill="#262a30" /><Bricks2 />
    {/* roll-up shutter */}
    <g transform="translate(-260 140)"><rect x={0} y={0} width={640} height={620} fill="#5a606a" />{Array.from({ length: 20 }, (_, i) => <rect key={i} x={0} y={i * 31} width={640} height={6} fill="#3a3e46" />)}<rect x={-20} y={-20} width={680} height={24} fill="#3a3e46" /><rect x={270} y={560} width={100} height={20} rx={6} fill="#c8ccd4" /></g>
    {/* steel door */}
    <g transform={`translate(${860 + sh} 160)`}>
      <rect x={-20} y={-20} width={400} height={640} fill="#3a3e46" />
      <rect x={0} y={0} width={360} height={600} fill="#2a2e36" />
      {open > 0 && <g><clipPath id="dockclip"><rect x={0} y={0} width={360 * open} height={600} /></clipPath><g clipPath="url(#dockclip)"><rect x={0} y={0} width={360} height={600} fill={day ? "#d8e2ea" : "#0a1020"} />{outside}<rect x={0} y={0} width={360} height={600} fill="#fff" opacity={day ? 0.2 : 0} /></g></g>}
      <rect x={360 * open} y={0} width={360 * (1 - open * 0.85)} height={600} fill="#6a7280" /><rect x={360 * open + 20} y={20} width={Math.max(0, 360 * (1 - open * 0.85) - 40)} height={560} fill="#7a828e" />
      <circle cx={360 * open + 180 * (1 - open * 0.85)} cy={170} r={12} fill="#1a1c20" stroke="#aab0ba" strokeWidth={4} />
      <rect x={360 * open + 300 * (1 - open * 0.85)} y={300} width={40} height={14} rx={6} fill="#c8ccd4" />
      <rect x={360 * open + 30} y={250} width={Math.max(0, 360 * (1 - open * 0.85) - 60)} height={16} rx={4} fill="#a8323a" />
      <rect x={-6} y={600} width={372} height={10} fill="#1a1c20" />
      {day && open === 0 && <rect x={0} y={598} width={360} height={4} fill="#fff6d8" opacity={0.8} />}
    </g>
    <text x={1040} y={120} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={30} fill="#d8323a">DELIVERIES · STAFF ONLY</text>
    <rect x={-600} y={760} width={3200} height={600} fill="#2e3238" /><AO x={-600} y={760} w={3200} h={50} dir="down" o={0.5} />
    {/* pallets */}
    <g transform="translate(1420 760)">{[0, 1, 2].map(i => <g key={i}><rect x={0} y={-60 - i * 120} width={300} height={110} fill="#c89a5a" /><rect x={0} y={-60 - i * 120} width={300} height={110} fill="none" stroke="#8a6a3a" strokeWidth={4} /><text x={150} y={-0 - i * 120} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={22} fill="#6a4a2a">WATER · 24</text></g>)}</g>
  </g>;
};
const Bricks2: React.FC = () => <g opacity={0.35}>{Array.from({ length: 30 }, (_, r) => Array.from({ length: 30 }, (_, c) => <rect key={`${r}-${c}`} x={-600 + c * 110 + (r % 2) * 55} y={-200 + r * 40} width={104} height={34} fill="#2e3238" />))}</g>;

// helper: a character in a store scene with a contact shadow already handled by Character
export const P = (look: Look, pose: Pose, x: number, y: number, s: number, f: number, seed = 1, rim?: string) =>
  <Character look={look} pose={pose} x={x} y={y} s={s} f={f} seed={seed} rim={rim ? { dx: 4, dy: -3, color: rim } : null} />;
