// 2D cinematic engine: a 1920x1080 stage, a camera with parallax layers (depth), depth-of-field blur, and helpers.
import React from "react";
export const W = 1920, H = 1080;
export const sat = (v: number) => Math.min(1, Math.max(0, v));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const ease = (t: number) => { t = sat(t); return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
export const easeOut = (t: number) => 1 - Math.pow(1 - sat(t), 3);
export const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };
export type Cam = { x: number; y: number; zoom: number; rot?: number };
// piecewise camera keys: [frame, x, y, zoom]
export const camAt = (f: number, keys: number[][]): Cam => {
  if (f <= keys[0][0]) return { x: keys[0][1], y: keys[0][2], zoom: keys[0][3] };
  for (let i = 0; i < keys.length - 1; i++) if (f < keys[i + 1][0]) { const a = keys[i], b = keys[i + 1], u = ease((f - a[0]) / (b[0] - a[0])); return { x: lerp(a[1], b[1], u), y: lerp(a[2], b[2], u), zoom: lerp(a[3], b[3], u) }; }
  const k = keys[keys.length - 1]; return { x: k[1], y: k[2], zoom: k[3] };
};
export const CamCtx = React.createContext<Cam>({ x: 0, y: 0, zoom: 1 });
export const Stage: React.FC<{ cam: Cam; children: React.ReactNode; bg?: string }> = ({ cam, children, bg = "#000" }) => (
  <div style={{ position: "absolute", inset: 0, overflow: "hidden", background: bg }}><CamCtx.Provider value={cam}>{children}</CamCtx.Provider></div>
);
// depth 0 = infinitely far (static), 1 = the action plane, >1 = foreground. blur in px for depth of field.
export const Layer: React.FC<{ depth: number; blur?: number; children: React.ReactNode; style?: React.CSSProperties; svg?: boolean }> = ({ depth, blur = 0, children, style, svg = true }) => {
  const cam = React.useContext(CamCtx);
  const z = 1 + (cam.zoom - 1) * depth, tx = -cam.x * depth, ty = -cam.y * depth;
  const t = `translate(${W / 2}px,${H / 2}px) rotate(${(cam.rot ?? 0) * depth}deg) scale(${z}) translate(${tx}px,${ty}px) translate(${-W / 2}px,${-H / 2}px)`;
  return <div style={{ position: "absolute", inset: 0, transform: t, transformOrigin: "0 0", filter: blur ? `blur(${blur}px)` : undefined, ...style }}>
    {svg ? <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ overflow: "visible", position: "absolute" }}>{children}</svg> : children}
  </div>;
};
