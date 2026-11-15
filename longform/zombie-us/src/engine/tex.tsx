// Procedural textures for richer backgrounds: noise, wood grain, wallpaper, bricks, ambient occlusion.
import React from "react";
let n = 0; const uid = (p: string) => `${p}${++n}`;
// fine noise multiplied over an area (paint / plaster / concrete)
export const Noise: React.FC<{ x: number; y: number; w: number; h: number; freq?: number; o?: number; seed?: number; blend?: any; stretch?: number }> = ({ x, y, w, h, freq = 0.8, o = 0.25, seed = 1, blend = "multiply", stretch = 1 }) => {
  const id = React.useMemo(() => uid("nz"), []);
  return <g style={{ mixBlendMode: blend }} opacity={o}><defs><filter id={id} x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency={`${freq / stretch} ${freq}`} numOctaves={3} seed={seed} /><feColorMatrix type="saturate" values="0" /></filter></defs><rect x={x} y={y} width={w} height={h} filter={`url(#${id})`} /></g>;
};
// wooden floor planks with grain
export const Wood: React.FC<{ x: number; y: number; w: number; h: number; color: string; rows?: number; seed?: number }> = ({ x, y, w, h, color, rows = 8, seed = 2 }) => {
  const rh = h / rows;
  return <g>
    <rect x={x} y={y} width={w} height={h} fill={color} />
    {Array.from({ length: rows }, (_, r) => <g key={r}>
      <rect x={x} y={y + r * rh} width={w} height={rh} fill={r % 2 ? "#000" : "#fff"} opacity={0.035} />
      <line x1={x} y1={y + r * rh} x2={x + w} y2={y + r * rh} stroke="#000" strokeWidth={2.5} opacity={0.45} />
      {Array.from({ length: 6 }, (_, k) => { const px = x + ((k * 397 + r * 211) % w); return <line key={k} x1={px} y1={y + r * rh} x2={px} y2={y + (r + 1) * rh} stroke="#000" strokeWidth={2} opacity={0.35} />; })}
    </g>)}
    <Noise x={x} y={y} w={w} h={h} freq={0.06} stretch={14} o={0.35} seed={seed} />
  </g>;
};
// wallpaper: a repeating motif pattern
export const Wallpaper: React.FC<{ x: number; y: number; w: number; h: number; base: string; ink: string; kind?: "diamond" | "floral" | "stripe"; o?: number }> = ({ x, y, w, h, base, ink, kind = "diamond", o = 0.18 }) => {
  const id = React.useMemo(() => uid("wp"), []);
  return <g><defs><pattern id={id} width={kind === "stripe" ? 60 : 90} height={90} patternUnits="userSpaceOnUse">
    {kind === "diamond" && <><path d="M45 8 L60 45 L45 82 L30 45 Z" fill="none" stroke={ink} strokeWidth={2} /><circle cx={0} cy={0} r={4} fill={ink} /><circle cx={90} cy={90} r={4} fill={ink} /><circle cx={0} cy={90} r={4} fill={ink} /><circle cx={90} cy={0} r={4} fill={ink} /></>}
    {kind === "floral" && <><circle cx={45} cy={45} r={9} fill={ink} /><circle cx={45} cy={30} r={7} fill={ink} /><circle cx={45} cy={60} r={7} fill={ink} /><circle cx={30} cy={45} r={7} fill={ink} /><circle cx={60} cy={45} r={7} fill={ink} /><path d="M0 0 Q10 20 0 40" stroke={ink} strokeWidth={2} fill="none" /></>}
    {kind === "stripe" && <><rect x={0} y={0} width={18} height={90} fill={ink} /><rect x={30} y={0} width={4} height={90} fill={ink} /></>}
  </pattern></defs>
    <rect x={x} y={y} width={w} height={h} fill={base} /><rect x={x} y={y} width={w} height={h} fill={`url(#${id})`} opacity={o} />
    <Noise x={x} y={y} w={w} h={h} freq={0.9} o={0.18} />
  </g>;
};
export const Bricks: React.FC<{ x: number; y: number; w: number; h: number; color: string; mortar?: string; bw?: number; bh?: number; o?: number }> = ({ x, y, w, h, color, mortar = "#000", bw = 64, bh = 26, o = 0.5 }) => {
  const id = React.useMemo(() => uid("br"), []);
  return <g><defs><pattern id={id} width={bw} height={bh * 2} patternUnits="userSpaceOnUse"><path d={`M0 0 H${bw} M0 ${bh} H${bw} M${bw / 2} 0 V${bh} M0 ${bh} V${bh * 2}`} stroke={mortar} strokeWidth={3} /></pattern></defs>
    <rect x={x} y={y} width={w} height={h} fill={color} /><rect x={x} y={y} width={w} height={h} fill={`url(#${id})`} opacity={o} />
    <Noise x={x} y={y} w={w} h={h} freq={0.5} o={0.3} seed={4} />
  </g>;
};
// ambient occlusion: a dark gradient band along an edge (where wall meets floor, corners, under furniture)
export const AO: React.FC<{ x: number; y: number; w: number; h: number; dir?: "up" | "down" | "left" | "right"; o?: number }> = ({ x, y, w, h, dir = "up", o = 0.6 }) => {
  const id = React.useMemo(() => uid("ao"), []);
  const v = { up: [0, 1, 0, 0], down: [0, 0, 0, 1], left: [1, 0, 0, 0], right: [0, 0, 1, 0] }[dir];
  return <g><defs><linearGradient id={id} x1={v[0]} y1={v[1]} x2={v[2]} y2={v[3]}><stop offset="0" stopColor="#000" stopOpacity={o} /><stop offset="1" stopColor="#000" stopOpacity={0} /></linearGradient></defs><rect x={x} y={y} width={w} height={h} fill={`url(#${id})`} /></g>;
};
