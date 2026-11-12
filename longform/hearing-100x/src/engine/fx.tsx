// Lighting and atmosphere: glows, light shafts, vignette, animated film grain, rain, bokeh, colour grade.
import React from "react";
import { W, H, rnd } from "./core";
let gid = 0; const uid = (p: string) => `${p}${++gid}`;
export const Glow: React.FC<{ x: number; y: number; r: number; color: string; o?: number }> = ({ x, y, r, color, o = 1 }) => {
  const id = React.useMemo(() => uid("g"), []);
  return <g style={{ mixBlendMode: "screen" }}><defs><radialGradient id={id}><stop offset="0" stopColor={color} stopOpacity={o} /><stop offset="0.35" stopColor={color} stopOpacity={o * 0.35} /><stop offset="1" stopColor={color} stopOpacity={0} /></radialGradient></defs><circle cx={x} cy={y} r={r} fill={`url(#${id})`} /></g>;
};
// a soft beam from a polygon (e.g. window light falling into a room)
export const Shaft: React.FC<{ pts: number[][]; color: string; o?: number; blur?: number; from?: number[]; to?: number[] }> = ({ pts, color, o = 0.35, blur = 18, from, to }) => {
  const id = React.useMemo(() => uid("s"), []), fid = React.useMemo(() => uid("f"), []);
  const f = from ?? pts[0], t2 = to ?? pts[2];
  return <g style={{ mixBlendMode: "screen" }}><defs>
    <linearGradient id={id} gradientUnits="userSpaceOnUse" x1={f[0]} y1={f[1]} x2={t2[0]} y2={t2[1]}><stop offset="0" stopColor={color} stopOpacity={o} /><stop offset="1" stopColor={color} stopOpacity={0} /></linearGradient>
    <filter id={fid} x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation={blur} /></filter></defs>
    <polygon points={pts.map(p => p.join(",")).join(" ")} fill={`url(#${id})`} filter={`url(#${fid})`} /></g>;
};
export const Vignette: React.FC<{ o?: number; color?: string }> = ({ o = 0.75, color = "0,0,0" }) => (
  <div style={{ position: "absolute", inset: 0, pointerEvents: "none", background: `radial-gradient(ellipse at 50% 50%, rgba(${color},0) 45%, rgba(${color},${o}) 100%)` }} />
);
export const Grain: React.FC<{ f: number; o?: number }> = ({ f, o = 0.07 }) => (
  <svg width={W} height={H} style={{ position: "absolute", inset: 0, mixBlendMode: "overlay", opacity: o, pointerEvents: "none" }}>
    <filter id={`grain${f % 8}`}><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={f % 8} /><feColorMatrix type="saturate" values="0" /></filter>
    <rect width={W} height={H} filter={`url(#grain${f % 8})`} />
  </svg>
);
export const Grade: React.FC<{ top: string; bottom: string; mode?: any; o?: number }> = ({ top, bottom, mode = "soft-light", o = 0.5 }) => (
  <div style={{ position: "absolute", inset: 0, pointerEvents: "none", mixBlendMode: mode, opacity: o, background: `linear-gradient(${top}, ${bottom})` }} />
);
// falling rain streaks inside a box
export const Rain: React.FC<{ f: number; x: number; y: number; w: number; h: number; n?: number; color?: string; speed?: number; len?: number; slant?: number; o?: number }> = ({ f, x, y, w, h, n = 120, color = "#aac4ff", speed = 38, len = 40, slant = 0.18, o = 0.35 }) => (
  <g opacity={o}>{Array.from({ length: n }, (_, i) => { const yy = ((rnd(i, 1) * h + f * speed * (0.8 + rnd(i, 2) * 0.4)) % (h + len)) - len; const xx = rnd(i, 3) * w; return <line key={i} x1={x + xx} y1={y + yy} x2={x + xx - len * slant} y2={y + yy + len} stroke={color} strokeWidth={1.4 + rnd(i, 4)} strokeLinecap="round" />; })}</g>
);
// raindrops sliding on a window pane
export const PaneDrops: React.FC<{ f: number; x: number; y: number; w: number; h: number; n?: number }> = ({ f, x, y, w, h, n = 40 }) => (
  <g>{Array.from({ length: n }, (_, i) => { const sp = 0.4 + rnd(i, 5) * 2.2, yy = (rnd(i, 6) * h + f * sp * (rnd(i, 9) > 0.7 ? 1 : 0.15)) % h, xx = rnd(i, 7) * w, r = 1.6 + rnd(i, 8) * 3.2; return <g key={i}><line x1={x + xx} y1={y + yy - r * 6} x2={x + xx} y2={y + yy} stroke="rgba(200,220,255,0.12)" strokeWidth={r * 0.8} /><ellipse cx={x + xx} cy={y + yy} rx={r * 0.8} ry={r} fill="rgba(210,225,255,0.35)" /><ellipse cx={x + xx - r * 0.25} cy={y + yy - r * 0.3} rx={r * 0.25} ry={r * 0.3} fill="rgba(255,255,255,0.7)" /></g>; })}</g>
);
export const Bokeh: React.FC<{ x: number; y: number; w: number; h: number; n?: number; colors?: string[]; seed?: number; f?: number }> = ({ x, y, w, h, n = 30, colors = ["#ffd38a", "#ff9a6a", "#9ec8ff"], seed = 1, f = 0 }) => (
  <g style={{ mixBlendMode: "screen" }}>{Array.from({ length: n }, (_, i) => { const r = 6 + rnd(i, seed) * 22; return <circle key={i} cx={x + rnd(i, seed + 1) * w} cy={y + rnd(i, seed + 2) * h} r={r} fill={colors[i % colors.length]} opacity={0.18 + 0.25 * rnd(i, seed + 3) * (0.8 + 0.2 * Math.sin(f * 0.05 + i))} />; })}</g>
);
