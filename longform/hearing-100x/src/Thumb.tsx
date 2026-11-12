// YouTube thumbnail 1280x720: the hero, headphones off, a glowing heartbeat behind the wall, big title.
import React from "react";
import { AbsoluteFill, delayRender, continueRender } from "remotion";
import "@fontsource/inter/900.css";
import { Character } from "./chars/Rig";
import { HERO } from "./chars/cast";
import { Glow } from "./engine/fx";
export const Thumb: React.FC = () => {
  const [h] = React.useState(() => delayRender("fonts"));
  React.useEffect(() => { document.fonts.load("900 80px Inter").then(() => continueRender(h)); }, [h]);
  return <AbsoluteFill style={{ background: "radial-gradient(circle at 70% 50%, #2a3a8a, #0a0618 70%)" }}>
    <svg width={1280} height={720}>
      {[0, 1, 2, 3, 4].map(k => <circle key={k} cx={930} cy={330} r={90 + k * 80} fill="none" stroke="#5ae0ff" strokeWidth={6} opacity={0.7 - k * 0.12} />)}
      <Glow x={930} y={330} r={260} color="#ff3a5a" o={0.8} />
      <path transform="translate(930 330) scale(3.2)" d="M0 18 C -26 -2 -22 -26 -6 -24 C 0 -23 0 -18 0 -14 C 0 -18 0 -23 6 -24 C 22 -26 26 -2 0 18 Z" fill="#ff4a6a" />
      <Character look={{ ...HERO, headphones: "neck" }} pose={{ mouth: "o", brow: 1, look: [1, -0.2], aL: [-160, -40], aR: [25, 40], head: -6 }} x={400} y={1040} s={2.0} rim={{ dx: 6, dy: -4, color: "#5ae0ff" }} />
    </svg>
    <div style={{ position: "absolute", left: 700, top: 420, fontFamily: "Inter", fontWeight: 900, fontSize: 130, color: "#fff", letterSpacing: -4, textShadow: "0 8px 0 rgba(0,0,0,.6)", lineHeight: 0.95 }}>100×<br /><span style={{ color: "#ffc34a", fontSize: 104 }}>HEARING</span></div>
  </AbsoluteFill>;
};
