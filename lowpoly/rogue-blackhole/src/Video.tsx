import React, { useEffect, useState } from "react";
import * as THREE from "three";
import { AbsoluteFill, Audio, staticFile, useCurrentFrame, delayRender, continueRender, interpolate, Easing } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import "@fontsource/inter/800.css";
import "@fontsource/inter/900.css";
import { World, beatOf, shotAt, cameraFor, toScreen } from "./World";
import { LensPost } from "./LensPost";
import { Captions } from "./Captions";
import { useSim, bodyAt, coreAt } from "./data";
import T from "./timeline.json";
import WORDS from "./words.json";

const B = T.beats;
const sat = (v: number) => Math.min(1, Math.max(0, v));
const sh = "0 4px 0 rgba(4,4,20,.6), 0 10px 30px rgba(4,4,20,.6)";
const ACC = ["#ffb46a", "#9ec8ff", "#c8b0ff", "#ffd36a", "#ff8a5a", "#ff5a5a", "#9ee0ff", "#ffd36a"];

// lake shore with pines (today) / a frozen ridge with ice (after)
const Shore: React.FC = () => (
  <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }} viewBox="0 0 1080 1920">
    <defs><linearGradient id="hz" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="rgba(30,50,110,0)" /><stop offset="1" stopColor="rgba(50,70,140,.45)" /></linearGradient></defs>
    <rect x={0} y={1250} width={1080} height={320} fill="url(#hz)" />
    <path d="M0 1560 L1080 1560 L1080 1920 L0 1920 Z" fill="#060a14" />
    <rect x={0} y={1560} width={1080} height={110} fill="rgba(80,110,180,.10)" />
    {Array.from({ length: 22 }, (_, i) => { const x = i * 52 + (i % 3) * 9, h = 120 + ((i * 37) % 90); return <path key={i} d={`M${x} 1565 L${x + 26} ${1565 - h} L${x + 52} 1565 Z`} fill="#03050b" />; })}
    <path d="M0 1690 L1080 1700 L1080 1920 L0 1920 Z" fill="#02030a" />
    <g fill="#02030a" transform="translate(800 1700)"><circle cx={0} cy={-150} r={17} /><path d="M-14 -132 Q-24 -80 -18 -40 L-22 0 L-8 0 L-2 -38 L6 -38 L12 0 L26 0 L20 -40 Q26 -86 14 -132 Z" /><path d="M-10 -122 L-40 -176 L-30 -180 L-2 -128 Z" /></g>
  </svg>
);
const Frozen: React.FC<{ k: number }> = ({ k }) => (
  <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }} viewBox="0 0 1080 1920">
    <path d="M0 1480 L140 1430 L260 1470 L400 1400 L540 1460 L680 1410 L820 1470 L960 1420 L1080 1450 L1080 1920 L0 1920 Z" fill="#0c1220" />
    <path d="M140 1430 L190 1452 L230 1440 L260 1470 M400 1400 L450 1428 L500 1418 L540 1460 M680 1410 L730 1436 L780 1430 M960 1420 L1010 1440" stroke="#9fb6d8" strokeWidth={6} fill="none" opacity={0.6} />
    <path d="M0 1600 L1080 1600 L1080 1920 L0 1920 Z" fill="#0a1424" />
    {Array.from({ length: 18 }, (_, i) => <path key={i} d={`M${i * 60} 1600 L${i * 60 + 30 + (i % 4) * 8} ${1640 + (i % 5) * 20} L${i * 60 + 70} 1600`} stroke="#a8c4e8" strokeWidth={2} fill="none" opacity={0.35 * k} />)}
    <rect x={0} y={1600} width={1080} height={320} fill={`rgba(170,200,240,${0.12 * k})`} />
    <g fill="#04070e" transform="translate(300 1600)"><circle cx={0} cy={-150} r={19} /><path d="M-20 -132 Q-30 -80 -24 -40 L-26 0 L-8 0 L-2 -38 L6 -38 L12 0 L30 0 L24 -40 Q32 -86 20 -132 Z" /><path d="M-18 -120 L-34 -60 L-24 -58 L-10 -112 Z M18 -120 L34 -60 L24 -58 L10 -112 Z" /></g>
  </svg>
);
const Label: React.FC<{ x: number; y: number; text: string; color: string; o?: number }> = ({ x, y, text, color, o = 1 }) => (
  <div style={{ position: "absolute", left: Math.min(880, Math.max(200, x)) - 200, top: y + 26, width: 400, textAlign: "center", fontFamily: "Inter", fontWeight: 900, fontSize: 36, color, textShadow: sh, opacity: o, letterSpacing: 2 }}>{text}</div>
);

export const Video: React.FC<{ withAudio?: boolean }> = ({ withAudio = true }) => {
  const f = useCurrentFrame();
  const sim = useSim();
  const [h] = useState(() => delayRender("fonts"));
  useEffect(() => { Promise.all([document.fonts.load("900 80px Inter"), document.fonts.load("800 40px Inter")]).then(() => continueRender(h)); }, [h]);
  const b = beatOf(f), lf = f - B[b], [l1, l2] = T.texts[b];
  const inT = b === 0 ? 1 : interpolate(lf, [2, 12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const outT = b === B.length - 2 ? 1 : interpolate(B[b + 1] - f, [0, 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const pop = b === 0 ? 1 : 1 + 0.2 * Math.exp(-Math.max(0, lf - 2) / 5);
  const s = shotAt(f), ground = s.mode === "ground";
  const dip = Math.max(...[B[1], B[2], B[3], B[6], T.frozenIn, B[7]].map(c => sat(1 - Math.abs(f - c) / 4)));
  let labels: { x: number; y: number; text: string; color: string; o: number }[] = [];
  if (sim && s.mode === "space") {
    const pc = new THREE.PerspectiveCamera(50, 1080 / 1920, 0.001, 5000); cameraFor(f, sim, pc);
    const add = (p: number[], text: string, color: string, o = 1) => { const q = toScreen(pc, p); if (q[2] < 1 && q[0] > 60 && q[0] < 1020 && q[1] > 450 && q[1] < 1700) labels.push({ x: q[0], y: q[1], text, color, o }); };
    if (b === 3) { add(coreAt(sim, s.t, 0), "SUN", "#ffd890"); add(coreAt(sim, s.t, 1), "BLACK HOLE", "#c8b0ff", sat((lf - 20) / 15)); }
    if (b === 4) { add(bodyAt(sim, s.t, 4), "JUPITER", "#ffcf90", sat((lf - 30) / 10)); add(bodyAt(sim, s.t, 2), "EARTH", "#8ab8ff"); }
    if (b === 5 || b === 6 || b === 7) { add(bodyAt(sim, s.t, 2), "EARTH", "#8ab8ff"); if (b !== 5) add(coreAt(sim, s.t, 0), "SUN", "#ffd890", 0.8); }
  }
  const yrs = b === 3 ? `+${Math.round(20 * sat(lf / (B[4] - B[3])))} YEARS` : "";
  return (
    <AbsoluteFill style={{ backgroundColor: "#010104" }}>
      {sim && <ThreeCanvas width={1080} height={1920} dpr={1} camera={{ fov: 50, position: [0, 0, 10] }} gl={{ antialias: true }}>
        <World f={f} sim={sim} />
        <LensPost />
      </ThreeCanvas>}
      {ground && !s.frozen && <Shore />}
      {ground && s.frozen && <Frozen k={sat((f - T.frozenIn) / 40)} />}
      {ground && s.frozen && sim && (() => { const pc = new THREE.PerspectiveCamera(50, 1080 / 1920, 0.001, 5000); cameraFor(f, sim, pc); const q = toScreen(pc, coreAt(sim, s.t, 0)); return <Label x={q[0]} y={q[1]} text="THE SUN" color="#ffd890" o={sat((f - T.frozenIn - 20) / 15)} />; })()}
      {labels.map((l, i) => <Label key={i} {...l} />)}
      {b === 1 && <div style={{ position: "absolute", top: 1180, width: "100%", textAlign: "center", fontFamily: "Inter", fontWeight: 800, fontSize: 34, color: "#cfd8ff", textShadow: sh, opacity: sat((lf - 20) / 15), letterSpacing: 1 }}>OGLE-2011-BLG-0462 · 5,000 LIGHT-YEARS AWAY</div>}
      {b === 7 && <div style={{ position: "absolute", bottom: 330, width: "100%", display: "flex", justifyContent: "center", gap: 36, fontFamily: "Inter", fontWeight: 900, fontSize: 72 }}>
        <span style={{ padding: "10px 36px", borderRadius: 22, background: "#3a2a6a", color: "#fff", textShadow: sh, border: "4px solid #c8b0ff", transform: `scale(${1 + 0.05 * Math.sin(f * 0.25)})` }}>SWALLOWED</span>
        <span style={{ padding: "10px 36px", borderRadius: 22, background: "#1a4a7a", color: "#fff", textShadow: sh, border: "4px solid #9ee0ff", transform: `scale(${1 + 0.05 * Math.sin(f * 0.25 + 1.6)})` }}>FROZEN</span>
      </div>}
      <AbsoluteFill style={{ background: `rgba(0,0,0,${dip})` }} />
      <AbsoluteFill style={{ fontFamily: "Inter", alignItems: "center", textAlign: "center", color: "#fff" }}>
        <div style={{ transform: `scale(${pop})`, marginTop: 190, fontWeight: 900, fontSize: 82, lineHeight: 1.0, letterSpacing: -2, textShadow: sh, opacity: inT * outT }}>{l1}</div>
        <div style={{ transform: `scale(${pop})`, fontWeight: 900, fontSize: l2.length > 18 ? 64 : 92, lineHeight: 1.05, letterSpacing: -1, color: ACC[b], textShadow: sh, opacity: inT * outT, padding: "0 40px" }}>{l2}</div>
        {yrs && <div style={{ marginTop: 16, fontWeight: 800, fontSize: 40, color: "#cfe0ff", textShadow: sh }}>{yrs}</div>}
      </AbsoluteFill>
      <Captions f={f} words={WORDS} top={ground ? 1150 : 1400} accent={ACC[b]} size={84} />
      {withAudio && <Audio src={staticFile("mix.wav")} />}
    </AbsoluteFill>
  );
};
