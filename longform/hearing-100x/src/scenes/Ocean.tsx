// Chapter 8: the deep Pacific — surface light rays, marine snow, a hydrophone, and a huge dark shape with a heartbeat.
import React from "react";
import { Layer, W, H, rnd, lerp, sat } from "../engine/core";
import { Glow } from "../engine/fx";
export const Ocean: React.FC<{ f: number; shape: number; pulse: number }> = ({ f, shape, pulse }) => {
  const b = Math.max(0, Math.sin(f * 0.09)) ** 12 * pulse;
  return <>
    <Layer depth={0.2}>
      <defs><linearGradient id="deep" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#1a5a8a" /><stop offset="0.45" stopColor="#0a2440" /><stop offset="1" stopColor="#02060e" /></linearGradient></defs>
      <rect x={-800} y={-500} width={W + 1600} height={H + 1000} fill="url(#deep)" />
      {Array.from({ length: 7 }, (_, i) => <polygon key={i} points={`${-200 + i * 380 + Math.sin(f * 0.01 + i) * 40},-100 ${-120 + i * 380 + Math.sin(f * 0.01 + i) * 40},-100 ${200 + i * 300},900 ${40 + i * 300},900`} fill="#7ad0ff" opacity={0.06} style={{ mixBlendMode: "screen" }} />)}
    </Layer>
    <Layer depth={0.45}>
      {/* the shape: enormous, barely visible, drifting; its heart glows */}
      <g opacity={shape} transform={`translate(${lerp(1300, 900, sat(f / 500))} 640)`}>
        <path d="M-900 0 Q-600 -260 -100 -240 Q300 -230 600 -80 Q760 0 600 70 Q300 220 -100 210 Q-600 200 -900 0 Z" fill="#03080f" />
        <path d="M-860 0 Q-1100 -180 -1240 -120 Q-1100 0 -1240 120 Q-1100 160 -860 0 Z" fill="#03080f" />
        <circle cx={480} cy={-30} r={18} fill="#9ad8ff" opacity={0.25 + 0.2 * Math.sin(f * 0.05)} />
        <Glow x={60} y={0} r={260 + b * 220} color="#ff3a5a" o={0.1 + b * 0.35} />
      </g>
      {pulse > 0 && [0, 1, 2].map(k => { const t = ((f + k * 30) % 90) / 90; return <circle key={k} cx={lerp(1300, 900, sat(f / 500)) + 60} cy={640} r={100 + t * 1200} fill="none" stroke="#ff6a8a" strokeWidth={4} opacity={(1 - t) * 0.5 * pulse} />; })}
    </Layer>
    <Layer depth={1}>
      {/* hydrophone hanging on its cable */}
      <line x1={420} y1={-300} x2={420} y2={520} stroke="#8aa0b0" strokeWidth={4} /><rect x={392} y={520} width={56} height={110} rx={24} fill="#c8a040" /><rect x={400} y={560} width={40} height={8} fill="#3a3020" /><rect x={400} y={580} width={40} height={8} fill="#3a3020" />
      <Glow x={420} y={580} r={90} color="#ffd890" o={0.35 + 0.4 * b} />
      {Array.from({ length: 140 }, (_, i) => { const y = ((rnd(i, 1) * 1300 + f * (0.3 + rnd(i, 2) * 0.6)) % 1300) - 100; return <circle key={i} cx={-300 + rnd(i, 3) * 2500 + Math.sin(f * 0.02 + i) * 14} cy={y} r={1 + rnd(i, 4) * 2.5} fill="#cfe8ff" opacity={0.3 + rnd(i, 5) * 0.4} />; })}
    </Layer>
  </>;
};
// spectrogram-style HUD of the 1997 recording: a rising sweep
export const Spectro: React.FC<{ k: number; f: number }> = ({ k, f }) => (
  <svg width={W} height={H} style={{ position: "absolute", opacity: k }}>
    <rect x={1260} y={760} width={580} height={240} rx={18} fill="rgba(4,10,20,.75)" stroke="#5ae0ff" strokeWidth={2} />
    <text x={1290} y={800} fontFamily="Inter" fontWeight={800} fontSize={26} fill="#9ad8ff">HYDROPHONE · PACIFIC · 1997</text>
    {Array.from({ length: 60 }, (_, i) => { const x = 1290 + i * 9, sweep = 960 - (i / 60) * 120 - Math.sin(i * 0.2) * 10; const on = i / 60 < k; return <rect key={i} x={x} y={sweep - 20 + rnd(i, 1) * 10} width={7} height={40} fill="#ffcf5a" opacity={on ? 0.4 + rnd(i, 2) * 0.5 : 0.08} />; })}
    <text x={1810} y={990} textAnchor="end" fontFamily="Inter" fontWeight={900} fontSize={30} fill="#ffcf5a">"THE BLOOP"</text>
  </svg>
);
