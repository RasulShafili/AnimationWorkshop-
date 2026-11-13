// YouTube channel banner 2560x1440. Everything important sits inside the 1546x423 centre (safe on every device).
import React from "react";
import { AbsoluteFill, delayRender, continueRender } from "remotion";
import "@fontsource/inter/800.css";
import "@fontsource/inter/900.css";
import { Character } from "./chars/Rig";
import { HERO, MIA } from "./chars/cast";
import { Glow } from "./engine/fx";
import { rnd } from "./engine/core";
const SX = (2560 - 1546) / 2, SY = (1440 - 423) / 2;
export const Banner: React.FC<{ guides?: boolean }> = ({ guides = false }) => {
  const [h] = React.useState(() => delayRender("fonts"));
  React.useEffect(() => { Promise.all([document.fonts.load("900 80px Inter"), document.fonts.load("800 40px Inter")]).then(() => continueRender(h)); }, [h]);
  // a spiral galaxy (left) from points
  const gal = Array.from({ length: 2600 }, (_, i) => { const arm = i % 2, r = Math.pow(rnd(i, 1), 0.6) * 300, a = arm * Math.PI + r * 0.018 + (rnd(i, 2) - 0.5) * 0.6; return [330 + Math.cos(a) * r * 1.6, 560 + Math.sin(a) * r * 0.6, rnd(i, 3)]; });
  return <AbsoluteFill style={{ background: "linear-gradient(180deg, #05061a 0%, #141a4a 45%, #3a2a5a 75%, #a85a6a 100%)" }}>
    <svg width={2560} height={1440}>
      {Array.from({ length: 700 }, (_, i) => <circle key={i} cx={rnd(i, 11) * 2560} cy={rnd(i, 12) * 1100} r={0.8 + rnd(i, 13) * 2.2} fill="#fff" opacity={0.25 + rnd(i, 14) * 0.7} />)}
      <Glow x={330} y={560} r={520} color="#ffd8a0" o={0.35} />
      {gal.map(([x, y, b], i) => <circle key={i} cx={x} cy={y} r={0.8 + b * 2} fill={b > 0.85 ? "#ff9ac8" : b > 0.5 ? "#cfe0ff" : "#ffe2b0"} opacity={0.35 + b * 0.5} />)}
      <Glow x={330} y={560} r={140} color="#fff2d0" o={0.9} />
      {/* black hole with a lensing ring (right of centre, top) */}
      <Glow x={2050} y={420} r={300} color="#ffb070" o={0.35} />
      <circle cx={2050} cy={420} r={150} fill="none" stroke="#ffc890" strokeWidth={10} opacity={0.85} /><circle cx={2050} cy={420} r={120} fill="#02020a" />
      {/* snowy mountains + city skyline along the bottom */}
      {Array.from({ length: 9 }, (_, i) => { const x = i * 330 - 100, hgt = 240 + rnd(i, 21) * 180; return <path key={i} d={`M${x - 260} 1440 L${x} ${1440 - hgt} L${x + 260} 1440 Z`} fill="#22264a" />; })}
      {Array.from({ length: 40 }, (_, i) => { const x = i * 66, hh = 80 + rnd(i, 31) * 160; return <g key={i}><rect x={x} y={1440 - hh} width={58} height={hh} fill="#0c0e22" />{Array.from({ length: 6 }, (_, k) => rnd(i * 9 + k, 32) > 0.5 ? <rect key={k} x={x + 8 + (k % 2) * 24} y={1440 - hh + 14 + Math.floor(k / 2) * 30} width={10} height={14} fill="#ffcf7a" opacity={0.8} /> : null)}</g>; })}
      {/* the rooftop they stand on: flat roof, parapet, water tank, antenna, lit windows below */}
      <rect x={1640} y={1150} width={760} height={300} fill="#141634" /><rect x={1620} y={1138} width={800} height={18} rx={4} fill="#2a2e5a" />
      {Array.from({ length: 12 }, (_, k) => <rect key={k} x={1680 + (k % 6) * 120} y={1200 + Math.floor(k / 6) * 110} width={60} height={70} fill={rnd(k, 41) > 0.4 ? "#ffcf7a" : "#2a2e5a"} opacity={0.85} />)}
      <rect x={2300} y={1010} width={80} height={130} rx={10} fill="#2a2e5a" /><path d="M2290 1010 L2340 970 L2390 1010 Z" fill="#2a2e5a" /><line x1={1700} y1={1138} x2={1700} y2={1010} stroke="#2a2e5a" strokeWidth={6} /><circle cx={1700} cy={1006} r={6} fill="#ff4a4a" />
      {/* sound rings behind the hero (right side of the safe area) */}
      {[0, 1, 2, 3].map(k => <circle key={k} cx={1880} cy={760} r={120 + k * 70} fill="none" stroke="#5ae0ff" strokeWidth={6} opacity={0.6 - k * 0.12} />)}
      <Character look={HERO} pose={{ mouth: "grin", brow: 0.6, look: [-1, -0.2], facing: -1, aR: [150, 20], hands: "open" }} x={1900} y={1140} s={1.15} rim={{ dx: -6, dy: -4, color: "#5ae0ff" }} />
      <Character look={MIA} pose={{ mouth: "smile", look: [1, -0.2], aL: [30, 40] }} x={2180} y={1140} s={0.95} rim={{ dx: -5, dy: -4, color: "#ffb06a" }} />
      {guides && <><rect x={SX} y={SY} width={1546} height={423} fill="none" stroke="#ff0" strokeWidth={4} strokeDasharray="20 12" /></>}
    </svg>
    {/* title inside the safe area */}
    <div style={{ position: "absolute", left: SX + 40, top: SY + 40, width: 1100, fontFamily: "Inter", color: "#fff" }}>
      <div style={{ fontWeight: 900, fontSize: 132, letterSpacing: -4, lineHeight: 1, textShadow: "0 8px 0 rgba(0,0,0,.45)" }}>whatif<span style={{ color: "#ffc34a" }}>.lab</span><span style={{ color: "#5ae0ff", fontSize: 92 }}>_daily</span></div>
      <div style={{ marginTop: 22, fontWeight: 800, fontSize: 46, color: "#e8ecff", textShadow: "0 4px 0 rgba(0,0,0,.4)" }}>Wild "what if" questions — animated.</div>
      <div style={{ marginTop: 18, display: "inline-block", padding: "10px 26px", borderRadius: 999, background: "#e8322a", fontWeight: 900, fontSize: 36 }}>NEW VIDEOS EVERY WEEK</div>
    </div>
  </AbsoluteFill>;
};
