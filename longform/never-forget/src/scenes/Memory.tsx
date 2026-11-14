// The memory replay ("REWIND") look + the street three years ago with the silver hatchback.
import React from "react";
import { Layer, W, H, sat, rnd } from "../engine/core";
import { Glow, Shaft, Bokeh } from "../engine/fx";
import { Noise, Bricks, AO } from "../engine/tex";
import { Character, walkPose } from "../chars/Rig2";
import { LINA, EXTRAS } from "../chars/cast";
import { Hatchback, HatchRear, HATCH } from "./Cars";

const GOLD = "#ffc94a";
// gold "memory outline" marker with label, pops in with k
export const Mark: React.FC<{ x: number; y: number; w: number; h: number; k: number; label?: string; lx?: number; ly?: number }> = ({ x, y, w, h, k, label, lx = 0, ly = -60 }) => k <= 0 ? null : <g opacity={Math.min(1, k)}>
  <rect x={x - 8} y={y - 8} width={w + 16} height={h + 16} rx={10} fill="none" stroke={GOLD} strokeWidth={10} opacity={0.35} style={{ filter: "blur(6px)" }} />
  <rect x={x - 6} y={y - 6} width={w + 12} height={h + 12} rx={8} fill="none" stroke={GOLD} strokeWidth={4} strokeDasharray={`${(w + h) * 2.2 * Math.min(1, k)} 9999`} />
  {label && <g transform={`translate(${x + w / 2 + lx} ${y + ly})`}><rect x={-label.length * 11 - 18} y={-34} width={label.length * 22 + 36} height={50} rx={10} fill="rgba(20,14,4,.8)" stroke={GOLD} strokeWidth={2} />
    <text x={0} y={2} fontFamily="Inter" fontWeight={900} fontSize={30} fill={GOLD} textAnchor="middle">{label}</text></g>}
</g>;

// silver hatchback, side view. Drawn facing right in local space; dir=-1 mirrors it so it drives LEFT and we see
// its LEFT side (the dent is on the back left door). Origin = rear-bottom. Marks are drawn un-mirrored (readable text).
export const CAR_PTS = { dent: HATCH.dent, fresh: HATCH.fresh };      // local points (facing right, before scale)
export const carPt = (x: number, s: number, dir: number, p: number[]) => [x + p[0] * s * dir, 880 + p[1] * s];
export const Car: React.FC<{ x: number; y: number; s?: number; wheel?: number; dir?: 1 | -1 }> = ({ x, y, s = 1, wheel = 0, dir = 1 }) => <g transform={`translate(${x} ${y}) scale(${s * dir} ${s})`}>
  <defs><linearGradient id="carb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#e4e8ee" /><stop offset="0.5" stopColor="#b8c0cc" /><stop offset="1" stopColor="#7a8494" /></linearGradient></defs>
  <ellipse cx={350} cy={8} rx={380} ry={22} fill="#000" opacity={0.35} />
  <path d="M0 -40 L6 -150 Q14 -186 60 -196 L150 -200 Q200 -290 300 -296 L470 -296 Q540 -290 590 -210 L660 -190 Q700 -178 700 -120 L700 -40 Z" fill="url(#carb)" />
  <rect x={-6} y={-70} width={22} height={34} rx={6} fill="#5a6474" /><rect x={690} y={-70} width={22} height={34} rx={6} fill="#5a6474" />
  <path d="M40 -196 L150 -200 L160 -206 Q208 -280 296 -284 L300 -206 Z" fill="#2a3444" />
  <path d="M320 -206 L318 -284 L465 -284 Q520 -280 570 -210 Z" fill="#2a3444" />
  <path d="M330 -270 L420 -270 L380 -214 L340 -214 Z" fill="#fff" opacity={0.12} />
  {/* rear-view mirror + air freshener hanging from it */}
  <rect x={500} y={-282} width={34} height={10} rx={4} fill="#1a1e26" />
  <line x1={520} y1={-272} x2={520} y2={-252} stroke="#ddd" strokeWidth={2} />
  <path d="M520 -252 L506 -228 L512 -228 L502 -210 L538 -210 L528 -228 L534 -228 Z" fill="#3aa85a" />
  <path d="M585 -200 L612 -214 L620 -196 Z" fill="#2a3444" />
  <line x1={300} y1={-206} x2={300} y2={-48} stroke="#5a6474" strokeWidth={3} /><line x1={150} y1={-200} x2={150} y2={-60} stroke="#5a6474" strokeWidth={3} />
  <path d="M170 -140 Q200 -120 236 -138 Q250 -110 214 -96 Q188 -104 170 -140 Z" fill="#6a7484" opacity={0.75} />
  <path d="M182 -132 Q205 -122 226 -132" stroke="#f4f6fa" strokeWidth={3} fill="none" opacity={0.8} />
  <rect x={250} y={-160} width={34} height={8} rx={4} fill="#5a6474" /><rect x={420} y={-160} width={34} height={8} rx={4} fill="#5a6474" />
  <rect x={0} y={-150} width={16} height={46} rx={4} fill="#d8322c" /><rect x={686} y={-140} width={16} height={30} rx={4} fill="#fff6d0" />
  {[130, 560].map(cx => <g key={cx} transform={`rotate(${wheel * dir} ${cx} -36)`}><circle cx={cx} cy={-36} r={52} fill="#141418" /><circle cx={cx} cy={-36} r={28} fill="#9aa2ae" />{[0, 72, 144, 216, 288].map(a => <line key={a} x1={cx} y1={-36} x2={cx + 26 * Math.cos(a * Math.PI / 180)} y2={-36 + 26 * Math.sin(a * Math.PI / 180)} stroke="#5a626e" strokeWidth={6} />)}</g>)}
</g>;

// rear view of the same car (for the plate close-up), centred at cx, ground at gy
export const CarRear: React.FC<{ cx: number; gy: number; s?: number; k: number }> = ({ cx, gy, s = 1, k }) => <g transform={`translate(${cx} ${gy}) scale(${s})`}>
  <ellipse cx={0} cy={6} rx={330} ry={26} fill="#000" opacity={0.4} />
  <rect x={-300} y={-110} width={70} height={110} rx={18} fill="#141418" /><rect x={230} y={-110} width={70} height={110} rx={18} fill="#141418" />
  <path d="M-310 -60 L-300 -230 Q-290 -280 -220 -300 Q-120 -440 0 -440 Q120 -440 220 -300 Q290 -280 300 -230 L310 -60 Q0 -40 -310 -60 Z" fill="url(#carb2)" />
  <defs><linearGradient id="carb2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#e4e8ee" /><stop offset="1" stopColor="#7a8494" /></linearGradient></defs>
  <path d="M-200 -300 Q-110 -410 0 -410 Q110 -410 200 -300 Z" fill="#2a3444" /><path d="M-150 -320 Q-60 -390 40 -392 L-60 -320 Z" fill="#fff" opacity={0.1} />
  <rect x={-290} y={-250} width={90} height={56} rx={12} fill="#d8322c" /><rect x={200} y={-250} width={90} height={56} rx={12} fill="#d8322c" />
  <rect x={-280} y={-242} width={70} height={16} rx={6} fill="#ff8a7a" opacity={0.6} /><rect x={210} y={-242} width={70} height={16} rx={6} fill="#ff8a7a" opacity={0.6} />
  <rect x={-320} y={-110} width={640} height={50} rx={16} fill="#5a6474" />
  <rect x={-110} y={-200} width={220} height={74} rx={8} fill="#f4f1e6" stroke="#20242c" strokeWidth={5} />
  <text x={0} y={-146} fontFamily="Inter" fontWeight={900} fontSize={52} fill="#1a2a6a" textAnchor="middle" letterSpacing={3}>7KR·419</text>
  <Mark x={-110} y={-200} w={220} h={74} k={k} label="7KR-419" ly={-70} />
</g>;

export const PlateInsert: React.FC<{ f: number; k: number }> = ({ f, k }) => <svg width={W} height={H} style={{ position: "absolute" }}>
  <defs><linearGradient id="pisky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#b8a68a" /><stop offset="1" stopColor="#8a7e6a" /></linearGradient></defs>
  <rect width={W} height={H} fill="url(#pisky)" />
  {/* blurred shop fronts behind */}
  <g style={{ filter: "blur(10px)" }}>{[0, 1, 2, 3].map(i => <g key={i}><rect x={-100 + i * 560} y={60} width={520} height={560} fill={i % 2 ? "#a8856a" : "#b8957a"} /><rect x={-60 + i * 560} y={300} width={440} height={240} fill="#3a4250" /><rect x={-80 + i * 560} y={260} width={480} height={50} fill={["#e8b06a", "#6ac0a8", "#c87a6a", "#7a9ad8"][i]} /></g>)}</g>
  <rect x={0} y={620} width={W} height={120} fill="#c8c2b6" /><rect x={0} y={740} width={W} height={340} fill="#4a4e58" />
  <g transform={`translate(960 900) scale(${1.25 * (1 + f * 0.0012)})`}><HatchRear /><Mark x={-112} y={-212} w={224} h={58} k={k} label="7KR-419" ly={-60} /></g>
</svg>;

// sunny street, 3 years ago. tf = memory time (stops when the car freezes → the whole memory freezes).
// crowd=false hides the people (for close-ups, so no heads are cut by the frame).
export const StreetPast: React.FC<{ f: number; tf: number; carX: number; wheel: number; marks: number[]; active?: number; crowd?: boolean }> = ({ f, tf, carX, wheel, marks, active = -1, crowd = true }) => {
  const s = 1.15, dir = -1 as const, dent = carPt(carX, s, dir, CAR_PTS.dent), fr = carPt(carX, s, dir, CAR_PTS.fresh);
  const walkX = 1500 - tf * 1.6;
  return <>
  <Layer depth={0.3}>
    <rect x={-800} y={-400} width={3520} height={900} fill="#9ec6e8" />
    <Glow x={1500} y={80} r={500} color="#fff3c8" o={0.8} />
    {[[-200, 260], [300, 200], [900, 240], [1500, 180], [2100, 230]].map(([x, h], i) => <rect key={i} x={x} y={500 - h - 120} width={420} height={h + 200} fill="#b8c8d8" opacity={0.7} />)}
  </Layer>
  <Layer depth={0.75}>
    {[["BAKERY", "#e8b06a", -200], ["PHARMACY", "#6ac0a8", 380], ["BOOKS", "#c87a6a", 960], ["CAFE", "#7a9ad8", 1540]].map(([name, c, x]: any, i) => <g key={i}>
      <Bricks x={x} y={100} w={560} h={520} color={i % 2 ? "#b88a6a" : "#c89a7a"} bw={56} bh={22} o={0.35} />
      <rect x={x + 40} y={330} width={480} height={240} fill="#2a3a4a" /><rect x={x + 40} y={330} width={480} height={240} fill="#fff" opacity={0.12} />
      <path d={`M${x + 20} 300 L${x + 540} 300 L${x + 520} 350 L${x + 40} 350 Z`} fill={c} />
      {Array.from({ length: 8 }, (_, k) => <path key={k} d={`M${x + 40 + k * 60} 350 q30 22 60 0`} fill={c} />)}
      <text x={x + 280} y={250} fontFamily="Inter" fontWeight={900} fontSize={46} fill="#fff8e8" textAnchor="middle">{name}</text>
    </g>)}
    <AO x={-800} y={520} w={3520} h={100} dir="up" o={0.4} />
  </Layer>
  <Layer depth={1}>
    <rect x={-800} y={620} width={3520} height={120} fill="#c8c2b6" />
    {Array.from({ length: 30 }, (_, i) => <line key={i} x1={-800 + i * 130} y1={620} x2={-800 + i * 130} y2={740} stroke="#9a948a" strokeWidth={3} />)}
    <rect x={-800} y={740} width={3520} height={16} fill="#e8e2d6" />
    <rect x={-800} y={756} width={3520} height={500} fill="#4a4e58" />
    <Noise x={-800} y={756} w={3520} h={500} freq={0.9} o={0.25} />
    {Array.from({ length: 16 }, (_, i) => <rect key={i} x={-800 + i * 240} y={930} width={130} height={14} fill="#f0e6c0" />)}
    {crowd && <>
      <Character look={EXTRAS[1]} pose={{ ...walkPose((1500 - walkX) / 290 * Math.PI * 2), facing: -1 }} x={walkX} y={690} s={0.85} f={tf} seed={5} />
      <Character look={EXTRAS[4]} pose={{ facing: -1, look: [0.8, 0.3] }} x={180} y={700} s={0.9} f={tf} seed={6} />
      <Character look={{ ...LINA, scale: 0.86 }} pose={{ facing: -1, look: [0.9, 0.5], aR: [40, 90], mouth: "o", eyes: 1.1 }} x={900} y={700} s={1} f={tf} seed={1} />
      <g transform="translate(828 470)"><path d="M0 0 L14 44 L28 0 Z" fill="#d8a85a" /><circle cx={14} cy={-6} r={18} fill="#f4c0d0" /></g>
    </>}
    <g transform={`translate(${carX} 880) scale(${s * dir} ${s})`}><Hatchback wheelRot={wheel} /></g>
    <Mark x={dent[0] - 42 * s} y={dent[1] - 32 * s} w={84 * s} h={64 * s} k={marks[1]} label={active === 1 ? "DENT · BACK LEFT DOOR" : undefined} ly={-80} />
    <Mark x={fr[0] - 28 * s} y={fr[1] - 44 * s} w={56 * s} h={88 * s} k={marks[2]} label={active === 2 ? "PINE TREE" : undefined} ly={-60} />
  </Layer>
</>; };

// overlay on top of a memory: VHS tracking line, scanlines, gold edge glow, chromatic split (k = strength)
export const MemoryFX: React.FC<{ f: number; k: number }> = ({ f, k }) => k <= 0 ? null : <>
  <div style={{ position: "absolute", inset: 0, pointerEvents: "none", opacity: k, boxShadow: `inset 0 0 160px rgba(255,190,70,${0.55})`, mixBlendMode: "screen" }} />
  <svg width={W} height={H} style={{ position: "absolute", inset: 0, opacity: 0.18 * k, mixBlendMode: "multiply" }}><defs><pattern id="scl" width={4} height={4} patternUnits="userSpaceOnUse"><rect width={4} height={2} fill="#000" /></pattern></defs><rect width={W} height={H} fill="url(#scl)" /></svg>
  <div style={{ position: "absolute", left: 0, right: 0, top: ((f * 23) % (H + 200)) - 100, height: 26, background: "rgba(255,255,255,.10)", opacity: k, filter: "blur(3px)" }} />
  {Array.from({ length: 14 }, (_, i) => <div key={i} style={{ position: "absolute", left: rnd(i, f % 30) * W, top: rnd(i + 9, f % 30) * H, width: 2 + rnd(i, 4) * 4, height: 2 + rnd(i, 4) * 4, borderRadius: 4, background: GOLD, opacity: 0.5 * k }} />)}
</>;
export const MEMORY_FILTER = (k: number) => `saturate(${1 - 0.55 * k}) sepia(${0.35 * k}) contrast(${1 + 0.08 * k}) brightness(${1 + 0.05 * k})`;
