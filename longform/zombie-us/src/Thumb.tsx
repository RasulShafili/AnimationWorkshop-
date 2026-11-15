// YouTube thumbnails 1280x720. Rule: the thumbnail ANSWERS the title ("What If A Zombie Virus Started In The US?"),
// bright and saturated, a big emotional face, a 2–4 word story quote. A = the glass + hands, B = the map from Atlanta.
import React from "react";
import { AbsoluteFill } from "remotion";
import { Glow } from "./engine/fx";
import { Character } from "./chars/Rig2";
import { KAI, MIRA, ZOMBIES, zombiePose } from "./chars/cast";
import { USMap } from "./scenes/World";
import { useFonts } from "./ui";
import { rnd } from "./engine/core";
const T: React.FC<{ children: React.ReactNode; size: number; color?: string; style?: React.CSSProperties }> = ({ children, size, color = "#fff", style }) =>
  <div style={{ fontFamily: "Inter", fontWeight: 900, fontSize: size, lineHeight: 0.95, color, letterSpacing: -2, textShadow: "4px 4px 0 #000, -4px 4px 0 #000, 4px -4px 0 #000, -4px -4px 0 #000, 0 10px 30px rgba(0,0,0,.6)", ...style }}>{children}</div>;
const Hand: React.FC<{ x: number; y: number; s: number; r: number }> = ({ x, y, s, r }) => <g transform={`translate(${x} ${y}) scale(${s}) rotate(${r})`}>
  <ellipse cx={0} cy={0} rx={30} ry={36} fill="#7fa070" />{[-22, -8, 6, 20].map((fx, k) => <rect key={k} x={fx - 6} y={-74 + Math.abs(k - 1.5) * 6} width={13} height={44} rx={6} fill="#7fa070" />)}<rect x={26} y={-14} width={12} height={34} rx={6} fill="#7fa070" transform="rotate(30 30 0)" /></g>;
export const Thumb: React.FC<{ v: string }> = ({ v }) => {
  useFonts();
  if (v === "B") return <AbsoluteFill style={{ background: "radial-gradient(circle at 70% 45%, #3a5a9a, #142446 70%)" }}>
    <div style={{ position: "absolute", left: 380, top: 40, width: 1920, height: 1080, transform: "scale(0.55)", transformOrigin: "0 0" }}><USMap f={0} spread={0.3} routes={1} bare /></div>
    <svg width={1280} height={720} style={{ position: "absolute" }}><Glow x={1072} y={401} r={160} color="#ff3a2a" o={0.9} /><circle cx={1072} cy={401} r={26} fill="none" stroke="#fff" strokeWidth={6} /><circle cx={1072} cy={401} r={44} fill="none" stroke="#ff3a2a" strokeWidth={5} />
      <Character look={KAI} pose={{ facing: 1, mouth: "o", eyes: 1.35, brow: 0.9, look: [0.9, 0.1], aR: [95, 0] }} x={250} y={1240} s={2.6} f={0} seed={1} rim={{ dx: 6, dy: -4, color: "#ff6a3a" }} /></svg>
    <T size={100} style={{ position: "absolute", right: 40, bottom: 34, textAlign: "right" }}>IT STARTED<br /><span style={{ color: "#ff3a2a" }}>HERE.</span></T>
  </AbsoluteFill>;
  // A: inside the bright store at night, hands and glowing eyes all over the glass
  return <AbsoluteFill style={{ background: "#0c1626" }}>
    <svg width={1280} height={720} style={{ position: "absolute" }}>
      <rect width={1280} height={720} fill="#11203a" />
      {Array.from({ length: 26 }, (_, i) => <Character key={i} look={ZOMBIES[i % ZOMBIES.length]} pose={{ facing: (i % 2 ? -1 : 1) as 1 | -1, ...zombiePose(i * 7, i) }} x={480 + rnd(i, 3) * 820} y={430 + (i % 3) * 120} s={0.55 + (i % 3) * 0.25} f={0} seed={i} />)}
      {Array.from({ length: 16 }, (_, i) => <Hand key={i} x={520 + rnd(i, 7) * 740} y={90 + rnd(i, 8) * 520} s={1.2 + rnd(i, 9) * 0.6} r={(rnd(i, 10) - 0.5) * 40} />)}
      {[600, 900, 1200].map(x => <rect key={x} x={x} y={0} width={18} height={720} fill="#2a3446" />)}<rect x={0} y={0} width={1280} height={22} fill="#2a3446" />
      <rect x={0} y={0} width={1280} height={720} fill="#9ad8ff" opacity={0.06} />
      <rect x={0} y={0} width={620} height={720} fill="#000" opacity={0.25} />
      <Glow x={280} y={480} r={420} color="#ffb060" o={0.55} />
      <Character look={MIRA} pose={{ facing: 1, mouth: "o", eyes: 1.3, brow: 0.9, look: [0.9, -0.2], hold: "torch", beam: 1, aR: [80, 6] }} x={430} y={900} s={1.6} f={0} seed={2} />
      <Character look={KAI} pose={{ facing: 1, mouth: "o", eyes: 1.35, brow: 0.9, look: [0.9, -0.1] }} x={210} y={1230} s={2.4} f={0} seed={1} rim={{ dx: 6, dy: -4, color: "#9ad8ff" }} />
    </svg>
    <div style={{ position: "absolute", left: 40, top: 30, fontFamily: "'Permanent Marker'", fontSize: 92, color: "#e8202a", transform: "rotate(-4deg)", textShadow: "0 0 10px #000, 0 0 30px #000" }}>DAY 3</div>
    <T size={86} style={{ position: "absolute", right: 36, bottom: 40, textAlign: "right" }}>DON'T MAKE<br /><span style={{ color: "#ffd34a" }}>A SOUND.</span></T>
  </AbsoluteFill>;
};
