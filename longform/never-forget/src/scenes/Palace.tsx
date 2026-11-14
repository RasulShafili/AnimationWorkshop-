// The MEMORY PALACE: Lina's mind as an endless indigo library where every day of her life is a glowing door.
// PalaceCorridor = first-person perspective dolly (camera z moves forward); PalaceHall = side view with Lina walking.
import React from "react";
import { Layer, W, H, rnd, sat, lerp } from "../engine/core";
import { Glow, Shaft } from "../engine/fx";
import { Character, walkPose, Pose } from "../chars/Rig2";
import { LINA } from "../chars/cast";

const GOLD = "#ffc94a";
const VIG = ["#e8a46a", "#6ab0d8", "#8ac87a", "#d87a9a", "#c8a0e8", "#e8d07a", "#7ad0c0", "#f0907a"];
const MON = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
export const dateOf = (i: number) => { const d = new Date(Date.UTC(2010, 2, 14) + i * 86400000); return `${String(d.getUTCDate()).padStart(2, "0")} ${MON[d.getUTCMonth()]} ${d.getUTCFullYear()}`; };

// a tiny scene inside an open door (a remembered day): sky/room colour, ground, a figure, a sun/lamp
export const Vignette: React.FC<{ x: number; y: number; w: number; h: number; i: number; dark?: boolean }> = ({ x, y, w, h, i, dark }) => {
  const c = VIG[i % VIG.length], kind = Math.floor(rnd(i, 4) * 4);
  if (dark) return <rect x={x} y={y} width={w} height={h} fill="#05040a" />;
  return <g>
    <rect x={x} y={y} width={w} height={h} fill={c} />
    <rect x={x} y={y + h * 0.66} width={w} height={h * 0.34} fill="#000" opacity={0.25} />
    <circle cx={x + w * (0.25 + rnd(i, 5) * 0.5)} cy={y + h * 0.24} r={w * 0.09} fill="#fff6d0" opacity={0.9} />
    {kind === 0 && <path d={`M${x + w * 0.2} ${y + h * 0.66} L${x + w * 0.4} ${y + h * 0.4} L${x + w * 0.6} ${y + h * 0.66} Z`} fill="#000" opacity={0.3} />}
    {kind === 1 && <rect x={x + w * 0.55} y={y + h * 0.4} width={w * 0.3} height={h * 0.26} fill="#000" opacity={0.28} />}
    {kind === 2 && <ellipse cx={x + w * 0.5} cy={y + h * 0.7} rx={w * 0.35} ry={h * 0.05} fill="#fff" opacity={0.35} />}
    <circle cx={x + w * 0.42} cy={y + h * 0.48} r={w * 0.07} fill="#1d1a26" /><rect x={x + w * 0.37} y={y + h * 0.53} width={w * 0.1} height={h * 0.14} rx={w * 0.03} fill="#1d1a26" />
    {kind === 3 && <><circle cx={x + w * 0.6} cy={y + h * 0.5} r={w * 0.06} fill="#1d1a26" /><rect x={x + w * 0.555} y={y + h * 0.545} width={w * 0.09} height={h * 0.12} rx={w * 0.03} fill="#1d1a26" /></>}
  </g>;
};

// one door. open 0..1 = how far the door leaf has swung (reveals the vignette). label under it.
export const Door: React.FC<{ x: number; y: number; w: number; h: number; i: number; open?: number; glow?: number; label?: string; dark?: boolean; fog?: number }> = ({ x, y, w, h, i, open = 0.75, glow = 1, label, dark, fog = 0 }) => {
  const leaf = w * (1 - open * 0.85);
  return <g opacity={1 - fog * 0.15}>
    {!dark && <rect x={x - w * 0.12} y={y - w * 0.12} width={w * 1.24} height={h + w * 0.12} rx={w * 0.08} fill={GOLD} opacity={0.22 * glow} style={{ filter: `blur(${Math.max(2, w * 0.08)}px)` }} />}
    <path d={`M${x - w * 0.08} ${y + h} L${x - w * 0.08} ${y + w * 0.42} A${w * 0.58} ${w * 0.58} 0 0 1 ${x + w * 1.08} ${y + w * 0.42} L${x + w * 1.08} ${y + h} Z`} fill={dark ? "#2a2636" : "#8a6a3a"} />
    <path d={`M${x} ${y + h} L${x} ${y + w * 0.5} A${w * 0.5} ${w * 0.5} 0 0 1 ${x + w} ${y + w * 0.5} L${x + w} ${y + h} Z`} fill="#000" />
    <clipPath id={`dc${i}_${Math.round(x)}`}><path d={`M${x} ${y + h} L${x} ${y + w * 0.5} A${w * 0.5} ${w * 0.5} 0 0 1 ${x + w} ${y + w * 0.5} L${x + w} ${y + h} Z`} /></clipPath>
    <g clipPath={`url(#dc${i}_${Math.round(x)})`}>
      <Vignette x={x} y={y} w={w} h={h} i={i} dark={dark} />
      {/* the door leaf, swung inward (narrower = more open) */}
      <rect x={x} y={y} width={leaf} height={h} fill={dark ? "#1a1724" : "#5a3a24"} />
      <rect x={x + leaf - w * 0.05} y={y} width={w * 0.05} height={h} fill="#000" opacity={0.35} />
      {leaf > w * 0.3 && <circle cx={x + leaf - w * 0.12} cy={y + h * 0.58} r={w * 0.035} fill={GOLD} />}
      {fog > 0 && <><rect x={x} y={y} width={w} height={h} fill="#cfc8f0" opacity={fog * 0.88} />{[0, 1, 2].map(j => <ellipse key={j} cx={x + w * (0.3 + 0.2 * j)} cy={y + h * (0.35 + 0.18 * j)} rx={w * 0.4} ry={h * 0.08} fill="#fff" opacity={0.35 * fog} />)}</>}
    </g>
    {label && <g><rect x={x + w * 0.08} y={y + h + w * 0.06} width={w * 0.84} height={w * 0.2} rx={w * 0.04} fill="#1a1424" stroke={GOLD} strokeWidth={Math.max(1, w * 0.012)} />
      <text x={x + w / 2} y={y + h + w * 0.205} fontFamily="Inter" fontWeight={800} fontSize={w * 0.11} fill={GOLD} textAnchor="middle">{label}</text></g>}
  </g>;
};

// first-person dolly through the corridor. z = camera distance travelled (world units). doorStart = index of the
// first door (door i shows dateOf(i)); fogFirst = number of first doors that are fogged (infantile amnesia).
export const PalaceCorridor: React.FC<{ f: number; z: number; doorStart?: number; fogFirst?: number; darkDoor?: number; brightEnd?: number; sway?: number }> = ({ f, z, doorStart = 2000, fogFirst = 0, darkDoor = -1, brightEnd = 1, sway = 0 }) => {
  const VX = 960 + sway, VY = 470, F = 700, D = 300, HALF = 420, FLOOR = 300, DOORH = 360, DOORW = 200;
  const items: React.ReactNode[] = [];
  const first = Math.floor(z / D) - 1;
  for (let k = first + 26; k >= Math.max(0, first); k--) {
    const dz = k * D - z + 200; if (dz < 60) continue;
    const s = F / dz, fogA = sat((dz - 2600) / 4000);
    for (const side of [-1, 1]) {
      const idx = doorStart + k * 2 + (side > 0 ? 1 : 0);
      const xIn = VX + side * HALF * s, w = DOORW * s * 0.95, h = DOORH * s;
      const x = side < 0 ? xIn - w * 0.15 - w : xIn + w * 0.15;
      const yb = VY + FLOOR * s;
      // bookshelf panel between doors
      items.push(<g key={`s${k}${side}`} opacity={1 - fogA}>
        <rect x={side < 0 ? x - w * 0.6 : x + w * 1.1} y={yb - h * 1.3} width={w * 0.5} height={h * 1.3} fill="#2a2140" />
        {Array.from({ length: 6 }, (_, r) => <rect key={r} x={side < 0 ? x - w * 0.58 : x + w * 1.12} y={yb - h * 1.3 + r * h * 0.21 + h * 0.03} width={w * 0.46} height={h * 0.16} fill={VIG[(idx + r) % 8]} opacity={0.45} />)}
      </g>);
      const fog = idx - doorStart < fogFirst ? 1 : 0;
      items.push(<g key={`d${k}${side}`} opacity={1 - fogA * 0.9}><Door x={x} y={yb - h} w={w} h={h} i={idx} open={fog ? 0 : 0.55 + 0.3 * rnd(idx, 2)} glow={fog ? 0.2 : 1} label={fog ? `AGE ${idx - doorStart}` : dateOf(idx)} dark={idx === darkDoor} fog={fog} /></g>);
    }
    // ceiling arch + hanging lamp per bay
    const yb = VY + FLOOR * s, yt = VY - 420 * s;
    items.push(<g key={`a${k}`} opacity={1 - fogA}>
      <path d={`M${VX - HALF * s * 1.25} ${yb - 560 * s} Q${VX} ${yt - 260 * s} ${VX + HALF * s * 1.25} ${yb - 560 * s}`} stroke="#3a2e58" strokeWidth={Math.max(2, 26 * s)} fill="none" />
      <line x1={VX} y1={yt - 140 * s} x2={VX} y2={yt - 40 * s} stroke="#1a1428" strokeWidth={Math.max(1, 4 * s)} />
      <circle cx={VX} cy={yt - 30 * s} r={Math.max(2, 16 * s)} fill="#fff1c0" /><circle cx={VX} cy={yt - 30 * s} r={Math.max(4, 70 * s)} fill={GOLD} opacity={0.12} />
    </g>);
  }
  return <svg width={W} height={H} style={{ position: "absolute" }}>
    <defs>
      <radialGradient id="pc_bg" cx="0.5" cy="0.43" r="0.75"><stop offset="0" stopColor="#fff0c8" stopOpacity={brightEnd} /><stop offset="0.12" stopColor="#8a6ac8" /><stop offset="0.6" stopColor="#1e1638" /><stop offset="1" stopColor="#07050f" /></radialGradient>
      <linearGradient id="pc_fl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#2a2048" /><stop offset="1" stopColor="#0c0918" /></linearGradient>
    </defs>
    <rect width={W} height={H} fill="url(#pc_bg)" />
    <path d={`M0 ${H} L${VX - 30} ${VY + 30} L${VX + 30} ${VY + 30} L${W} ${H} Z`} fill="url(#pc_fl)" />
    {/* marble floor lines toward the vanishing point + reflections of the door glow */}
    {Array.from({ length: 12 }, (_, i) => <line key={i} x1={VX + (i - 5.5) * 6} y1={VY + 30} x2={VX + (i - 5.5) * 380} y2={H} stroke="#fff" strokeOpacity={0.05} strokeWidth={2} />)}
    {Array.from({ length: 14 }, (_, i) => { const dz = ((i * 300 - z) % 4200 + 4200) % 4200 + 200, s = 700 / dz; return <line key={`h${i}`} x1={0} y1={VY + 300 * s} x2={W} y2={VY + 300 * s} stroke="#fff" strokeOpacity={0.04 * Math.min(1, s * 2)} strokeWidth={2} />; })}
    {items}
    <ellipse cx={VX} cy={VY + 120} rx={200} ry={30} fill={GOLD} opacity={0.12} />
    <Glow x={VX} y={VY} r={360} color="#fff0c8" o={0.55 * brightEnd} />
    {/* god rays + dust */}
    <Shaft pts={[[VX - 40, VY - 60], [VX + 40, VY - 60], [VX + 520, H], [VX - 520, H]]} color="#ffe8b0" o={0.12} blur={30} />
    {Array.from({ length: 70 }, (_, i) => { const px = rnd(i, 1) * W, py = ((rnd(i, 2) * H + f * (0.3 + rnd(i, 3) * 0.6)) % H), r = 1 + rnd(i, 4) * 2.5;
      return <circle key={`m${i}`} cx={px + Math.sin(f / 40 + i) * 12} cy={H - py} r={r} fill="#ffe8b0" opacity={0.25 + 0.35 * rnd(i, 5)} />; })}
  </svg>;
};

// side view hall: doors along the back wall (depth 1), Lina walks in front; pillars in the foreground.
export const PalaceHall: React.FC<{ f: number; linaX: number; lina?: Pose; walking?: boolean; doorStart?: number; openDoor?: number; openK?: number; darkDoor?: number; fogUntil?: number; pillars?: boolean; shake?: number; dim?: number }> = ({ f, linaX, lina = {}, walking = true, doorStart = 2400, openDoor = -1, openK = 0, darkDoor = -1, fogUntil = -1, pillars = true, shake = 0, dim = 0 }) => {
  const doors = Array.from({ length: 16 }, (_, k) => k);
  return <>
    <Layer depth={0.45}>
      <rect x={-1200} y={-500} width={4400} height={1300} fill="#140f26" />
      {Array.from({ length: 22 }, (_, i) => <g key={i}><rect x={-1100 + i * 200} y={-200} width={160} height={700} fill="#1e1638" />
        {Array.from({ length: 9 }, (_, r) => <rect key={r} x={-1094 + i * 200} y={-190 + r * 76} width={148} height={56} fill={VIG[(i + r) % 8]} opacity={0.18} />)}</g>)}
      <Glow x={960} y={-100} r={900} color="#8a6ac8" o={0.35} />
    </Layer>
    <Layer depth={1}>
      <rect x={-1400} y={120} width={4800} height={580} fill="#241a44" />
      {doors.map(k => { const x = -1200 + k * 300, idx = doorStart + k;
        const fog = k < fogUntil; return <g key={k} transform={idx === darkDoor && shake ? `translate(${Math.sin(f * 2.3) * 4 * shake} 0)` : undefined}><Door x={x} y={300} w={190} h={360} i={idx} open={fog ? 0 : k === openDoor ? 0.2 + 0.8 * openK : 0.15} glow={fog ? 0.2 : k === openDoor ? 1.6 : 0.8} label={fog ? `AGE ${k}` : dateOf(idx)} dark={idx === darkDoor} fog={fog ? 1 : 0} /></g>; })}
      <rect x={-1400} y={700} width={4800} height={500} fill="#120d22" />
      <rect x={-1400} y={700} width={4800} height={10} fill="#3a2e58" />
      {doors.map(k => <ellipse key={k} cx={-1105 + k * 300} cy={760} rx={110} ry={16} fill={GOLD} opacity={0.08} />)}
      {Array.from({ length: 40 }, (_, i) => <circle key={i} cx={-1200 + rnd(i, 7) * 4400} cy={((rnd(i, 8) * 900 - f * (0.4 + rnd(i, 9))) % 900 + 900) % 900} r={1.5 + rnd(i, 3) * 2} fill="#ffe8b0" opacity={0.4} />)}
      <Character look={LINA} pose={{ ...(walking ? walkPose(((lina.facing ?? 1) * linaX + 4000) / 290 * Math.PI * 2) : {}), facing: 1, gold: 0.9, look: [0.8, -0.2], ...lina }} x={linaX} y={740} s={1.0} f={f} seed={1} rim={{ dx: 4, dy: -3, color: GOLD }} />
    </Layer>
    {dim > 0 && <Layer depth={1}><rect x={-1600} y={-700} width={5200} height={2200} fill="#05030c" opacity={dim} /></Layer>}
    {pillars && <Layer depth={1.35} blur={7}>
      {[-900, 260, 1700, 2900].map((px, i) => <g key={i}><rect x={px} y={-300} width={120} height={1600} fill="#0a0716" /><rect x={px + 10} y={-300} width={14} height={1600} fill={GOLD} opacity={0.18} /></g>)}
    </Layer>}
  </>;
};
