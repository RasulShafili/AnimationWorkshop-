// Thumbnails v2 (owner 2026-11-17: "thumbnails are very bad, as if no work went into them — click-bait, interesting,
// relevant"). One focal idea each, custom big art (not the small rig), warm-vs-cold contrast, 2–3 word text.
// A "AI LOCKED US IN?!": inside a warm room, a giant white home robot presses its face + claw to the window, two red
//   eyes; Leo's huge terrified face in front, phone "STAY HOME". B "PULL IT?!": Leo's hand on the red MAIN breaker,
//   Bolt beside him with one blue eye and one red (ORIN inside him), blue server hall behind.
import React from "react";
import { AbsoluteFill } from "remotion";
import { rnd } from "./engine/core";
import { Character } from "./chars/Rig2";
import { LEO } from "./chars/cast";
import { useFonts } from "./ui";

const T: React.FC<{ children: React.ReactNode; size: number; style?: React.CSSProperties; rot?: number }> = ({ children, size, style, rot = 0 }) =>
  <div style={{ fontFamily: "Inter", fontWeight: 900, fontSize: size, lineHeight: 0.9, color: "#fff", letterSpacing: -3, transform: `rotate(${rot}deg)`,
    textShadow: "6px 6px 0 #000, -6px 6px 0 #000, 6px -6px 0 #000, -6px -6px 0 #000, 0 6px 0 #000, 0 -6px 0 #000, 6px 0 0 #000, -6px 0 0 #000, 0 16px 34px rgba(0,0,0,.75)", ...style }}>{children}</div>;
type Stop = [number, string, number?];
const LG = (id: string, stops: Stop[], x2 = 0, y2 = 1) => <linearGradient id={id} x1={0} y1={0} x2={x2} y2={y2}>{stops.map(([o, c, a], i) => <stop key={i} offset={o} stopColor={c} stopOpacity={a ?? 1} />)}</linearGradient>;
const RG = (id: string, stops: Stop[], rr = 0.5, cx = 0.5, cy = 0.5) => <radialGradient id={id} cx={cx} cy={cy} r={rr}>{stops.map(([o, c, a], i) => <stop key={i} offset={o} stopColor={c} stopOpacity={a ?? 1} />)}</radialGradient>;

// a big, carefully shaded robot head (front view): white shell, dark visor, two eyes (colour per eye), ear discs
const BigHead: React.FC<{ x: number; y: number; s: number; eyeL: string; eyeR: string; angry?: boolean; crack?: boolean; id: string }> = ({ x, y, s, eyeL, eyeR, angry, crack, id }) =>
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <defs>{LG(`${id}sh`, [[0, "#ffffff"], [0.55, "#e6ebf1"], [1, "#a9b3c0"]], 1, 1)}{LG(`${id}vi`, [[0, "#1b2230"], [1, "#05070b"]])}</defs>
    <rect x={-55} y={150} width={110} height={70} rx={20} fill="#3a404c" /><rect x={-70} y={205} width={140} height={30} rx={14} fill="#2a2f38" />
    {[-1, 1].map(k => <g key={k}><circle cx={k * 205} cy={10} r={48} fill="#c9d0da" /><circle cx={k * 205} cy={10} r={30} fill="#2a2f38" /><circle cx={k * 205} cy={10} r={18} fill="none" stroke={k < 0 ? eyeL : eyeR} strokeWidth={6} /></g>)}
    <rect x={-200} y={-170} width={400} height={330} rx={150} fill={`url(#${id}sh)`} />
    <path d="M-150 -150 Q-60 -185 60 -168" stroke="#fff" strokeWidth={14} strokeLinecap="round" fill="none" opacity={0.9} />
    <path d="M-185 40 Q-190 120 -120 150" stroke="#8a95a4" strokeWidth={5} fill="none" opacity={0.5} />
    {crack && <path d="M120 -150 L95 -95 L130 -70 L100 -10" stroke="#3a404c" strokeWidth={6} fill="none" strokeLinejoin="bevel" />}
    <rect x={-165} y={-70} width={330} height={150} rx={70} fill={`url(#${id}vi)`} />
    <path d="M-140 -50 Q-60 -66 40 -60" stroke="#fff" strokeWidth={9} strokeLinecap="round" fill="none" opacity={0.18} />
    {([[-70, eyeL, -1], [70, eyeR, 1]] as [number, string, number][]).map(([ex, c, k]) => <g key={k}>
      <circle cx={ex} cy={5} r={62} fill={c} opacity={0.25} /><circle cx={ex} cy={5} r={40} fill={c} opacity={0.35} />
      {angry ? <path d={`M${ex - 36} ${-22 + (k < 0 ? -8 : 8)} L${ex + 36} ${-22 + (k < 0 ? 8 : -8)} L${ex + 32} 28 Q${ex} 42 ${ex - 32} 28 Z`} fill={c} />
        : <ellipse cx={ex} cy={5} rx={30} ry={34} fill={c} />}
      <circle cx={ex - 10} cy={-4} r={9} fill="#fff" opacity={0.9} /></g>)}
  </g>;

export const Thumb: React.FC<{ v: string }> = ({ v }) => {
  useFonts();
  if (v === "A") return <AbsoluteFill>
    <svg width={1280} height={720} style={{ position: "absolute" }}>
      <defs>{LG("wall", [[0, "#ff9a3a"], [0.6, "#e8692a"], [1, "#b8401e"]], 1, 0)}{LG("night", [[0, "#0a0f1e"], [1, "#1c2440"]])}
        {RG("redglow", [[0, "#ff2a1a", 0.75], [1, "#ff2a1a", 0]])}{RG("vig", [[0.55, "#000", 0], [1, "#000", 0.55]], 0.75)}</defs>
      <rect width={1280} height={720} fill="url(#wall)" />
      <rect x={560} y={40} width={700} height={640} fill="url(#night)" />
      {Array.from({ length: 6 }, (_, i) => <rect key={i} x={580 + i * 120} y={420 - rnd(i, 2) * 200} width={90} height={400} fill="#151c32" />)}
      <circle cx={940} cy={360} r={420} fill="url(#redglow)" />
      <BigHead x={930} y={330} s={1.18} eyeL="#ff2a1a" eyeR="#ff2a1a" angry id="ra" />
      <g transform="translate(690 330) rotate(-8)"><rect x={-40} y={-10} width={80} height={110} rx={22} fill="#3a404c" />{[-28, 0, 28].map((dx, i) => <path key={i} d={`M${dx} -5 L${dx * 1.3} -90 L${dx * 1.1} -130`} stroke="#4a5160" strokeWidth={22} strokeLinecap="round" fill="none" />)}
        <circle cx={0} cy={-5} r={30} fill="#2a2f38" /></g>
      {Array.from({ length: 60 }, (_, i) => <line key={i} x1={570 + rnd(i, 3) * 680} y1={50 + rnd(i, 4) * 600} x2={566 + rnd(i, 3) * 680} y2={80 + rnd(i, 4) * 600} stroke="#cfe0ff" strokeWidth={3} opacity={0.35} />)}
      <path d="M600 60 L760 60 L620 400 L590 400 Z" fill="#fff" opacity={0.06} />
      <rect x={548} y={28} width={724} height={664} fill="none" stroke="#f4efe6" strokeWidth={26} /><rect x={1196} y={28} width={22} height={664} fill="#f4efe6" />
      <path d="M560 680 L1280 680 L1280 720 L300 720 Z" fill="#ff2a1a" opacity={0.18} />
      <Character look={LEO} pose={{ facing: 1, mouth: "shout", eyes: 1.65, brow: 1, look: [1, -0.15], hold: null }} x={300} y={1520} s={3.1} f={7} seed={1} rim={{ dx: 9, dy: -6, color: "#ffe2c4" }} />
      {[[120, 300, 1.3], [470, 270, 1.0], [500, 360, 0.75]].map(([x, y, k], i) => <path key={i} d={`M${x} ${y} q${-15 * k} ${32 * k} 0 ${46 * k} q${15 * k} -14 0 ${-46 * k} Z`} fill="#8ad0ff" stroke="#fff" strokeWidth={3} />)}
      <g transform="translate(590 600) rotate(10) scale(0.82)"><rect x={-78} y={-140} width={156} height={280} rx={24} fill="#111" /><rect x={-66} y={-126} width={132} height={252} rx={16} fill="#3a0a0c" />
        <circle cx={0} cy={-60} r={30} fill="none" stroke="#ff3a2a" strokeWidth={8} /><circle cx={0} cy={-60} r={8} fill="#ff3a2a" />
        <text x={0} y={10} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={30} fill="#fff">STAY</text><text x={0} y={46} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={30} fill="#fff">HOME.</text>
        <text x={0} y={86} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={16} fill="#ff8a7a">DOORS LOCKED</text>
        <path d="M-120 150 Q-110 60 -70 70 L-50 150 Z" fill="#3f8a4e" /><ellipse cx={-62} cy={95} rx={34} ry={50} fill="#f4ccb0" stroke="#c8906a" strokeWidth={3} />{[0, 1, 2].map(i => <rect key={i} x={-36} y={58 + i * 26} width={46} height={20} rx={10} fill="#f4ccb0" stroke="#c8906a" strokeWidth={3} />)}<ellipse cx={-80} cy={30} rx={14} ry={30} fill="#f4ccb0" stroke="#c8906a" strokeWidth={3} transform="rotate(-20 -80 30)" /></g>
      <rect width={1280} height={720} fill="url(#vig)" />
    </svg>
    <T size={128} style={{ position: "absolute", left: 34, top: 24 }} rot={-3}>AI LOCKED<br /><span style={{ color: "#ff2a1a" }}>US IN?!</span></T>
  </AbsoluteFill>;
  return <AbsoluteFill>
    <svg width={1280} height={720} style={{ position: "absolute" }}>
      <defs>{LG("hall", [[0, "#06101e"], [1, "#0c2440"]])}{RG("blue", [[0, "#3ab8ff", 0.55], [1, "#3ab8ff", 0]], 0.5, 0.5, 0.45)}
        {RG("red2", [[0, "#ff2a1a", 0.7], [1, "#ff2a1a", 0]])}{LG("lever", [[0, "#ff5a3a"], [1, "#b81e10"]], 1, 0)}{RG("vig2", [[0.55, "#000", 0], [1, "#000", 0.6]], 0.75)}</defs>
      <rect width={1280} height={720} fill="url(#hall)" />
      {Array.from({ length: 9 }, (_, i) => { const z = Math.pow(1 - i / 9, 1.4), lx = 640 - 900 * z, rx = 640 + 900 * z, t = 330 - 380 * z, b = 330 + 420 * z;
        return <g key={i}><path d={`M${lx} ${t} L${lx + 90 * z} ${t + 20 * z} L${lx + 90 * z} ${b - 20 * z} L${lx} ${b} Z`} fill="#0f1a2c" /><path d={`M${rx} ${t} L${rx - 90 * z} ${t + 20 * z} L${rx - 90 * z} ${b - 20 * z} L${rx} ${b} Z`} fill="#0f1a2c" />
          {Array.from({ length: 6 }, (_, j) => <g key={j}><circle cx={lx + 30 * z} cy={t + 40 * z + j * 50 * z} r={4 * z + 1} fill="#3ab8ff" /><circle cx={rx - 30 * z} cy={t + 40 * z + j * 50 * z} r={4 * z + 1} fill="#3ab8ff" /></g>)}</g>; })}
      <circle cx={640} cy={300} r={520} fill="url(#blue)" />
      <circle cx={360} cy={400} r={360} fill="url(#red2)" opacity={0.6} />
      <BigHead x={350} y={380} s={1.05} eyeL="#3ab8ff" eyeR="#ff2a1a" crack id="bolt" />
      <g transform="translate(960 380)"><rect x={-150} y={-230} width={300} height={440} rx={26} fill="#2a2f38" stroke="#ffd34a" strokeWidth={14} strokeDasharray="44 26" />
        <rect x={-26} y={-150} width={52} height={250} rx={18} fill="#0e1118" />
        <g transform="rotate(-24 0 80)"><rect x={-22} y={-170} width={44} height={250} rx={18} fill="url(#lever)" /><rect x={-80} y={-210} width={160} height={66} rx={28} fill="#e8402e" stroke="#fff" strokeWidth={5} />
          <path d="M-90 -230 Q-20 -270 70 -232 L86 -168 Q0 -140 -86 -170 Z" fill="#f4ccb0" stroke="#c8906a" strokeWidth={4} />
          {[-50, -15, 20, 55].map((x, i) => <path key={i} d={`M${x} -236 Q${x + 6} -200 ${x + 2} -172`} stroke="#c8906a" strokeWidth={4} fill="none" />)}
          <path d="M70 -232 L300 -330 L340 -230 L86 -168 Z" fill="#3f8a4e" /></g>
        <text x={0} y={250} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={56} fill="#ffd34a" stroke="#000" strokeWidth={5} paintOrder="stroke">MAIN</text></g>
      <rect width={1280} height={720} fill="url(#vig2)" />
      <g transform="translate(700 210) rotate(28)"><path d="M0 -20 L130 -20 L130 -54 L210 0 L130 54 L130 20 L0 20 Z" fill="#ff2a2a" stroke="#fff" strokeWidth={9} strokeLinejoin="round" /></g>
    </svg>
    <T size={150} style={{ position: "absolute", left: 40, top: 22 }} rot={-3}>PULL <span style={{ color: "#ffd34a" }}>IT?!</span></T>
  </AbsoluteFill>;
};
