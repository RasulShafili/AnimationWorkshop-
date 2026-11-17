// Clickbait thumbnails 1280x720 (owner: "thumbnail is the main thing, make it click-bait"). Rules kept: the image
// ANSWERS the title (where/when you woke up), one giant terrified face, one huge danger, 2–3 word text with ?!,
// warm-vs-cold contrast, a red arrow / circle, bright saturated (no dark purple that dies in dark mode).
import React from "react";
import { AbsoluteFill } from "remotion";
import { Glow } from "./engine/fx";
import { rnd } from "./engine/core";
import { Character } from "./chars/Rig2";
import { ELI, NIA, VOSS } from "./chars/cast";
import { Mammoth, CaveLion } from "./scenes/Animals";
import { PaintedCave } from "./scenes/Ice";
import { useFonts } from "./ui";

const T: React.FC<{ children: React.ReactNode; size: number; color?: string; style?: React.CSSProperties; rot?: number }> = ({ children, size, color = "#fff", style, rot = 0 }) =>
  <div style={{ fontFamily: "Inter", fontWeight: 900, fontSize: size, lineHeight: 0.92, color, letterSpacing: -2, transform: `rotate(${rot}deg)`,
    textShadow: "5px 5px 0 #000, -5px 5px 0 #000, 5px -5px 0 #000, -5px -5px 0 #000, 0 5px 0 #000, 0 -5px 0 #000, 5px 0 0 #000, -5px 0 0 #000, 0 14px 30px rgba(0,0,0,.7)", ...style }}>{children}</div>;
const Arrow: React.FC<{ x: number; y: number; rot: number; s?: number }> = ({ x, y, rot, s = 1 }) =>
  <g transform={`translate(${x} ${y}) rotate(${rot}) scale(${s})`}><path d="M0 -18 L120 -18 L120 -48 L190 0 L120 48 L120 18 L0 18 Z" fill="#ff2a2a" stroke="#fff" strokeWidth={8} strokeLinejoin="round" /></g>;
const Snowfall: React.FC = () => <g>{Array.from({ length: 90 }, (_, i) => <circle key={i} cx={rnd(i, 1) * 1280} cy={rnd(i, 2) * 720} r={2 + rnd(i, 3) * 5} fill="#fff" opacity={0.5 + 0.5 * rnd(i, 4)} />)}</g>;
// a phone in Eli's hand showing the impossible date
const PhoneDate: React.FC<{ x: number; y: number; s?: number; r?: number }> = ({ x, y, s = 1, r = -8 }) => <g transform={`translate(${x} ${y}) rotate(${r}) scale(${s})`}>
  <rect x={-70} y={-130} width={140} height={260} rx={22} fill="#111" /><rect x={-60} y={-118} width={120} height={236} rx={14} fill="#0e1a30" />
  <Glow x={0} y={0} r={170} color="#7ab8ff" o={0.5} />
  <text x={0} y={-62} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={15} fill="#ff6a5a">NO SERVICE</text>
  <text x={0} y={-6} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={30} fill="#fff">28,000</text>
  <text x={0} y={30} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={30} fill="#ffd34a">B.C.</text>
  <text x={0} y={82} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={14} fill="#8ab0d8">🔋 1%</text>
</g>;

export const Thumb: React.FC<{ v: string }> = ({ v }) => {
  useFonts();
  if (v === "A") return <AbsoluteFill style={{ background: "linear-gradient(180deg, #2a6ad8 0%, #7ab8f4 45%, #ffd0a0 78%, #fff4e6 100%)" }}>
    <svg width={1280} height={720} style={{ position: "absolute" }}>
      <path d="M-20 470 L110 330 L250 420 L400 280 L560 400 L720 300 L880 420 L1040 290 L1180 380 L1300 330 L1300 720 L-20 720 Z" fill="#a8c4e4" />
      <path d="M380 290 L400 280 L430 310 L415 305 Z M1030 300 L1040 290 L1070 320 Z" fill="#fff" />
      <Glow x={930} y={330} r={560} color="#ff9a3a" o={0.75} />
      <rect y={600} width={1280} height={120} fill="#f4f8fc" />
      {/* the mammoth charging LEFT toward Eli, trunk up, angry, rim-lit */}
      <g transform="translate(1210 760) scale(-1.18 1.18)"><Mammoth trumpet={1} ph={1.1} eye={1.3} angry={1} rim="#ffd8a0" /></g>
      {Array.from({ length: 26 }, (_, i) => <circle key={i} cx={760 + rnd(i, 7) * 520} cy={610 + rnd(i, 8) * 90} r={8 + rnd(i, 9) * 26} fill="#fff" opacity={0.85} />)}
      <Snowfall />
      {/* Eli: giant screaming face, sweat drops, white outline glow */}
      <Glow x={250} y={460} r={360} color="#ffffff" o={0.45} />
      <Character look={ELI} pose={{ facing: 1, mouth: "shout", eyes: 1.6, brow: 1, look: [0.95, -0.55], aR: [62, 96], hold: null }} x={300} y={1420} s={2.9} f={7} seed={1} rim={{ dx: 8, dy: -6, color: "#ffffff" }} />
      {[[150, 260, 1.2], [420, 250, 0.9], [440, 330, 0.7]].map(([x, y, k], i) => <path key={i} d={`M${x} ${y} q${-14 * k} ${30 * k} 0 ${44 * k} q${14 * k} -14 0 ${-44 * k} Z`} fill="#8ad0ff" stroke="#fff" strokeWidth={3} />)}
      <PhoneDate x={590} y={520} s={1.25} r={-12} />
      <circle cx={600} cy={512} r={118} fill="none" stroke="#ff2a2a" strokeWidth={10} />
    </svg>
    <T size={122} style={{ position: "absolute", left: 30, top: 22 }} rot={-3}>IT'S <span style={{ color: "#ffd34a" }}>28,000</span><br /><span style={{ color: "#ffd34a" }}>BC</span><span style={{ color: "#ff3a2a" }}>?!</span></T>
  </AbsoluteFill>;
  if (v === "B") return <AbsoluteFill style={{ background: "radial-gradient(ellipse at 62% 42%, #ffe0a8 0%, #f0b468 38%, #c8783a 75%, #8a4a22 100%)" }}>
    <svg width={1280} height={720} style={{ position: "absolute" }}>
      {/* rock texture: soft cracks and blotches */}
      {Array.from({ length: 14 }, (_, i) => <ellipse key={i} cx={rnd(i, 11) * 1280} cy={rnd(i, 12) * 720} rx={60 + rnd(i, 13) * 160} ry={30 + rnd(i, 14) * 80} fill="#a85e2a" opacity={0.12} />)}
      {[[520, 0, 600, 180, 560, 330], [1180, 60, 1120, 260, 1200, 420], [700, 720, 760, 560, 900, 520]].map((q, i) => <path key={i} d={`M${q[0]} ${q[1]} Q${q[2]} ${q[3]} ${q[4]} ${q[5]}`} stroke="#8a4a22" strokeWidth={4} fill="none" opacity={0.35} />)}
      {/* ancient paintings around: red horses, black mammoth */}
      <g transform="translate(560 120) scale(0.9)" opacity={0.75}><path d="M0 40 Q30 0 90 10 Q140 0 160 30 L175 20 L170 45 Q160 70 140 60 L135 100 M20 50 L15 100 M60 55 L58 100 M110 55 L112 100" stroke="#b02a1a" strokeWidth={10} fill="none" strokeLinecap="round" /></g>
      <g transform="translate(1060 560) scale(0.8)" opacity={0.7}><path d="M0 60 Q20 0 90 0 Q150 0 170 50 Q190 90 170 120 M40 70 L35 130 M140 70 L145 130 M170 50 Q200 80 190 130" stroke="#2a1408" strokeWidth={11} fill="none" strokeLinecap="round" /></g>
      {[[1210, 130], [1150, 180], [600, 420]].map(([x, y], i) => <g key={i} transform={`translate(${x} ${y})`} opacity={0.55}><path d="M-14 -20 Q0 -30 10 -14 L14 20 Q0 26 -12 18 Z" fill="#b02a1a" /></g>)}
      {/* THE figure: hooded person holding a glowing phone, painted in charcoal */}
      <Glow x={900} y={330} r={330} color="#fff2c0" o={0.8} />
      <g transform="translate(870 330) scale(1.85)" stroke="#1a0e08" strokeWidth={9} fill="none" strokeLinecap="round" strokeLinejoin="round">
        <circle cx={0} cy={-110} r={34} /><path d="M-42 -118 Q0 -178 42 -118" /><path d="M0 -76 L0 30 M0 30 L-34 110 M0 30 L34 110 M0 -50 L-38 0 M0 -50 L44 -24" />
        <rect x={42} y={-58} width={34} height={54} rx={6} fill="#7ad0ff" strokeWidth={7} />
      </g>
      <Glow x={980} y={250} r={120} color="#7ad0ff" o={0.95} />
      <text x={950} y={560} fontFamily="Permanent Marker" fontSize={70} fill="#1a0e08" letterSpacing={10}>E L I ☺</text>
      <circle cx={985} cy={258} r={90} fill="none" stroke="#ff1a1a" strokeWidth={11} />
      {/* scientist: giant shocked face, flashlight beam on the wall */}
      <path d="M330 470 L760 200 L800 330 Z" fill="#fffbe0" opacity={0.35} />
      <Character look={{ ...VOSS, hatColor: "#ffc81a" }} pose={{ facing: 1, mouth: "shout", eyes: 1.6, brow: 1, look: [0.95, -0.4], hold: "torch", beam: 0, aR: [70, 20] }} x={250} y={1400} s={2.75} f={6} seed={31} rim={{ dx: 8, dy: -6, color: "#ffffff" }} />
      {[[110, 330, 1.1], [395, 300, 0.9]].map(([x, y, k], i) => <path key={i} d={`M${x} ${y} q${-14 * k} ${30 * k} 0 ${44 * k} q${14 * k} -14 0 ${-44 * k} Z`} fill="#8ad0ff" stroke="#fff" strokeWidth={3} />)}
      <Arrow x={640} y={470} rot={-32} s={1.15} />
    </svg>
    <T size={112} style={{ position: "absolute", left: 28, top: 18 }} rot={-3}><span style={{ color: "#ffd34a" }}>30,000</span><br />YEARS OLD<span style={{ color: "#ff3a2a" }}>?!</span></T>
  </AbsoluteFill>;
  // C: the cave lion roaring right into Eli's face
  return <AbsoluteFill style={{ background: "linear-gradient(180deg, #ff9a4a 0%, #ffcf8a 55%, #f4f8fc 100%)" }}>
    <svg width={1280} height={720} style={{ position: "absolute" }}>
      <path d="M-20 520 L160 390 L300 480 L480 340 L640 450 L800 360 L980 470 L1140 350 L1300 430 L1300 720 L-20 720 Z" fill="#c8a0a0" opacity={0.6} />
      <rect y={580} width={1280} height={140} fill="#f4f8fc" />
      <g transform="translate(330 700) scale(0.62)" opacity={0.85}><Mammoth ph={0.3} trunk={0.6} /></g>
      <g transform="translate(560 760) scale(1.55)"><CaveLion roar={1} ph={0.4} /></g>
      <Snowfall />
      <Character look={ELI} pose={{ facing: -1, mouth: "shout", eyes: 1.45, brow: 0.95, look: [0.9, -0.2] }} x={1080} y={1330} s={2.6} f={5} seed={1} rim={{ dx: -7, dy: -5, color: "#ffb060" }} />
    </svg>
    <T size={118} style={{ position: "absolute", left: 34, top: 26 }} rot={-3}>DAY <span style={{ color: "#ff2a2a" }}>1</span><br />IN 28,000 BC</T>
  </AbsoluteFill>;
};
