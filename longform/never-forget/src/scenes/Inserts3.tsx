// Chapter 3 inserts: a textbook whose pages flip and fly into gold memory frames, the exam paper filled in seconds,
// a shuffled deck spread on the cafeteria table and read in one glance, a speech bubble for the remembered quote.
import React from "react";
import { W, H, rnd, sat, ease, easeOut, lerp } from "../engine/core";
import { Glow } from "../engine/fx";
import { Noise } from "../engine/tex";
import { MemFrame } from "./Title";
import { Sleeve } from "./Inserts";

const GOLD = "#ffc94a";
const Mit: React.FC<{ x: number; y: number; r?: number; c?: string; sleeve?: string; ang?: number }> = ({ x, y, r = 60, c = "#2a2536", sleeve = "#1f6f78", ang = 200 }) => {
  const a = ang * Math.PI / 180;
  return <g><Sleeve x0={x + Math.cos(a) * 760} y0={y + Math.sin(a) * 760} x1={x + Math.cos(a) * r * 0.6} y1={y + Math.sin(a) * r * 0.6} w0={r * 3.2} w1={r * 1.9} c={sleeve} cuff="#134a52" dark="#0c3238" />
    <circle cx={x} cy={y} r={r} fill={c} /><circle cx={x - r * 0.3} cy={y - r * 0.35} r={r * 0.28} fill="#fff" opacity={0.15} /></g>;
};

export const BookInsert: React.FC<{ f: number }> = ({ f }) => {
  const flips = Math.floor(f / 3);
  return <svg width={W} height={H} style={{ position: "absolute" }}>
    <rect width={W} height={H} fill="#c89a62" /><Noise x={0} y={0} w={W} h={H} freq={0.05} stretch={14} o={0.3} />
    <Glow x={1300} y={200} r={900} color="#fff2c8" o={0.35} />
    <ellipse cx={960} cy={860} rx={720} ry={60} fill="#000" opacity={0.25} />
    <path d="M300 300 L940 260 L940 840 L300 860 Z" fill="#f6f1e4" /><path d="M980 260 L1620 300 L1620 860 L980 840 Z" fill="#f8f4e8" />
    <rect x={930} y={250} width={60} height={600} fill="#2a5a88" />
    {[0, 1].map(side => Array.from({ length: 12 }, (_, l) => <rect key={`${side}${l}`} x={side ? 1040 : 360} y={340 + l * 40} width={side ? 520 : 520} height={10} rx={5} fill="#9a958a" opacity={0.55} />))}
    <text x={360} y={320} fontFamily="Inter" fontWeight={900} fontSize={30} fill="#2a5a88">CHAPTER {6 + (flips % 9)}</text>
    {/* the page flipping over */}
    {(() => { const u = (f % 3) / 3, w = Math.cos(u * Math.PI) * 640; return <path d={`M960 260 L${960 + w} ${280 - Math.sin(u * Math.PI) * 80} L${960 + w} ${850 - Math.sin(u * Math.PI) * 60} L960 840 Z`} fill="#fffdf6" stroke="#d8d0c0" strokeWidth={2} />; })()}
    {/* words lifting off the pages as gold glyph frames */}
    {Array.from({ length: 24 }, (_, i) => { const t = (f - i * 2) / 30; if (t < 0 || t > 1) return null; return <MemFrame key={i} x={lerp(400 + rnd(i, 1) * 1100, 960 + (rnd(i, 2) - 0.5) * 300, t)} y={lerp(560 + rnd(i, 3) * 200, -80, ease(t))} w={60 + 40 * t} r={(rnd(i, 4) - 0.5) * 40} i={i} o={1 - t * 0.6} />; })}
    <Mit x={1660} y={760} r={64} ang={-20} />
  </svg>;
};

export const ExamInsert: React.FC<{ f: number }> = ({ f }) => {
  const rows = 10, done = Math.min(rows, Math.floor(f / 4));
  const pen = done < rows ? [520 + (f % 4) * 90, 300 + done * 62] : [1300, 980];
  return <svg width={W} height={H} style={{ position: "absolute" }}>
    <rect width={W} height={H} fill="#c89a62" /><Noise x={0} y={0} w={W} h={H} freq={0.05} stretch={14} o={0.3} />
    <g transform="rotate(-3 960 560)">
      <rect x={420} y={120} width={1080} height={960} fill="#fbfaf6" />
      <text x={480} y={200} fontFamily="Inter" fontWeight={900} fontSize={44} fill="#222">POP QUIZ · CHAPTER 6</text>
      <text x={1220} y={200} fontFamily="Inter" fontWeight={800} fontSize={34} fill="#c0392b">Name: LINA</text>
      {Array.from({ length: rows }, (_, r) => <g key={r}>
        <text x={480} y={316 + r * 62} fontFamily="Inter" fontWeight={700} fontSize={30} fill="#444">{r + 1}.</text>
        <line x1={540} y1={322 + r * 62} x2={1420} y2={322 + r * 62} stroke="#c8c4b8" strokeWidth={2} />
        {r < done && <path d={`M560 ${312 + r * 62} q40 -20 80 0 t80 0 t80 -6 t80 4 t60 0`} stroke="#1a3a8a" strokeWidth={5} fill="none" strokeLinecap="round" />}
        {r < done && <path d={`M1360 ${306 + r * 62} l14 14 l28 -30`} stroke="#2a9a4a" strokeWidth={7} fill="none" strokeLinecap="round" opacity={f > 44 ? 1 : 0} />}
      </g>)}
      {f > 46 && <g transform={`translate(1240 980) rotate(-12) scale(${1 + 0.4 * Math.exp(-(f - 46) / 4)})`}><circle r={90} fill="none" stroke="#c0392b" strokeWidth={10} /><text y={26} fontFamily="Inter" fontWeight={900} fontSize={76} fill="#c0392b" textAnchor="middle">100</text></g>}
    </g>
    {/* the clock in the corner: only 4 minutes used */}
    <g transform="translate(1700 180)"><circle r={110} fill="#fff" stroke="#333" strokeWidth={10} /><line x1={0} y1={0} x2={0} y2={-80} stroke="#222" strokeWidth={8} />
      <line x1={0} y1={0} x2={Math.sin(f * 0.02) * 70} y2={-Math.cos(f * 0.02) * 70} stroke="#c0392b" strokeWidth={5} /><text y={160} fontFamily="Inter" fontWeight={900} fontSize={40} fill="#222" textAnchor="middle">4 MIN</text></g>
    {done < rows && <g transform={`translate(${pen[0]} ${pen[1]})`}>
      <path d="M0 0 L-6 -18 L84 -170 L102 -160 L12 -8 Z" fill="#2a5aa8" /><path d="M0 0 L-6 -18 L6 -12 Z" fill="#222" /><rect x={88} y={-186} width={20} height={34} rx={6} fill="#1a3a7a" transform="rotate(30 98 -169)" />
      <Mit x={70} y={-118} r={46} ang={-15} /></g>}
  </svg>;
};

const SUITS = ["♠", "♥", "♦", "♣"], RANKS = ["A", "7", "Q", "3", "10", "K", "5", "J", "2", "9", "4", "8", "6"];
const Card: React.FC<{ x: number; y: number; r: number; i: number; face: number; s?: number; glow?: number }> = ({ x, y, r, i, face, s = 1, glow = 0 }) => {
  const suit = SUITS[Math.floor(i / 13) % 4], red = suit === "♥" || suit === "♦";
  return <g transform={`translate(${x} ${y}) rotate(${r}) scale(${s * Math.max(0.04, Math.abs(Math.cos(face * Math.PI)))} ${s})`}>
    {glow > 0 && <rect x={-66} y={-96} width={132} height={192} rx={14} fill={GOLD} opacity={0.5 * glow} style={{ filter: "blur(8px)" }} />}
    <rect x={-60} y={-90} width={120} height={180} rx={10} fill={face > 0.5 ? "#fdfbf4" : "#2a4a9a"} stroke="#1a1a24" strokeWidth={2} />
    {face <= 0.5 && <rect x={-50} y={-80} width={100} height={160} rx={6} fill="none" stroke="#fff" strokeWidth={3} strokeDasharray="8 6" />}
    {face > 0.5 && <><text x={-44} y={-52} fontFamily="Inter" fontWeight={900} fontSize={34} fill={red ? "#c8302c" : "#1a1a24"}>{RANKS[i % 13]}</text>
      <text x={0} y={22} fontFamily="Inter" fontWeight={900} fontSize={70} fill={red ? "#c8302c" : "#1a1a24"} textAnchor="middle">{suit}</text></>}
  </g>;
};
const PERM = Array.from({ length: 52 }, (_, i) => i).sort((a, b) => rnd(a, 77) - rnd(b, 77));
// the whole deck spread in rows; glance = 0..1 (a gold scan line passes and every card glows once)
export const CardsInsert: React.FC<{ f: number; glance?: number }> = ({ f, glance = -1 }) => {
  const spread = easeOut(f / 20), push = 1 + Math.min(f, 200) * 0.0006;
  return <svg width={W} height={H} style={{ position: "absolute", transform: `scale(${push})`, transformOrigin: "900px 520px" }}>
    <rect width={W} height={H} fill="#d8e2dc" /><rect width={W} height={H} fill="url(#ct)" />
    <defs><radialGradient id="ct" cx="0.5" cy="0.4" r="0.7"><stop offset="0" stopColor="#fff" stopOpacity={0.4} /><stop offset="1" stopColor="#000" stopOpacity={0.15} /></radialGradient></defs>
    {Array.from({ length: 52 }, (_, i) => { const row = Math.floor(i / 13), col = i % 13, tx = 210 + col * 125, ty = 250 + row * 200;
      const x = lerp(960, tx, spread), y = lerp(560, ty, spread), scanX = 150 + glance * 1650, g = glance >= 0 ? sat(1 - Math.abs(tx - scanX) / 120) : 0;
      return <Card key={i} x={x} y={y} r={(rnd(i, 3) - 0.5) * 8 * spread} i={PERM[i]} face={sat((f - 14 - i * 0.35) / 6)} s={0.9} glow={g} />; })}
    {glance >= 0 && glance <= 1 && <rect x={150 + glance * 1650 - 4} y={120} width={8} height={860} fill={GOLD} opacity={0.8} style={{ filter: "blur(2px)" }} />}
  </svg>;
};

export const Bubble: React.FC<{ x: number; y: number; text: string; k: number; w?: number }> = ({ x, y, text, k, w = 640 }) => k <= 0 ? null :
  <g transform={`translate(${x} ${y}) scale(${0.6 + 0.4 * easeOut(k)})`} opacity={Math.min(1, k * 2)}>
    <rect x={-w / 2} y={-90} width={w} height={150} rx={40} fill="#fff" stroke="#1a1a24" strokeWidth={5} />
    <path d="M60 58 L110 120 L130 58 Z" fill="#fff" stroke="#1a1a24" strokeWidth={5} /><rect x={58} y={50} width={76} height={14} fill="#fff" />
    <text x={0} y={-12} fontFamily="Inter" fontWeight={900} fontSize={40} fill="#1a1a24" textAnchor="middle">{text.split("|")[0]}</text>
    <text x={0} y={36} fontFamily="Inter" fontWeight={900} fontSize={40} fill="#c8302c" textAnchor="middle">{text.split("|")[1] ?? ""}</text>
  </g>;
