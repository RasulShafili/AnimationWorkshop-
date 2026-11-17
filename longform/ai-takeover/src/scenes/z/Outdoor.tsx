// Outdoor locations: suburban street (dawn), I-75 traffic jam, store roof over the street, parking lot at night with
// the FRESHWAY box truck, truck cab (front view), crossroads at dawn, road montage, army checkpoint, tent city.
import React from "react";
import { rnd, sat, ease, lerp } from "../../engine/core";
import { Glow, Shaft } from "../../engine/fx";
import { Noise, AO, Bricks } from "../../engine/tex";
import { Character, Pose } from "../../chars/Rig2";
import { EXTRAS, HOLT, ZOMBIES, zombiePose } from "../../chars/zcast";
import { Hatchback, Wheel } from "./Cars";
import { Crowd } from "./Store";

const CAR_C = ["#c3cad4", "#c8323a", "#2f5ab8", "#f2f2f4", "#2a2a30", "#3a8a5a", "#e8b83a", "#7a4a8a"];
const Sky: React.FC<{ kind: "dawn" | "day" | "dusk" | "night"; id: string }> = ({ kind, id }) => {
  const c = { dawn: ["#4a5a9a", "#f0a07a"], day: ["#6aa8e8", "#cfe6f4"], dusk: ["#2a2a5a", "#e87a4a"], night: ["#05070f", "#141c30"] }[kind];
  return <><defs><linearGradient id={id} x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={c[0]} /><stop offset="1" stopColor={c[1]} /></linearGradient></defs><rect x={-1200} y={-400} width={4400} height={1300} fill={`url(#${id})`} /></>;
};
const Smoke: React.FC<{ x: number; y: number; f: number; s?: number }> = ({ x, y, f, s = 1 }) => <g opacity={0.55}>{Array.from({ length: 9 }, (_, i) => <circle key={i} cx={x + Math.sin(i * 0.9 + f * 0.01) * 30 * s + i * 14 * s} cy={y - i * 60 * s - (f * 0.4) % 60} r={(30 + i * 12) * s} fill="#3a3a44" />)}</g>;
const House: React.FC<{ x: number; y: number; c: string; roof: string; door?: string; lit?: boolean }> = ({ x, y, c, roof, door = "#8a3a2a", lit }) => <g transform={`translate(${x} ${y})`}>
  <rect x={-220} y={-300} width={440} height={300} fill={c} /><path d="M-250 -300 L0 -460 L250 -300 Z" fill={roof} /><rect x={-40} y={-170} width={90} height={170} fill={door} /><circle cx={34} cy={-84} r={6} fill="#e8c86a" />
  {[-150, 110].map(wx => <g key={wx}><rect x={wx} y={-230} width={90} height={80} fill={lit ? "#ffd88a" : "#8ab0d0"} /><line x1={wx + 45} y1={-230} x2={wx + 45} y2={-150} stroke="#fff" strokeWidth={5} /><rect x={wx - 6} y={-154} width={102} height={10} fill="#f4f1e8" /></g>)}
  <rect x={-60} y={0} width={130} height={14} fill="#bab4a8" /><Noise x={-220} y={-300} w={440} h={300} freq={0.6} o={0.12} />
</g>;
const Tree: React.FC<{ x: number; y: number; s?: number; c?: string }> = ({ x, y, s = 1, c = "#3a7a4a" }) => <g transform={`translate(${x} ${y}) scale(${s})`}><rect x={-12} y={-160} width={24} height={160} fill="#5a3e2a" />{[[0, -230, 90], [-60, -180, 70], [60, -180, 70], [0, -300, 60]].map(([cx, cy, r], i) => <circle key={i} cx={cx} cy={cy} r={r} fill={i % 2 ? c : "#2e6a3e"} />)}</g>;

// ---------- suburban street at dawn (the Cole house in the middle) ----------
export const Street: React.FC<{ f: number; children?: React.ReactNode; smoke?: boolean; kind?: "dawn" | "day" }> = ({ f, children, smoke = true, kind = "dawn" }) => <g>
  <Sky kind={kind} id="stsky" />
  {smoke && <><Smoke x={300} y={560} f={f} s={1.4} /><Smoke x={1700} y={540} f={f + 50} s={1.1} /></>}
  {Array.from({ length: 14 }, (_, i) => <rect key={i} x={-800 + i * 260} y={420 + rnd(i, 4) * 100} width={180} height={300} fill="#5a6280" opacity={0.6} />)}
  <rect x={-1000} y={600} width={4000} height={120} fill="#6a9a5a" />
  <Tree x={-300} y={640} s={1.1} /><House x={200} y={680} c="#d8c8a8" roof="#6a4a4a" /><House x={960} y={680} c="#a8c0d8" roof="#3a4a6a" door="#c8402e" /><House x={1720} y={680} c="#e8d8c0" roof="#7a5a3a" /><Tree x={580} y={650} /><Tree x={1360} y={650} s={0.9} /><Tree x={2200} y={640} />
  {/* mailboxes, hydrant, sidewalk, road */}
  <rect x={-1000} y={700} width={4000} height={60} fill="#bab4a8" />{Array.from({ length: 30 }, (_, i) => <line key={i} x1={-1000 + i * 140} y1={700} x2={-1000 + i * 140} y2={760} stroke="#8a847a" strokeWidth={3} />)}
  <rect x={-1000} y={760} width={4000} height={500} fill="#4a4c54" />{Array.from({ length: 24 }, (_, i) => <rect key={i} x={-1000 + i * 180} y={900} width={100} height={12} fill="#e8d86a" />)}
  <g transform="translate(1250 700)"><rect x={-14} y={-60} width={28} height={60} rx={10} fill="#d8322a" /><rect x={-22} y={-40} width={44} height={10} rx={4} fill="#d8322a" /></g>
  <g transform="translate(-20 1000)"><Hatchback color="#c8323a" /></g>
  {children}
</g>;

// ---------- I-75 jam: three lanes of stopped cars (side views), overhead sign, honks ----------
export const Highway: React.FC<{ f: number; children?: React.ReactNode; man?: boolean; smoke?: boolean }> = ({ f, children, man = true, smoke = true }) => <g>
  <Sky kind="day" id="hwsky" />{smoke && <><Smoke x={1500} y={480} f={f} s={1.6} /><Smoke x={200} y={470} f={f + 80} s={1.0} /></>}
  {Array.from({ length: 18 }, (_, i) => <rect key={i} x={-800 + i * 220} y={250 + rnd(i, 7) * 150} width={160} height={400} fill="#7a88a0" />)}
  <rect x={-1000} y={600} width={4000} height={700} fill="#5a5c64" /><rect x={-1000} y={596} width={4000} height={14} fill="#c8c4b8" />
  {[700, 840].map(y => <g key={y}>{Array.from({ length: 30 }, (_, i) => <rect key={i} x={-1000 + i * 160} y={y} width={80} height={8} fill="#f4f1e0" />)}</g>)}
  {/* overhead sign */}
  <g transform="translate(960 0)"><rect x={-700} y={170} width={20} height={430} fill="#6a6e78" /><rect x={680} y={170} width={20} height={430} fill="#6a6e78" /><rect x={-700} y={170} width={1400} height={16} fill="#6a6e78" />
    <rect x={-300} y={190} width={600} height={140} rx={10} fill="#1e6a3e" stroke="#f4f4f4" strokeWidth={5} /><path d="M-250 222 l60 0 l0 76 l-60 0 l0 -40 l30 -36 Z" fill="#fff" opacity={0} />
    <rect x={-260} y={214} width={90} height={90} rx={8} fill="#1a3a8a" stroke="#fff" strokeWidth={4} /><text x={-215} y={276} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={40} fill="#fff">75</text>
    <text x={-140} y={260} fontFamily="Inter" fontWeight={900} fontSize={46} fill="#fff">NORTH</text><text x={-140} y={306} fontFamily="Inter" fontWeight={700} fontSize={30} fill="#fff">Chattanooga</text></g>
  {/* 3 lanes of cars, far to near */}
  {[[680, 0.42], [810, 0.55], [990, 0.7]].map(([y, s], lane) => <g key={lane}>{Array.from({ length: 9 }, (_, i) => { const x = -900 + i * 900 * s + (lane % 2) * 200 + Math.sin(f * 0.05 + i) * 0.5;
    return <g key={i} transform={`translate(${x} ${y}) scale(${s})`}><Hatchback color={CAR_C[(i * 3 + lane) % CAR_C.length]} />{(i + lane) % 3 === 0 && <rect x={560} y={-150} width={50} height={20} fill="#ff3a2a" opacity={0.6 + 0.4 * Math.sin(f * 0.3 + i)} />}</g>; })}</g>)}
  {/* honk marks */}
  {Array.from({ length: 6 }, (_, i) => { const t = (f + i * 13) % 40; return <g key={i} opacity={1 - t / 40} transform={`translate(${200 + i * 300} ${520 + (i % 2) * 120})`}>{[0, 1, 2].map(k => <path key={k} d={`M${20 + k * 14 + t} -20 q8 20 0 40`} stroke="#fff" strokeWidth={4} fill="none" />)}</g>; })}
  {man && <Character look={EXTRAS[4]} pose={{ facing: 1, aR: [150 + 10 * Math.sin(f * 0.3), 20], aL: [-140, 30], mouth: "shout" }} x={1320} y={810 - 230 * 0.55} s={0.55} f={f} seed={7} />}
  {children}
</g>;

// ---------- the store roof, side section: Kai up on the roof (left), the street far below (right) ----------
// roof top y=520 (stand Kai at y=520, s≈0.8), building wall x=720, street ground y=1010. The can flies from Kai's hand
// to the car roof. turn>0 makes the infected turn toward the car.
export const ROOF_Y = 520, WALL_X = 720;
export const RoofView: React.FC<{ f: number; children?: React.ReactNode; crowd?: number; turn?: number; canT?: number }> = ({ f, children, crowd = 16, turn = 0, canT = -1 }) => {
  const carX = 1380, carTop = 1010 - 300 * 0.5;
  return <g>
  <Sky kind="day" id="rfsky" /><Smoke x={1700} y={420} f={f} s={1.3} />
  {Array.from({ length: 14 }, (_, i) => <rect key={i} x={-600 + i * 260} y={300 + rnd(i, 3) * 160} width={210} height={700} fill="#9aa6ba" />)}
  <rect x={-800} y={760} width={3600} height={40} fill="#b8c4d4" opacity={0.6} />
  {/* street + far sidewalk */}
  <rect x={-800} y={900} width={3600} height={40} fill="#bab4a8" /><rect x={-800} y={940} width={3600} height={400} fill="#4a4c54" />
  {Array.from({ length: 20 }, (_, i) => <rect key={i} x={-800 + i * 200} y={1040} width={110} height={10} fill="#e8d86a" />)}
  <g transform={`translate(${carX - 195} 1010) scale(0.5)`}><Hatchback color="#2f5ab8" /></g>
  {Array.from({ length: crowd }, (_, i) => { const x0 = 860 + rnd(i, 2) * 1500, y = 975 + rnd(i, 3) * 70, on = turn > rnd(i, 6) * 0.7; const x = on ? x0 + (carX - x0) * 0.25 * turn : x0;
    return { y, el: <Character key={i} look={ZOMBIES[i % ZOMBIES.length]} pose={{ facing: (on ? (x < carX ? 1 : -1) : (rnd(i, 4) > 0.5 ? 1 : -1)) as 1 | -1, ...zombiePose(f, i), head: on ? -4 : 10 }} x={x} y={y} s={0.42} f={f} seed={i} /> }; })
    .sort((a, b) => a.y - b.y).map(o => o.el)}
  {/* the can: from the roof edge to the car roof */}
  {canT >= 0 && canT < 26 && (() => { const u = canT / 26, x = lerp(640, carX, u), y = lerp(ROOF_Y - 190, carTop, u) - Math.sin(u * Math.PI) * 220; return <g transform={`translate(${x} ${y}) rotate(${canT * 30})`}><rect x={-10} y={-13} width={20} height={26} rx={3} fill="#c8342c" /><rect x={-10} y={-5} width={20} height={8} fill="#f2ead8" /></g>; })()}
  {canT >= 26 && canT < 44 && <g transform={`translate(${carX} ${carTop})`}>{Array.from({ length: 8 }, (_, i) => <line key={i} x1={0} y1={0} x2={Math.cos(i * 0.8) * (20 + (canT - 26) * 4)} y2={Math.sin(i * 0.8) * (20 + (canT - 26) * 4)} stroke="#fff" strokeWidth={5} opacity={1 - (canT - 26) / 18} />)}</g>}
  {canT >= 26 && <g transform={`translate(${carX + 40} ${carTop + 4}) rotate(90)`}><rect x={-10} y={-13} width={20} height={26} rx={3} fill="#c8342c" /></g>}
  {/* the building (store) on the left: brick wall, boarded windows, FRESHWAY sign, roof with parapet + HVAC */}
  <rect x={-800} y={ROOF_Y} width={WALL_X + 800} height={900} fill="#8a5a46" />
  <clipPath id="roofwall"><rect x={-800} y={ROOF_Y} width={WALL_X + 800} height={900} /></clipPath><g clipPath="url(#roofwall)">{Array.from({ length: 30 }, (_, r) => Array.from({ length: 16 }, (_, k) => <rect key={`${r}-${k}`} x={-800 + k * 100 + (r % 2) * 50} y={ROOF_Y + 30 + r * 36} width={94} height={30} fill="#9a6a52" opacity={0.6} />))}</g>
  <rect x={WALL_X - 14} y={ROOF_Y} width={14} height={900} fill="#000" opacity={0.25} />
  {[[120, 640], [420, 640]].map(([x, y], i) => <g key={i}><rect x={x} y={y} width={200} height={160} fill="#141820" />{[0, 1, 2].map(k => <rect key={k} x={x - 14} y={y + 20 + k * 50} width={228} height={26} fill="#a8865a" transform={`rotate(${(k - 1) * 4} ${x + 100} ${y + 33 + k * 50})`} />)}</g>)}
  <rect x={60} y={850} width={560} height={90} rx={8} fill="#2f8a4e" /><text x={340} y={912} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={60} fill="#fff" letterSpacing={6}>FRESHWAY</text>
  <rect x={-800} y={ROOF_Y - 24} width={WALL_X + 820} height={30} fill="#7a5a4a" /><rect x={-800} y={ROOF_Y - 30} width={WALL_X + 830} height={10} fill="#c8ccd4" />
  <g transform={`translate(80 ${ROOF_Y - 24})`}><rect x={0} y={-130} width={230} height={130} fill="#9aa0aa" />{Array.from({ length: 6 }, (_, i) => <rect key={i} x={18 + i * 34} y={-110} width={20} height={80} fill="#5a606a" />)}<circle cx={115} cy={-150} r={34} fill="#7a808a" /></g>
  {children}
  </g>; };

// ---------- box truck (side view facing RIGHT; text never mirrored) ----------
export const BoxTruck: React.FC<{ wheelRot?: number; lights?: boolean; dirty?: number }> = ({ wheelRot = 0, lights = false, dirty = 0 }) => <g>
  <ellipse cx={460} cy={6} rx={520} ry={26} fill="#000" opacity={0.45} />
  <rect x={0} y={-460} width={640} height={380} rx={10} fill="#f4f2ec" /><rect x={0} y={-460} width={640} height={30} fill="#e0ddd4" /><rect x={0} y={-110} width={640} height={30} fill="#c8c4ba" />
  <rect x={30} y={-400} width={580} height={130} rx={8} fill="#2f8a4e" /><text x={320} y={-318} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={86} fill="#fff" letterSpacing={4}>FRESHWAY</text>
  <text x={320} y={-220} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={30} fill="#2f8a4e">FRESH FOOD · EVERY DAY</text>
  {/* cab */}
  <path d="M650 -80 L650 -330 Q650 -350 670 -350 L800 -350 Q830 -350 850 -320 L910 -210 Q920 -196 920 -170 L920 -80 Z" fill="#e8e6e0" />
  <path d="M676 -330 L800 -330 Q818 -330 830 -310 L880 -216 L676 -216 Z" fill="#2a3a4e" /><path d="M690 -320 L720 -320 L700 -230 L680 -230 Z" fill="#fff" opacity={0.2} />
  <rect x={740} y={-200} width={30} height={8} rx={3} fill="#9a9a9a" /><rect x={896} y={-180} width={26} height={30} rx={4} fill={lights ? "#fff6c8" : "#c8c4b0"} />{lights && <Glow x={940} y={-165} r={180} color="#fff2c0" o={0.6} />}
  <rect x={640} y={-100} width={290} height={24} fill="#2a2a30" /><rect x={-10} y={-90} width={60} height={20} fill="#2a2a30" />
  {[150, 470, 790].map(x => <g key={x}><path d={`M${x - 70} -76 A70 70 0 0 1 ${x + 70} -76 Z`} fill="#121318" /><Wheel cx={x} cy={-44} r={52} rot={wheelRot} /></g>)}
  {dirty > 0 && <rect x={0} y={-460} width={640} height={380} rx={10} fill="#6a5a3a" opacity={dirty * 0.25} />}
</g>;

// ---------- the parking lot at night, store facade behind (sign dark) ----------
export const Lot: React.FC<{ f: number; children?: React.ReactNode; zombies?: number; moon?: boolean }> = ({ f, children, zombies = 10, moon = false }) => <g>
  <Sky kind="night" id="ltsky" />{Array.from({ length: 60 }, (_, i) => <circle key={i} cx={-600 + rnd(i, 1) * 3200} cy={-100 + rnd(i, 2) * 400} r={1.5 + rnd(i, 3) * 1.5} fill="#fff" opacity={0.6} />)}
  {moon && <><circle cx={1700} cy={80} r={50} fill="#e8eef8" /><Glow x={1700} y={80} r={200} color="#c8d8ff" o={0.35} /></>}
  {/* store facade */}
  <rect x={-700} y={160} width={1700} height={500} fill="#2a2e38" /><rect x={-700} y={160} width={1700} height={90} fill="#1e222a" />
  <text x={150} y={230} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={72} fill="#2f5a3e" letterSpacing={6}>FRESHWAY</text>
  {Array.from({ length: 5 }, (_, i) => <rect key={i} x={-640 + i * 330} y={300} width={300} height={360} fill="#0e141e" />)}
  {Array.from({ length: 5 }, (_, i) => <g key={i}>{[0, 1, 2].map(k => <rect key={k} x={-640 + i * 330} y={330 + k * 110} width={300} height={22} fill="#7a5a3a" transform={`rotate(${(k - 1) * 3} ${-490 + i * 330} ${340 + k * 110})`} />)}</g>)}
  {/* lot */}
  <rect x={-900} y={660} width={3800} height={700} fill="#1c2028" />{Array.from({ length: 14 }, (_, i) => <line key={i} x1={-700 + i * 280} y1={700} x2={-900 + i * 320} y2={1000} stroke="#c8c4b0" strokeOpacity={0.2} strokeWidth={6} />)}
  <g><rect x={1100} y={140} width={14} height={530} fill="#2a2e38" /><rect x={1110} y={136} width={70} height={14} rx={4} fill="#3a3a3a" /></g>
  <Crowd f={f} x0={-600} x1={2400} y={700} n={zombies} s={0.42} seed={31} dark={0.35} />
  <rect x={-900} y={-300} width={3800} height={1600} fill="#1a2a5a" opacity={0.25} style={{ mixBlendMode: "multiply" }} />
  {children}
</g>;

// ---------- truck cab seen from the front through the windshield ----------
export const Cab: React.FC<{ f: number; children?: React.ReactNode; outside?: "night" | "dawn" | "day" | "snow"; shake?: number }> = ({ f, children, outside = "night", shake = 0 }) => {
  const sh = shake ? Math.sin(f * 1.3) * 3 : 0;
  return <g transform={`translate(0 ${sh})`}>
    <rect x={-600} y={-200} width={3200} height={1500} fill={{ night: "#0a0e18", dawn: "#d8946a", day: "#9ec8e8", snow: "#d8e2ea" }[outside]} />
    {/* interior back wall */}
    <rect x={160} y={140} width={1600} height={700} fill={outside === "night" ? "#1a1e28" : "#3a3e48"} /><rect x={300} y={200} width={1320} height={200} rx={20} fill={outside === "night" ? "#0a0e18" : "#6a8aa8"} opacity={0.8} />
    {children}
    {/* windshield frame (we look in from outside), wipers, dashboard */}
    <path d="M-600 -200 L2600 -200 L2600 1300 L-600 1300 Z M200 120 L1720 120 Q1780 120 1790 180 L1840 760 L80 760 L130 180 Q140 120 200 120 Z" fill="#d8dce2" fillRule="evenodd" />
    <path d="M-600 -200 L2600 -200 L2600 1300 L-600 1300 Z M200 120 L1720 120 Q1780 120 1790 180 L1840 760 L80 760 L130 180 Q140 120 200 120 Z" fill="#000" opacity={0.25} fillRule="evenodd" />
    <rect x={60} y={740} width={1800} height={360} fill="#2a2a30" /><rect x={60} y={740} width={1800} height={20} fill="#4a4a52" />
    <text x={960} y={980} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={70} fill="#2f8a4e" letterSpacing={6}>FRESHWAY</text>
    <path d="M500 760 L960 700" stroke="#1a1a1e" strokeWidth={10} /><path d="M1100 760 L1560 700" stroke="#1a1a1e" strokeWidth={10} />
    {[200, 1720].map(x => <g key={x}><rect x={x - 70} y={820} width={140} height={60} rx={14} fill="#f4f4e8" /><Glow x={x} y={850} r={90} color="#fff6c8" o={outside === "night" ? 0.5 : 0.1} /></g>)}
    <path d="M200 120 L620 120 L340 760 L80 760 Z" fill="#fff" opacity={0.06} />
  </g>;
};

// ---------- crossroads at dawn ----------
export const Crossroads: React.FC<{ f: number; children?: React.ReactNode }> = ({ f, children }) => <g>
  <Sky kind="dawn" id="crsky" /><circle cx={1500} cy={600} r={80} fill="#fff0c0" /><Glow x={1500} y={600} r={420} color="#ffb070" o={0.5} />
  <rect x={-900} y={620} width={3800} height={700} fill="#8aa06a" />{Array.from({ length: 40 }, (_, i) => <line key={i} x1={-900 + i * 100} y1={640} x2={-900 + i * 100 + 20} y2={1300} stroke="#6a8a4a" strokeWidth={4} opacity={0.35} />)}
  <rect x={-900} y={780} width={3800} height={160} fill="#5a5c62" /><rect x={-900} y={852} width={3800} height={8} fill="#e8d86a" />
  <path d="M900 620 L1020 620 L1300 1300 L620 1300 Z" fill="#5a5c62" />
  {Array.from({ length: 10 }, (_, i) => <g key={i}><rect x={-700 + i * 380} y={420} width={10} height={220} fill="#5a4030" /><rect x={-730 + i * 380} y={430} width={70} height={6} fill="#5a4030" /></g>)}
  <path d="M-700 434 Q-510 460 -320 434 Q-130 460 60 434 Q250 460 440 434 Q630 460 820 434 Q1010 460 1200 434 Q1390 460 1580 434 Q1770 460 1960 434 Q2150 460 2340 434" stroke="#2a2a2a" strokeWidth={2} fill="none" />
  <g transform="translate(1180 780)"><rect x={-5} y={-200} width={10} height={200} fill="#9aa0aa" /><path d="M-50 -250 L-20 -280 L20 -280 L50 -250 L50 -210 L20 -180 L-20 -180 L-50 -210 Z" fill="#c8282a" stroke="#fff" strokeWidth={4} /><text x={0} y={-222} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={26} fill="#fff">STOP</text></g>
  {children}
</g>;

// ---------- montage backgrounds (parallax by f) ----------
export const Landscape: React.FC<{ f: number; kind: "town" | "plains" | "mountains" | "gas"; children?: React.ReactNode; speed?: number }> = ({ f, kind, children, speed = 14 }) => {
  const sx = (d: number, w: number) => ((-f * speed * d) % w + w) % w - w;
  return <g>
    <Sky kind={kind === "plains" ? "dawn" : kind === "mountains" ? "day" : "dusk"} id={`ls${kind}`} />
    {kind === "mountains" && <g>{[0, 1].map(k => <path key={k} transform={`translate(${sx(0.1, 2400) + k * 2400} 0)`} d="M-200 700 L200 280 L380 420 L640 160 L900 460 L1100 300 L1400 520 L1700 220 L2000 500 L2400 300 L2600 700 Z" fill="#7a8aa8" />)}
      {[0, 1].map(k => <path key={k} transform={`translate(${sx(0.1, 2400) + k * 2400} 0)`} d="M200 280 L260 340 L300 320 L380 420 L320 380 Z M640 160 L700 230 L760 210 L800 300 L700 260 Z M1700 220 L1770 300 L1820 280 L1880 360 Z" fill="#f4f6fa" />)}</g>}
    {kind === "plains" && <g>{Array.from({ length: 3 }, (_, k) => <g key={k} transform={`translate(${sx(0.2, 2400) + k * 2400} 0)`}><rect x={300} y={560} width={30} height={100} fill="#6a4a2a" /><path d="M200 600 L430 600 L380 520 L250 520 Z" fill="#a8322a" /><circle cx={1400} cy={600} r={60} fill="#4a6a3a" /></g>)}</g>}
    {kind === "town" && <g>{Array.from({ length: 3 }, (_, k) => <g key={k} transform={`translate(${sx(0.4, 2400) + k * 2400} 0)`}>{Array.from({ length: 6 }, (_, i) => <g key={i}><rect x={i * 400} y={380} width={340} height={300} fill={["#a87a5a", "#8a9aa8", "#c8a87a", "#7a6a5a"][i % 4]} />{[0, 1, 2].map(w => <rect key={w} x={i * 400 + 30 + w * 100} y={430} width={70} height={90} fill="#1a1e28" />)}<rect x={i * 400} y={560} width={340} height={30} fill="#3a2a2a" /><rect x={i * 400 + 20} y={600} width={300} height={80} fill="#0e1218" opacity={0.8} /></g>)}</g>)}</g>}
    {kind === "gas" && <g transform={`translate(${sx(0.4, 3000) + 1400} 0)`}><rect x={0} y={360} width={700} height={40} fill="#d8322a" /><rect x={60} y={400} width={20} height={280} fill="#8a8a8a" /><rect x={620} y={400} width={20} height={280} fill="#8a8a8a" /><rect x={250} y={540} width={60} height={140} rx={6} fill="#e8e4da" /><rect x={400} y={540} width={60} height={140} rx={6} fill="#e8e4da" /><rect x={760} y={420} width={400} height={260} fill="#c8c0b0" /><text x={350} y={392} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={30} fill="#fff">GAS · OPEN 24H</text></g>}
    <rect x={-900} y={660} width={3800} height={700} fill={kind === "mountains" ? "#e8eef4" : kind === "plains" ? "#c8a86a" : "#6a7a5a"} />
    <rect x={-900} y={760} width={3800} height={180} fill="#4a4c52" />{Array.from({ length: 30 }, (_, i) => <rect key={i} x={sx(1, 4800) + i * 160} y={846} width={90} height={10} fill="#e8d86a" />)}
    {kind === "mountains" && Array.from({ length: 50 }, (_, i) => <circle key={i} cx={(rnd(i, 1) * 2200 - f * 3) % 2200} cy={(rnd(i, 2) * 1100 + f * 4) % 1100} r={3} fill="#fff" opacity={0.8} />)}
    {children}
  </g>;
};

// ---------- army checkpoint at dusk ----------
export const Checkpoint: React.FC<{ f: number; children?: React.ReactNode; flood?: number }> = ({ f, children, flood = 1 }) => <g>
  <Sky kind="dusk" id="cpsky" /><path d="M-900 640 L-400 420 L0 560 L500 300 L900 520 L1400 340 L1900 560 L2400 400 L2900 640 Z" fill="#3a3a5a" /><path d="M500 300 L560 350 L520 360 Z M1400 340 L1460 390 L1420 400 Z" fill="#e8eef4" />
  <rect x={-900} y={640} width={3800} height={700} fill="#4a4a3a" />
  {/* tents beyond the fence */}
  {Array.from({ length: 7 }, (_, i) => <path key={i} d={`M${-300 + i * 400} 640 L${-200 + i * 400} 540 L${-40 + i * 400} 540 L${60 + i * 400} 640 Z`} fill="#5a6a3a" />)}
  {/* floodlight towers */}
  {[-200, 2100].map((x, i) => <g key={i}><path d={`M${x - 40} 700 L${x} 160 L${x + 40} 700`} stroke="#3a3a3a" strokeWidth={10} fill="none" /><rect x={x - 70} y={130} width={140} height={50} rx={6} fill="#2a2a2a" />{[0, 1, 2].map(k => <circle key={k} cx={x - 40 + k * 40} cy={155} r={15} fill="#fff8d8" />)}
    <path d={`M${x - 70} 180 L${x + 70} 180 L${x + (i ? -500 : 500) + 300} 1100 L${x + (i ? -500 : 500) - 300} 1100 Z`} fill="#fff6d0" opacity={0.12 * flood} /><Glow x={x} y={155} r={260} color="#fff2c0" o={0.5 * flood} /></g>)}
  {/* chain-link fence with barbed wire, gate in the middle */}
  <g>{Array.from({ length: 14 }, (_, i) => <rect key={i} x={-800 + i * 280} y={360} width={12} height={360} fill="#7a7e88" />)}
    <rect x={-800} y={380} width={3600} height={340} fill="url(#chain)" opacity={0.6} />
    <defs><pattern id="chain" width={26} height={26} patternUnits="userSpaceOnUse"><path d="M0 0 L26 26 M26 0 L0 26" stroke="#9aa0aa" strokeWidth={2} /></pattern></defs>
    {Array.from({ length: 90 }, (_, i) => <path key={i} d={`M${-800 + i * 40} 360 l10 -10 l10 10 l10 -10`} stroke="#aab0ba" strokeWidth={2} fill="none" />)}</g>
  {/* sandbags + BITE CHECK sign */}
  {Array.from({ length: 14 }, (_, i) => <ellipse key={i} cx={1300 + (i % 7) * 70} cy={760 - Math.floor(i / 7) * 34} rx={40} ry={20} fill="#a89a6a" stroke="#7a6e4a" strokeWidth={3} />)}
  <g transform="translate(520 560) rotate(-2)"><rect x={-6} y={0} width={12} height={180} fill="#5a4030" /><rect x={-180} y={-150} width={360} height={170} fill="#f4efe0" stroke="#3a3a3a" strokeWidth={5} />
    <text x={0} y={-100} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={40} fill="#c8282a">BITE CHECK</text>
    <text x={0} y={-56} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={24} fill="#2a2a2a">SLEEVES UP · BOTH ARMS</text><text x={0} y={-20} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={24} fill="#2a2a2a">NECK · HANDS · ANKLES</text></g>
  <rect x={-900} y={780} width={3800} height={600} fill="#3a3a30" /><AO x={-900} y={780} w={3800} h={40} dir="down" o={0.4} />
  {children}
</g>;

// ---------- tent city + missing persons board ----------
export const TentCity: React.FC<{ f: number; children?: React.ReactNode; board?: boolean }> = ({ f, children, board = true }) => <g>
  <Sky kind="dusk" id="tcsky" /><path d="M-900 560 L-300 300 L200 480 L800 220 L1300 460 L1900 260 L2900 560 Z" fill="#4a4a6a" /><path d="M800 220 L870 280 L820 290 Z M1900 260 L1970 320 L1920 330 Z" fill="#eef2f6" />
  <rect x={-900} y={560} width={3800} height={800} fill="#6a6a52" />{Array.from({ length: 40 }, (_, i) => <ellipse key={i} cx={-900 + rnd(i, 1) * 3800} cy={600 + rnd(i, 2) * 500} rx={40} ry={8} fill="#f4f6f8" opacity={0.5} />)}
  {[[600, 0.5], [700, 0.7]].map(([y, s], r) => <g key={r}>{Array.from({ length: 8 }, (_, i) => { const x = -700 + i * 460 * s + r * 120; return <g key={i} transform={`translate(${x} ${y}) scale(${s})`}><path d="M-200 0 L-140 -170 L140 -170 L200 0 Z" fill={r ? "#5e6e3e" : "#55653a"} /><path d="M-40 0 L0 -150 L40 0 Z" fill="#2a3220" /><text x={0} y={-120} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={34} fill="#e8e4c8">{String(40 + r * 8 + i)}</text></g>; })}</g>)}
  {[[200, 820], [1500, 860]].map(([x, y], i) => <g key={i}><path d={`M${x - 40} ${y} L${x + 40} ${y}`} stroke="#3a2a1a" strokeWidth={10} />{[0, 1, 2].map(k => <path key={k} d={`M${x - 20 + k * 20} ${y} q${-10 + 20 * Math.sin(f * 0.3 + k)} -40 0 -${60 + 10 * Math.sin(f * 0.4 + k)}`} fill="#ffb84a" opacity={0.85} />)}<Glow x={x} y={y - 30} r={200} color="#ffa84a" o={0.4} /></g>)}
  {/* survivors */}
  {Array.from({ length: 9 }, (_, i) => <Character key={i} look={{ ...EXTRAS[i % EXTRAS.length], backpack: i % 2 ? "#4a5a4a" : undefined }} pose={{ facing: (i % 2 ? 1 : -1) as 1 | -1, aR: [10, 20] }} x={-200 + i * 300 + rnd(i, 5) * 80} y={760 + rnd(i, 6) * 40} s={0.5} f={f} seed={i + 40} />)}
  {board && <g transform="translate(960 760)"><rect x={-8} y={0} width={16} height={160} fill="#5a4030" /><rect x={-330} y={0} width={16} height={160} fill="#5a4030" transform="translate(330 0)" />
    <rect x={-330} y={-330} width={660} height={340} fill="#8a6a44" /><rect x={-314} y={-314} width={628} height={308} fill="#c8a878" />
    <text x={0} y={-276} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={32} fill="#3a2a1a">MISSING · LOOKING FOR</text>
    {Array.from({ length: 14 }, (_, i) => <g key={i} transform={`translate(${-290 + (i % 7) * 84} ${-240 + Math.floor(i / 7) * 120}) rotate(${(rnd(i, 9) - 0.5) * 10})`}><rect x={0} y={0} width={70} height={100} fill="#f4f1e8" /><rect x={8} y={8} width={54} height={50} fill={["#8a9ab0", "#a89a8a", "#9ab09a"][i % 3]} /><circle cx={35} cy={30} r={14} fill="#2a2532" />{[0, 1].map(k => <rect key={k} x={10} y={68 + k * 12} width={50} height={5} fill="#8a8a8a" />)}</g>)}</g>}
  {children}
</g>;
