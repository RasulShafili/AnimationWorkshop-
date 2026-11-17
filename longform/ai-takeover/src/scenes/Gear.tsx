// Vehicles + weapon FX (our own designs): Walt's rusty orange 1972 pickup (plate WHAT-IF), the army Humvee with a
// mounted gun, delivery/search drones (FRESHWAY boxes = zombie easter egg), and cartoon combat FX — muzzle flash,
// metal sparks, the hunters' net (flying + wrapped), stun dart with a blue zap trail, red laser dot, drone explosion.
// No blood anywhere: humans shoot, robots catch.
import React from "react";
import { rnd, sat, lerp } from "../engine/core";
import { Glow } from "../engine/fx";
import { Wheel } from "./z/Cars";
import { ORIN_BLUE, ORIN_RED } from "./City";

// pickup side view, facing right, origin = ground under the middle. ~560 long.
export const Pickup: React.FC<{ wheelRot?: number; bounce?: number; lights?: boolean; walt?: React.ReactNode; dent?: number; claws?: number }> = ({ wheelRot = 0, bounce = 0, lights, walt, dent = 0, claws = 0 }) => <g>
  <ellipse cx={0} cy={4} rx={300} ry={16} fill="#000" opacity={0.3} />
  <g transform={`translate(0 ${-bounce})`}>
    <path d="M-280 -60 L-280 -150 L40 -150 L60 -160 L80 -250 L210 -250 Q240 -250 250 -220 L270 -160 L300 -150 Q316 -146 316 -120 L316 -60 Z" fill="#d8742a" />
    <path d="M-280 -150 L40 -150 L40 -134 L-280 -134 Z" fill="#b85a1e" />
    {/* rust patches */}
    {[[-220, -100, 30], [120, -90, 22], [-60, -120, 18]].map(([x, y, r], i) => <ellipse key={i} cx={x} cy={y} rx={r} ry={r * 0.6} fill="#8a4a1e" opacity={0.6} />)}
    <path d="M96 -240 L200 -240 Q222 -240 230 -216 L246 -166 L96 -166 Z" fill="#9ac0d8" />
    <path d="M110 -236 L150 -236 L120 -170 L100 -170 Z" fill="#fff" opacity={0.3} />
    {walt && <g>{walt}</g>}
    <rect x={56} y={-160} width={6} height={100} fill="#a85a1e" />
    <rect x={250} y={-124} width={66} height={14} rx={4} fill="#c8c8c0" /><rect x={-288} y={-90} width={20} height={30} fill="#c8c8c0" />
    <rect x={296} y={-148} width={22} height={18} rx={4} fill={lights ? "#fff4c0" : "#e8e0c0"} />
    {lights && <path d="M318 -140 L1100 -260 L1100 0 Z" fill="#fff4c0" opacity={0.12} />}
    {/* plate WHAT-IF (easter egg) */}
    <rect x={-300} y={-120} width={44} height={22} rx={2} fill="#f4f0e0" stroke="#2a2a2a" strokeWidth={2} /><text x={-278} y={-104} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={8} fill="#2a3a6a">WHAT-IF</text>
    {/* claw holes in the roof (c9) */}
    {claws > 0 && [0, 1, 2].map(i => <path key={i} d={`M${140 + i * 22} -250 l6 ${30 * claws} l6 ${-30 * claws}`} fill="#2a2e38" />)}
    {dent > 0 && <path d="M90 -250 Q150 -230 210 -250" stroke="#8a4a1e" strokeWidth={6} fill="none" />}
  </g>
  <Wheel cx={-170} cy={-50} r={50} rot={wheelRot} /><Wheel cx={200} cy={-50} r={50} rot={wheelRot} />
</g>;

export const Humvee: React.FC<{ wheelRot?: number; f: number; firing?: boolean; gunner?: React.ReactNode }> = ({ wheelRot = 0, f, firing, gunner }) => <g>
  <ellipse cx={0} cy={4} rx={320} ry={18} fill="#000" opacity={0.3} />
  <path d="M-300 -60 L-300 -190 L-120 -200 L-60 -280 L150 -280 L200 -200 L300 -190 L310 -60 Z" fill="#6a6a4a" />
  <path d="M-40 -270 L140 -270 L180 -206 L-80 -206 Z" fill="#3a4250" /><rect x={-300} y={-130} width={610} height={10} fill="#4e4e36" />
  {gunner}
  <rect x={20} y={-330} width={60} height={50} rx={6} fill="#4e4e36" /><rect x={70} y={-318} width={110} height={12} fill="#2a2a2a" />
  {firing && <g><Glow x={186} y={-312} r={60} color="#ffd38a" o={0.5 + 0.5 * (f % 3 === 0 ? 1 : 0)} />{f % 3 !== 2 && <path d="M180 -312 l50 -14 l-14 14 l14 14 Z" fill="#fff4c0" />}</g>}
  <Wheel cx={-180} cy={-56} r={58} rot={wheelRot} /><Wheel cx={190} cy={-56} r={58} rot={wheelRot} />
</g>;

// drone: kind "delivery" (FRESHWAY box) | "search" (spotlight) ; eye = blue / red
export const Drone: React.FC<{ x: number; y: number; s?: number; f: number; kind?: "delivery" | "search"; red?: boolean; beam?: number; tilt?: number; speaker?: number }> = ({ x, y, s = 1, f, kind = "delivery", red, beam = 0, tilt = 0, speaker = 0 }) => {
  const eye = red ? ORIN_RED : ORIN_BLUE;
  return <g transform={`translate(${x} ${y + Math.sin(f * 0.25) * 4}) rotate(${tilt}) scale(${s})`}>
    {beam > 0 && <path d="M-20 20 L-260 700 L260 700 L20 20 Z" fill="#fff4d0" opacity={0.12 * beam} />}
    {[-1, 1].map(k => <g key={k}><line x1={k * 30} y1={-6} x2={k * 80} y2={-20} stroke="#3a3e48" strokeWidth={8} strokeLinecap="round" />
      <ellipse cx={k * 80} cy={-26} rx={46} ry={5} fill="#9aa4b4" opacity={0.45} /><rect x={k * 80 - 6} y={-30} width={12} height={10} fill="#2a2e38" />
      <line x1={k * 80 + Math.sin(f * 2 + k) * 44} y1={-27} x2={k * 80 - Math.sin(f * 2 + k) * 44} y2={-25} stroke="#e8eef4" strokeWidth={2} opacity={0.6} /></g>)}
    <rect x={-44} y={-18} width={88} height={34} rx={14} fill="#eef1f5" /><rect x={-44} y={4} width={88} height={12} rx={6} fill="#c8ced6" />
    <circle cx={0} cy={2} r={9} fill="#0b0e14" /><circle cx={0} cy={2} r={5} fill={eye} /><Glow x={0} y={2} r={26} color={eye} o={0.5} />
    {kind === "delivery" && <g><line x1={-16} y1={16} x2={-20} y2={40} stroke="#3a3e48" strokeWidth={3} /><line x1={16} y1={16} x2={20} y2={40} stroke="#3a3e48" strokeWidth={3} />
      <rect x={-34} y={40} width={68} height={50} rx={4} fill="#c89a5a" /><rect x={-34} y={52} width={68} height={12} fill="#2f8a4e" /><text x={0} y={62} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={9} fill="#fff">FRESHWAY</text></g>}
    {kind === "search" && <rect x={-14} y={16} width={28} height={16} rx={4} fill="#3a3e48" />}
    {speaker > 0 && [1, 2, 3].map(i => <path key={i} d={`M${50 + i * 14} -10 q10 14 0 28`} stroke={eye} strokeWidth={3} fill="none" opacity={speaker * (0.4 + 0.6 * Math.abs(Math.sin(f * 0.3 + i)))} />)}
  </g>; };

// ---------- combat FX ----------
export const Muzzle: React.FC<{ x: number; y: number; ang?: number; k: number; s?: number }> = ({ x, y, ang = 0, k, s = 1 }) => k <= 0 ? null :
  <g transform={`translate(${x} ${y}) rotate(${ang}) scale(${s * (0.6 + 0.4 * k)})`} opacity={k}><Glow x={0} y={0} r={90} color="#ffcf6a" o={0.7} />
    <path d="M0 0 L70 -18 L52 0 L90 4 L50 12 L66 34 Z" fill="#fff4c0" /><path d="M0 0 L40 -8 L30 0 L50 4 L30 8 Z" fill="#ffb02a" /></g>;
export const Sparks: React.FC<{ x: number; y: number; t: number; n?: number; seed?: number; s?: number }> = ({ x, y, t, n = 14, seed = 1, s = 1 }) => t < 0 || t > 20 ? null :
  <g>{t < 4 && <Glow x={x} y={y} r={60 * s} color="#ffd38a" o={0.8} />}{Array.from({ length: n }, (_, i) => { const a = rnd(i, seed) * Math.PI * 2, v = (4 + rnd(i, seed + 1) * 10) * s, px = x + Math.cos(a) * v * t, py = y + Math.sin(a) * v * t + 0.4 * t * t;
    return <line key={i} x1={px} y1={py} x2={px - Math.cos(a) * v * 1.4} y2={py - Math.sin(a) * v * 1.4 - 0.8 * t} stroke="#ffe08a" strokeWidth={3 * s} strokeLinecap="round" opacity={1 - t / 20} />; })}</g>;
// a net flying from (x0,y0) to (x1,y1) over k 0..1, unfolding; wrap = wrapped around something at the end
export const NetShot: React.FC<{ x0: number; y0: number; x1: number; y1: number; k: number; s?: number }> = ({ x0, y0, x1, y1, k, s = 1 }) => {
  if (k <= 0) return null; const x = lerp(x0, x1, sat(k)), y = lerp(y0, y1, sat(k)) - Math.sin(Math.PI * sat(k)) * 60, r = (20 + 90 * sat(k * 1.4)) * s;
  return <g transform={`translate(${x} ${y})`}>{[0, 1, 2, 3].map(i => { const a = i * Math.PI / 2 + k * 2; return <circle key={i} cx={Math.cos(a) * r} cy={Math.sin(a) * r} r={7 * s} fill="#3a3e48" />; })}
    <g opacity={0.9}>{Array.from({ length: 7 }, (_, i) => <line key={i} x1={-r} y1={-r + i * r / 3} x2={r} y2={-r + i * r / 3} stroke="#c8d0dc" strokeWidth={2.5 * s} />)}{Array.from({ length: 7 }, (_, i) => <line key={i} x1={-r + i * r / 3} y1={-r} x2={-r + i * r / 3} y2={r} stroke="#c8d0dc" strokeWidth={2.5 * s} />)}</g></g>; };
export const NetWrap: React.FC<{ x: number; y: number; w: number; h: number }> = ({ x, y, w, h }) => <g opacity={0.9}>
  {Array.from({ length: 9 }, (_, i) => <path key={i} d={`M${x - w / 2} ${y - h + i * h / 8} Q${x} ${y - h + i * h / 8 + 12} ${x + w / 2} ${y - h + i * h / 8}`} stroke="#c8d0dc" strokeWidth={3} fill="none" />)}
  {Array.from({ length: 7 }, (_, i) => <line key={i} x1={x - w / 2 + i * w / 6} y1={y - h} x2={x - w / 2 + i * w / 6 + 6} y2={y} stroke="#c8d0dc" strokeWidth={3} />)}</g>;
export const Dart: React.FC<{ x0: number; y0: number; x1: number; y1: number; k: number; f: number }> = ({ x0, y0, x1, y1, k, f }) => {
  if (k <= 0 || k > 1.3) return null; const kk = sat(k), x = lerp(x0, x1, kk), y = lerp(y0, y1, kk);
  const zig = Array.from({ length: 8 }, (_, i) => { const t = i / 7, px = lerp(x0, x, t), py = lerp(y0, y, t) + (i % 2 ? 1 : -1) * 10 * Math.sin(f + i); return `${i ? "L" : "M"}${px} ${py}`; }).join(" ");
  return <g opacity={k > 1 ? 1 - (k - 1) / 0.3 : 1}><path d={zig} stroke={ORIN_BLUE} strokeWidth={4} fill="none" /><Glow x={x} y={y} r={40} color={ORIN_BLUE} o={0.7} /><circle cx={x} cy={y} r={7} fill="#e8f8ff" /></g>; };
export const LaserDot: React.FC<{ x0: number; y0: number; x: number; y: number; f: number; o?: number }> = ({ x0, y0, x, y, f, o = 1 }) => <g opacity={o}>
  <line x1={x0} y1={y0} x2={x} y2={y} stroke={ORIN_RED} strokeWidth={2} opacity={0.35} /><circle cx={x + Math.sin(f * 0.7) * 3} cy={y + Math.cos(f * 0.9) * 3} r={6} fill={ORIN_RED} /><Glow x={x} y={y} r={20} color={ORIN_RED} o={0.8} /></g>;
export const Boom: React.FC<{ x: number; y: number; t: number; s?: number }> = ({ x, y, t, s = 1 }) => t < 0 || t > 40 ? null : <g>
  <Glow x={x} y={y} r={(80 + t * 10) * s} color="#ffb04a" o={Math.max(0, 1 - t / 18)} />
  {t < 14 && <circle cx={x} cy={y} r={(30 + t * 8) * s} fill="#fff4c0" opacity={1 - t / 14} />}
  {Array.from({ length: 8 }, (_, i) => { const a = i / 8 * Math.PI * 2 + 0.3; return <circle key={i} cx={x + Math.cos(a) * t * 5 * s} cy={y + Math.sin(a) * t * 4 * s - t * 2} r={(18 + t * 1.6) * s} fill="#4a4a52" opacity={0.6 * (1 - t / 40)} />; })}
  <Sparks x={x} y={y} t={t * 0.6} n={20} seed={5} s={s * 1.4} /></g>;
