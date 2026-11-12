// Title card: a heartbeat line that turns into sound rings, then the question.
import React from "react";
import { W, H, sat, easeOut } from "../engine/core";
import { Glow } from "../engine/fx";
export const Title: React.FC<{ f: number }> = ({ f }) => {
  const draw = sat(f / 30), rings = [0, 12, 24, 36].map(d => f - 20 - d).filter(t => t > 0);
  const ecg = Array.from({ length: 120 }, (_, i) => { const x = i * 16, k = i % 30; const y = 540 + (k === 14 ? -110 : k === 15 ? 90 : k === 16 ? -30 : 0); return `${i ? "L" : "M"}${x} ${y}`; }).join(" ");
  const t = easeOut((f - 24) / 20);
  return <svg width={W} height={H} style={{ position: "absolute" }}>
    <rect width={W} height={H} fill="#06050c" />
    <Glow x={960} y={540} r={700} color="#3a5aff" o={0.25} />
    <path d={ecg} stroke="#ff4a6a" strokeWidth={5} fill="none" strokeDasharray={2000} strokeDashoffset={2000 * (1 - draw)} opacity={1 - sat((f - 30) / 20)} style={{ filter: "drop-shadow(0 0 8px #ff4a6a)" }} />
    {rings.map((r, i) => <circle key={i} cx={960} cy={540} r={r * 26} fill="none" stroke="#5ae0ff" strokeWidth={3} opacity={sat(1 - r / 50) * 0.8} />)}
    <g opacity={t} transform={`translate(960 ${540 + (1 - t) * 30})`} style={{ filter: "drop-shadow(0 0 18px rgba(90,224,255,.45))" }}>
      <text y={-30} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={92} fill="#fff" letterSpacing={-2}>WHAT IF YOUR HEARING</text>
      <text y={80} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={110} fill="#ffc34a" letterSpacing={-2}>WAS 100× BETTER?</text>
    </g>
  </svg>;
};
