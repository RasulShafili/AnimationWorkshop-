// YouTube thumbnails (1280x720), two A/B variants. Lessons from the outliers: one big emotional face (>=40% of the
// frame), a rich lit scene, a neon glow line linking hero -> other, and a 1-3 word STORY QUOTE (not the title).
import React from "react";
import { AbsoluteFill } from "remotion";
import { Glow } from "./engine/fx";
import { Character } from "./chars/Rig2";
import { LINA, AYLA } from "./chars/cast";
import { MemFrame } from "./scenes/Title";
import { Door } from "./scenes/Palace";
import { useFonts } from "./ui";
const GOLD = "#ffc94a";
export const Thumb: React.FC<{ v?: "A" | "B" | "C" | "D" }> = ({ v = "A" }) => {
  useFonts();
  if (v === "C" || v === "D") return <ThumbBright v={v} />;
  const quote = v === "A" ? ["SHE FORGOT", "ME."] : ["ONE DAY IS", "MISSING."];
  return <AbsoluteFill style={{ background: v === "A" ? "radial-gradient(circle at 70% 45%, #4a2e6a, #0b0716 70%)" : "radial-gradient(circle at 75% 45%, #2a1e4a, #05030c 70%)" }}>
    <svg width={1280} height={720} style={{ position: "absolute" }}>
      {v === "A" ? <>
        {Array.from({ length: 22 }, (_, i) => { const a = i * 0.9, d = 160 + (i % 7) * 70; return <MemFrame key={i} x={820 + Math.cos(a) * d * 1.3} y={330 + Math.sin(a) * d * 0.7} w={70 + (i % 4) * 22} r={Math.sin(a) * 18} i={i} o={0.75} />; })}
        <Glow x={1010} y={380} r={360} color="#ffd890" o={0.35} />
        {/* Grandma, a little blurred, in her armchair, looking away */}
        <g style={{ filter: "blur(2.5px)" }}><path d="M890 720 L890 360 Q890 320 940 320 L1080 320 Q1130 320 1130 360 L1130 720 Z" fill="#8a5a6a" />
          <Character look={AYLA} pose={{ facing: -1, look: [-0.8, -0.1], mouth: "flat", eyes: 0.9 }} x={1010} y={1000} s={1.65} f={3} seed={4} /></g>
        {/* the gold line from Lina's eye to Grandma */}
        <path d="M470 300 Q760 160 990 330" stroke={GOLD} strokeWidth={7} fill="none" strokeLinecap="round" style={{ filter: `drop-shadow(0 0 10px ${GOLD}) drop-shadow(0 0 24px ${GOLD})` }} />
        <circle cx={990} cy={330} r={10} fill="#fff" style={{ filter: `drop-shadow(0 0 12px ${GOLD})` }} />
      </> : <>
        {[0, 1, 2, 3, 4].map(k => <Door key={k} x={560 + k * 150 - (k === 2 ? 30 : 0)} y={60 + (k === 2 ? -40 : 0)} w={k === 2 ? 190 : 120} h={k === 2 ? 380 : 260} i={k + 3} open={k === 2 ? 0 : 0.5} dark={k === 2} label={k === 2 ? "14 MAR 2020" : undefined} glow={k === 2 ? 0 : 0.8} />)}
        <Glow x={815} y={400} r={160} color="#ff3a3a" o={0.35} />
        <rect x={800} y={416} width={34} height={4} fill="#ffe8b0" opacity={0.9} style={{ filter: "drop-shadow(0 0 8px #ffe8b0)" }} />
      </>}
      {/* Lina's face, huge, left third */}
      <Character look={LINA} pose={v === "A" ? { facing: 1, gold: 1, look: [0.85, -0.25], mouth: "sad", browIn: 0.9, tears: 1, noBlink: true, eyes: 1.15 }
        : { facing: 1, gold: 1, look: [0.9, -0.1], mouth: "o", eyes: 1.3, brow: 0.9, noBlink: true }} x={330} y={1640} s={3.75} f={3} seed={1} rim={{ dx: 10, dy: -8, color: GOLD }} />
    </svg>
    <div style={{ position: "absolute", left: v === "A" ? 640 : 610, top: v === "A" ? 470 : 520, fontFamily: "Inter", fontWeight: 900, fontSize: 96, lineHeight: 0.95, color: "#fff",
      textShadow: "3px 3px 0 #000, -3px 3px 0 #000, 3px -3px 0 #000, -3px -3px 0 #000, 0 8px 0 rgba(0,0,0,.6), 0 0 30px rgba(0,0,0,.7)" }}>
      {quote[0]}<br /><span style={{ color: GOLD }}>{quote[1]}</span></div>
  </AbsoluteFill>;
};

// BRIGHT variants (CTR fix, 2026-11-15: A got 0.6% CTR — too dark, power not visible). Warm saturated light, the
// power shown on screen (gold memory streams into her eyes / gold vs grey split), 3–4 word quote.
const sh = "4px 4px 0 #000, -4px 4px 0 #000, 4px -4px 0 #000, -4px -4px 0 #000, 0 10px 0 rgba(0,0,0,.55)";
const ThumbBright: React.FC<{ v: "C" | "D" }> = ({ v }) => {
  if (v === "C") return <AbsoluteFill style={{ background: "radial-gradient(circle at 35% 45%, #fff3c4 0%, #ffb547 30%, #e0602a 62%, #6a1838 100%)" }}>
    <svg width={1280} height={720} style={{ position: "absolute" }}>
      {Array.from({ length: 26 }, (_, i) => { const a = -0.9 + i * 0.13, d = 260 + (i % 5) * 120; return <g key={i}>
        <line x1={420} y1={300} x2={420 + Math.cos(a) * d * 1.6} y2={300 + Math.sin(a) * d} stroke="#fff6d0" strokeWidth={3} opacity={0.5} />
        <MemFrame x={420 + Math.cos(a) * d * 1.6} y={300 + Math.sin(a) * d} w={60 + (i % 4) * 26} r={a * 20} i={i} o={0.95} /></g>; })}
      <Glow x={420} y={300} r={420} color="#fffbe0" o={0.7} />
      <Character look={LINA} pose={{ facing: 1, gold: 1, look: [0.9, -0.35], mouth: "o", eyes: 1.3, brow: 0.9, noBlink: true }} x={300} y={1640} s={3.75} f={3} seed={1} rim={{ dx: 10, dy: -8, color: "#fff" }} />
    </svg>
    <div style={{ position: "absolute", right: 50, top: 70, textAlign: "right", fontFamily: "Inter", fontWeight: 900, fontSize: 104, lineHeight: 0.95, color: "#fff", textShadow: sh }}>I REMEMBER<br /><span style={{ color: "#ffe14a" }}>EVERY</span><br /><span style={{ color: "#ffe14a" }}>SECOND.</span></div>
  </AbsoluteFill>;
  return <AbsoluteFill style={{ background: "#000" }}>
    <div style={{ position: "absolute", left: 0, top: 0, width: 640, height: 720, background: "radial-gradient(circle at 50% 40%, #fff1b8, #ffb02e 45%, #c8501e 100%)" }} />
    <div style={{ position: "absolute", left: 640, top: 0, width: 640, height: 720, background: "radial-gradient(circle at 50% 40%, #b8bcc8, #6a6e7c 50%, #2a2c34 100%)" }} />
    <svg width={1280} height={720} style={{ position: "absolute" }}>
      {Array.from({ length: 10 }, (_, i) => <MemFrame key={i} x={60 + (i % 5) * 120} y={80 + Math.floor(i / 5) * 560} w={90} r={(i % 3 - 1) * 12} i={i} o={0.95} />)}
      {Array.from({ length: 10 }, (_, i) => <g key={i} opacity={0.35 - i * 0.03} style={{ filter: "grayscale(1) blur(1px)" }}><MemFrame x={700 + (i % 5) * 120} y={80 + Math.floor(i / 5) * 560} w={90} r={(i % 3 - 1) * 12} i={i} o={1} /></g>)}
      <Character look={LINA} pose={{ facing: 1, gold: 1, look: [0.8, -0.1], mouth: "flat", eyes: 1.15, browIn: 0.6, tears: 0.7, noBlink: true }} x={330} y={1420} s={3.0} f={3} seed={1} rim={{ dx: 8, dy: -6, color: "#fff" }} />
      <g style={{ filter: "grayscale(0.85)" }}><Character look={AYLA} pose={{ facing: -1, look: [-0.7, 0.1], mouth: "flat", eyes: 0.85 }} x={960} y={1420} s={3.0} f={3} seed={4} /></g>
      <line x1={640} y1={0} x2={640} y2={720} stroke="#fff" strokeWidth={8} />
    </svg>
    <div style={{ position: "absolute", left: 0, width: 640, top: 500, textAlign: "center", fontFamily: "Inter", fontWeight: 900, fontSize: 84, lineHeight: 0.95, color: "#ffe14a", textShadow: sh }}>I CAN'T<br />FORGET.</div>
    <div style={{ position: "absolute", left: 640, width: 640, top: 500, textAlign: "center", fontFamily: "Inter", fontWeight: 900, fontSize: 84, lineHeight: 0.95, color: "#fff", textShadow: sh }}>SHE CAN'T<br />REMEMBER.</div>
  </AbsoluteFill>;
};
