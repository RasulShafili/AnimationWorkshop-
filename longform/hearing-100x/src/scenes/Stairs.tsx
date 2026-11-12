// Stairwell at night: concrete, a flickering bulb, a green EXIT sign; the hero runs down with his phone.
import React from "react";
import { Layer, W, H, rnd, lerp } from "../engine/core";
import { Glow, Shaft } from "../engine/fx";
import { Noise, AO } from "../engine/tex";
import { Character, runPose } from "../chars/Rig";
import { HERO_PJ } from "../chars/cast";
export const STAIR = (u: number) => [lerp(260, 1660, u), lerp(330, 820, u)];   // the flight the hero runs down
export const Stairs: React.FC<{ f: number; u: number }> = ({ f, u }) => {
  const flick = (f % 47 < 3 || f % 71 < 2) ? 0.35 : 1;
  const p = STAIR(u), ph = f * 0.55;
  return <>
    <Layer depth={0.9}>
      <defs><linearGradient id="cw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#262a2c" /><stop offset="1" stopColor="#141617" /></linearGradient></defs>
      <rect x={-600} y={-300} width={W + 1200} height={H + 600} fill="url(#cw)" />
      <Noise x={-600} y={-300} w={W + 1200} h={H + 600} freq={0.35} o={0.45} seed={7} />
      {/* two-tone painted wall: green lower half, chipped */}
      <path d={`M-600 ${STAIR(0)[1] - 260} L${W + 600} ${STAIR(1)[1] + 300 - 260} L${W + 600} ${H + 300} L-600 ${H + 300} Z`} fill="#24382e" opacity={0.85} />
      <path d={`M-600 ${STAIR(0)[1] - 262} L${W + 600} ${STAIR(1)[1] + 300 - 262}`} stroke="#4a6a5a" strokeWidth={4} />
      {Array.from({ length: 14 }, (_, i) => <ellipse key={i} cx={-500 + rnd(i, 1) * 2900} cy={rnd(i, 2) * 900} rx={8 + rnd(i, 3) * 26} ry={5 + rnd(i, 4) * 12} fill="#3a3e40" opacity={0.6} />)}
      {/* pipes along the wall */}
      <line x1={-600} y1={60} x2={W + 600} y2={60} stroke="#3a3430" strokeWidth={18} /><line x1={-600} y1={60} x2={W + 600} y2={60} stroke="#5a5048" strokeWidth={4} transform="translate(0 -5)" />
      <line x1={-600} y1={100} x2={W + 600} y2={100} stroke="#2a3238" strokeWidth={10} />
      {[200, 900, 1500].map(x => <rect key={x} x={x} y={44} width={14} height={34} fill="#22201c" />)}
      {/* floor number + door + extinguisher */}
      <text x={300} y={230} fontFamily="Inter" fontWeight={900} fontSize={140} fill="#e8d23a" opacity={0.55}>3</text>
      <rect x={1240} y={180} width={190} height={360} fill="#3a2a22" stroke="#1a1410" strokeWidth={10} /><rect x={1300} y={220} width={70} height={90} fill="#ffd89a" opacity={0.25} /><circle cx={1410} cy={380} r={8} fill="#c8b88a" />
      <rect x={1700} y={300} width={44} height={110} rx={14} fill="#c82a2a" /><rect x={1712} y={282} width={20} height={22} fill="#222" /><path d="M1732 290 Q1760 300 1752 340" stroke="#222" strokeWidth={6} fill="none" />
      {/* the flight above (back) */}
      <path d={`M-200 120 L700 -120 L700 -80 L-200 160 Z`} fill="#1a1c1e" />
      {/* EXIT sign */}
      <rect x={1500} y={150} width={170} height={64} rx={6} fill="#0a2a14" /><text x={1585} y={196} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={40} fill="#5aff8a">EXIT</text>
      <Glow x={1585} y={182} r={260} color="#3aff7a" o={0.35} />
      {/* bulb */}
      <line x1={760} y1={-300} x2={760} y2={40} stroke="#0a0a0a" strokeWidth={4} /><circle cx={760} cy={52} r={16} fill={`rgba(255,220,150,${flick})`} />
      <Glow x={760} y={60} r={620} color="#ffcf8a" o={0.45 * flick} />
    </Layer>
    <Layer depth={1}>
      {/* stairs: a zig-zag of steps along the run line, railing */}
      {Array.from({ length: 22 }, (_, i) => { const a = STAIR(i / 22), b = STAIR((i + 1) / 22); return <g key={i}><rect x={a[0]} y={a[1]} width={b[0] - a[0] + 2} height={H} fill={i % 2 ? "#3a3d40" : "#363a3c"} /><rect x={a[0]} y={a[1]} width={b[0] - a[0] + 2} height={7} fill="#6a6e70" /><rect x={a[0]} y={a[1] + 7} width={b[0] - a[0] + 2} height={10} fill="#000" opacity={0.25} /><rect x={a[0] + 4} y={a[1] + 1} width={b[0] - a[0] - 8} height={3} fill="#c8a83a" opacity={0.5} /></g>; })}
      <Noise x={200} y={300} w={1600} h={900} freq={0.6} o={0.35} seed={9} />
      <line x1={STAIR(0)[0]} y1={STAIR(0)[1] - 150} x2={STAIR(1)[0]} y2={STAIR(1)[1] - 150} stroke="#8a8e90" strokeWidth={8} />
      {Array.from({ length: 12 }, (_, i) => { const a = STAIR(i / 11); return <line key={i} x1={a[0]} y1={a[1] - 150} x2={a[0]} y2={a[1]} stroke="#6a6e70" strokeWidth={5} />; })}
      <Shaft pts={[[700, 40], [820, 40], [1500, 1100], [100, 1100]]} color="#ffd8a0" o={0.12 * flick} blur={30} from={[760, 40]} to={[760, 1100]} />
      <Character look={HERO_PJ} pose={{ ...runPose(ph, 1.1), mouth: "open", brow: 0.8, look: [1, 0.3], aR: [110, 70], hands: "fist" }} x={p[0]} y={p[1] + 10} rim={{ dx: -4, dy: -3, color: "#ffd8a0" }} />
      {/* phone in the raised hand */}
      <Glow x={p[0] + 70} y={p[1] - 330} r={60} color="#9ec8ff" o={0.6} />
    </Layer>
  </>;
};
