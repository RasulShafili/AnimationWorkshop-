// 1.8 s chapter title card between chapters: a glowing door opens a crack, "CHAPTER N" + the title (matches the
// YouTube chapter list). Props: num, title.
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { W, H, sat, easeOut, rnd } from "./engine/core";
import { Glow } from "./engine/fx";
import { MemFrame } from "./scenes/Title";
import { useFonts } from "./ui";
export const ChapterCard: React.FC<{ num: number; title: string }> = ({ num, title }) => {
  useFonts(); const f = useCurrentFrame(); const k = easeOut(f / 14), out = sat((f - 44) / 10);
  return <AbsoluteFill style={{ background: "#07050f", opacity: 1 - out * 0.9 }}>
    <svg width={W} height={H} style={{ position: "absolute" }}>
      <Glow x={960} y={520} r={700} color="#8a6ac8" o={0.3} />
      {Array.from({ length: 14 }, (_, i) => <MemFrame key={i} x={160 + rnd(i, 1) * 1600} y={140 + rnd(i, 2) * 800 - f * (0.6 + rnd(i, 3))} w={70 + rnd(i, 4) * 60} r={(rnd(i, 5) - 0.5) * 30} i={i + num} o={0.35} />)}
      <g transform="translate(960 380)" opacity={k}>
        <path d="M-90 170 L-90 -40 A90 90 0 0 1 90 -40 L90 170 Z" fill="#000" stroke="#ffc94a" strokeWidth={6} />
        <path d={`M-90 170 L-90 -40 A90 90 0 0 1 ${-90 + 180 * (1 - 0.35 * k)} ${-40 - 0} L${-90 + 180 * (1 - 0.35 * k)} 170 Z`} fill="#5a3a24" />
        <rect x={-90 + 180 * (1 - 0.35 * k)} y={-120} width={180 * 0.35 * k} height={290} fill="#ffe8b0" opacity={0.8} />
        <Glow x={60} y={60} r={260 * k} color="#ffc94a" o={0.5} />
      </g>
    </svg>
    <div style={{ position: "absolute", top: 610, width: "100%", textAlign: "center", fontFamily: "Inter", fontWeight: 900, fontSize: 40, letterSpacing: 14, color: "#ffc94a", opacity: k }}>CHAPTER {num}</div>
    <div style={{ position: "absolute", top: 668, width: "100%", textAlign: "center", fontFamily: "Inter", fontWeight: 900, fontSize: 96, color: "#fff", opacity: sat((f - 6) / 12), transform: `translateY(${(1 - easeOut((f - 6) / 16)) * 30}px)` }}>{title.toUpperCase()}</div>
  </AbsoluteFill>;
};
