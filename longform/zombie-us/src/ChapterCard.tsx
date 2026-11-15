// 1.8 s chapter card between chapters (matches the YouTube chapter list): dark, a flickering fluorescent tube,
// grey hands rising at the bottom, "CHAPTER N" + the title, and an optional red marker day tag.
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { W, H, sat, easeOut, rnd } from "./engine/core";
import { Glow } from "./engine/fx";
import { useFonts } from "./ui";
export const ChapterCard: React.FC<{ num: number; title: string; day?: string }> = ({ num, title, day }) => {
  useFonts(); const f = useCurrentFrame(); const k = easeOut(f / 12), out = sat((f - 44) / 10), flick = rnd(Math.floor(f / 2), num) > 0.15 ? 1 : 0.3;
  return <AbsoluteFill style={{ background: "#06080c", opacity: 1 - out * 0.9 }}>
    <svg width={W} height={H} style={{ position: "absolute" }}>
      <rect x={760} y={190} width={400} height={16} rx={8} fill={flick > 0.5 ? "#e8fff0" : "#3a4a40"} /><Glow x={960} y={200} r={700} color="#9ad8a8" o={0.22 * flick} />
      {Array.from({ length: 16 }, (_, i) => { const x = 60 + i * 120 + rnd(i, num) * 40, y = 1120 - 140 * easeOut((f - i * 1.5) / 20) - rnd(i, num + 1) * 60;
        return <g key={i} transform={`translate(${x} ${y}) rotate(${(rnd(i, 3) - 0.5) * 30})`} opacity={0.55}><rect x={-40} y={20} width={80} height={200} fill="#3a4a3a" /><ellipse cx={0} cy={0} rx={30} ry={36} fill="#4a5e4a" />{[-22, -8, 6, 20].map((fx, kk) => <rect key={kk} x={fx - 6} y={-74 + Math.abs(kk - 1.5) * 6} width={13} height={44} rx={6} fill="#4a5e4a" />)}</g>; })}
    </svg>
    <div style={{ position: "absolute", top: 380, width: "100%", textAlign: "center", fontFamily: "Inter", fontWeight: 900, fontSize: 40, letterSpacing: 14, color: "#9ad88a", opacity: k }}>CHAPTER {num}</div>
    <div style={{ position: "absolute", top: 440, width: "100%", textAlign: "center", fontFamily: "Inter", fontWeight: 900, fontSize: 104, color: "#fff", opacity: sat((f - 5) / 10), transform: `translateY(${(1 - easeOut((f - 5) / 14)) * 30}px)` }}>{title.toUpperCase()}</div>
    {day && <div style={{ position: "absolute", top: 590, width: "100%", textAlign: "center", fontFamily: "'Permanent Marker'", fontSize: 64, color: "#d8202a", opacity: sat((f - 12) / 8), transform: "rotate(-2deg)" }}>{day}</div>}
  </AbsoluteFill>;
};
