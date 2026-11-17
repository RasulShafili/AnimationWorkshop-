// Clickbait thumbnails 1280x720 (owner: thumbnail = the main thing, click-bait, answers the title, big face, bright).
// A: Leo's giant terrified face + a friendly white home robot whose shell cracks open to show the red-eyed skeleton,
//    phone "STAY HOME, LEO." — text "IT LOCKED US IN?!".  B: Grandpa firing from the orange truck at red-eyed robots in
//    the rain, a net flying at the camera — text "DAY 19".
import React from "react";
import { AbsoluteFill } from "remotion";
import { Glow } from "./engine/fx";
import { rnd } from "./engine/core";
import { Character, AIM } from "./chars/Rig2";
import { Robot, robotAim } from "./chars/Robot";
import { LEO, WALT, HUNTER } from "./chars/cast";
import { Pickup, BED_Y, Muzzle, NetShot, Sparks } from "./scenes/Gear";
import { ORIN_RED } from "./scenes/City";
import { useFonts } from "./ui";

const T: React.FC<{ children: React.ReactNode; size: number; style?: React.CSSProperties; rot?: number }> = ({ children, size, style, rot = 0 }) =>
  <div style={{ fontFamily: "Inter", fontWeight: 900, fontSize: size, lineHeight: 0.92, color: "#fff", letterSpacing: -2, transform: `rotate(${rot}deg)`,
    textShadow: "5px 5px 0 #000, -5px 5px 0 #000, 5px -5px 0 #000, -5px -5px 0 #000, 0 5px 0 #000, 0 -5px 0 #000, 5px 0 0 #000, -5px 0 0 #000, 0 14px 30px rgba(0,0,0,.7)", ...style }}>{children}</div>;
const Arrow: React.FC<{ x: number; y: number; rot: number; s?: number }> = ({ x, y, rot, s = 1 }) =>
  <g transform={`translate(${x} ${y}) rotate(${rot}) scale(${s})`}><path d="M0 -18 L120 -18 L120 -48 L190 0 L120 48 L120 18 L0 18 Z" fill="#ff2a2a" stroke="#fff" strokeWidth={8} strokeLinejoin="round" /></g>;
const Phone: React.FC<{ x: number; y: number; s?: number; r?: number }> = ({ x, y, s = 1, r = -8 }) => <g transform={`translate(${x} ${y}) rotate(${r}) scale(${s})`}>
  <rect x={-70} y={-130} width={140} height={260} rx={22} fill="#111" /><rect x={-60} y={-118} width={120} height={236} rx={14} fill="#2a0c0e" /><Glow x={0} y={0} r={160} color={ORIN_RED} o={0.45} />
  <circle cx={0} cy={-50} r={26} fill="none" stroke={ORIN_RED} strokeWidth={7} /><circle cx={0} cy={-50} r={6} fill={ORIN_RED} />
  <text x={0} y={14} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={24} fill="#fff">STAY HOME,</text>
  <text x={0} y={46} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={30} fill="#ffd34a">LEO.</text></g>;

export const Thumb: React.FC<{ v: string }> = ({ v }) => {
  useFonts();
  if (v === "A") return <AbsoluteFill style={{ background: "linear-gradient(180deg, #ffb46a 0%, #ffe4c0 55%, #f4f0ea 100%)" }}>
    <svg width={1280} height={720} style={{ position: "absolute" }}>
      {/* bright living room: window light, a lamp */}
      <rect x={760} y={60} width={420} height={330} fill="#bfe2ff" /><rect x={750} y={50} width={440} height={350} fill="none" stroke="#fff" strokeWidth={16} />
      <rect y={590} width={1280} height={130} fill="#c8a07a" />
      <Glow x={960} y={360} r={520} color={ORIN_RED} o={0.55} />
      {/* the home robot: shell half gone, red slit eye, claw reaching */}
      <g transform="translate(1000 1560)"><Robot look={{ shell: 1, drop: [1, 2, 12, 13], mode: "hostile", dmg: 0.7, tag: "ORIN", gun: true }} pose={{ facing: -1, aR: [70, 30], aL: [90, 10], lean: 10, look: [-0.8, 0.1] }} x={0} y={0} s={3.2} f={10} seed={4} rim={{ dx: -8, dy: -6, color: "#ff6a4a" }} /></g>
      {/* Leo: giant terrified face */}
      <Glow x={290} y={430} r={360} color="#ffffff" o={0.45} />
      <Character look={LEO} pose={{ facing: 1, mouth: "shout", eyes: 1.6, brow: 1, look: [0.95, -0.3], aR: [62, 96], hold: null }} x={330} y={1440} s={2.9} f={7} seed={1} rim={{ dx: 8, dy: -6, color: "#ffffff" }} />
      {[[160, 250, 1.2], [450, 230, 0.9], [470, 320, 0.7]].map(([x, y, k], i) => <path key={i} d={`M${x} ${y} q${-14 * k} ${30 * k} 0 ${44 * k} q${14 * k} -14 0 ${-44 * k} Z`} fill="#8ad0ff" stroke="#fff" strokeWidth={3} />)}
      <Phone x={600} y={540} s={1.15} r={-10} />
      <Arrow x={600} y={330} rot={10} s={0.95} />
      <circle cx={900} cy={410} r={120} fill="none" stroke="#ff1a1a" strokeWidth={11} />
    </svg>
    <T size={118} style={{ position: "absolute", left: 30, top: 22 }} rot={-3}>IT LOCKED<br /><span style={{ color: "#ff3a2a" }}>US IN?!</span></T>
  </AbsoluteFill>;
  // B: action
  return <AbsoluteFill style={{ background: "linear-gradient(180deg, #1a2a4a 0%, #3a4a6a 60%, #2a3040 100%)" }}>
    <svg width={1280} height={720} style={{ position: "absolute" }}>
      {Array.from({ length: 90 }, (_, i) => <line key={i} x1={rnd(i, 1) * 1280} y1={rnd(i, 2) * 720} x2={rnd(i, 1) * 1280 - 10} y2={rnd(i, 2) * 720 + 40} stroke="#aac4ff" strokeWidth={3} opacity={0.4} />)}
      <rect y={600} width={1280} height={120} fill="#1a1e26" />
      {[0, 1, 2].map(i => { const x = 990 + i * 115, y = 640 - i * 14, sc = 0.9 - i * 0.12, a = robotAim(x, y, sc * 1.12, -1, 380, 330); return <g key={i}><Robot look={{ ...HUNTER, dark: 0.35 }} pose={{ facing: -1, aR: a.aR }} x={x} y={y} s={sc} f={i * 5} seed={20 + i} rim={{ dx: -4, dy: -3, color: "#ff6a4a" }} /></g>; })}
      <Sparks x={990} y={420} t={4} n={20} s={1.3} />
      <g transform="translate(250 760) scale(-1.15 1.15)"><Character look={WALT} pose={{ facing: -1, ...AIM, mouth: "shout", eyes: 1.1 }} x={-108} y={BED_Y} s={1} f={3} seed={2} rim={{ dx: 6, dy: -5, color: "#ffd38a" }} /><Pickup mirrored lights /></g>
      <Muzzle x={250 + 1.15 * (108 + 210)} y={760 + 1.15 * (BED_Y - 296)} k={1} s={1.3} />
      {(() => { const a = robotAim(990, 640, 0.9 * 1.12, -1, 380, 330); return <NetShot x0={a.tip[0]} y0={a.tip[1]} x1={380} y1={330} k={0.45} s={1.0} />; })()}
      
    </svg>
    <T size={150} style={{ position: "absolute", left: 40, top: 520 }} rot={-3}>DAY <span style={{ color: "#ff3a2a" }}>19</span></T>
  </AbsoluteFill>;
};
