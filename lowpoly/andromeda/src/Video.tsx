import React, { useEffect, useState } from "react";
import { AbsoluteFill, Audio, staticFile, useCurrentFrame, delayRender, continueRender, interpolate, Easing } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import "@fontsource/inter/800.css";
import "@fontsource/inter/900.css";
import * as THREE from "three";
import { World, beatOf, shotAt, cameraFor, toScreen } from "./World";
import { coreAt } from "./data";
import { Post } from "./Post";
import { Captions } from "./Captions";
import { useSim } from "./data";
import T from "./timeline.json";
import WORDS from "./words.json";

const B = T.beats;
const sat = (v: number) => Math.min(1, Math.max(0, v));
const sh = "0 4px 0 rgba(4,4,20,.6), 0 10px 30px rgba(4,4,20,.6)";
const ACC = ["#ffd36a", "#9ec8ff", "#ffd36a", "#ff9ad0", "#ff8ac0", "#ffd36a", "#ff6a6a", "#9ec8ff"];
const rnd = (i: number, k = 0) => { let h = Math.imul(i ^ 0x9e3779b9, 2654435761) ^ Math.imul(k + 7, 40503); h ^= h >>> 15; h = Math.imul(h, 2246822519); h ^= h >>> 13; return (h >>> 0) / 4294967296; };

// night horizon: two ridges, a stargazer with a telescope
const Silhouette: React.FC<{ glow: number }> = ({ glow }) => (
  <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }} viewBox="0 0 1080 1920">
    <defs><linearGradient id="hz" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={`rgba(40,60,120,0)`} /><stop offset="1" stopColor={`rgba(60,80,150,${0.35 * glow})`} /></linearGradient></defs>
    <rect x={0} y={1300} width={1080} height={300} fill="url(#hz)" />
    <path d="M0 1520 L120 1470 L230 1500 L360 1420 L470 1480 L600 1440 L720 1495 L860 1430 L980 1470 L1080 1450 L1080 1920 L0 1920 Z" fill="#0a0c18" />
    <path d="M0 1600 L160 1560 L300 1590 L420 1550 L560 1600 L700 1570 L860 1610 L1000 1575 L1080 1590 L1080 1920 L0 1920 Z" fill="#04050b" />
    {/* stargazer looking up-left, telescope on a tripod */}
    <g fill="#04050b" transform="translate(720 1600)">
      <circle cx={0} cy={-150} r={17} />
      <path d="M-14 -132 Q-24 -80 -18 -40 L-22 0 L-8 0 L-2 -38 L6 -38 L12 0 L26 0 L20 -40 Q26 -86 14 -132 Z" />
      <path d="M-10 -122 L-48 -170 L-40 -176 L-2 -128 Z" />
      <path d="M-100 -150 L-36 -110 L-30 -120 L-94 -160 Z" />
      <path d="M-62 -128 L-86 0 L-80 0 L-58 -122 Z M-62 -128 L-40 0 L-34 0 L-56 -126 Z M-60 -126 L-62 0 L-56 0 L-56 -126 Z" />
    </g>
  </svg>
);
// 100 simulated futures: half end in a collision (red), half miss (blue)
const Futures: React.FC<{ k: number; from: number[]; to: number[] }> = ({ k, from, to }) => (
  <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }} viewBox="0 0 1080 1920">
    {Array.from({ length: 100 }, (_, i) => {
      const hit = rnd(i, 1) < 0.5, sx = from[0] + (rnd(i, 3) - 0.5) * 40, sy = from[1] + (rnd(i, 2) - 0.5) * 40;
      const dx = to[0] - from[0], dy = to[1] - from[1], nx = -dy, ny = dx, side = rnd(i, 6) > 0.5 ? 1 : -1, miss = 0.35 + rnd(i, 4) * 0.5;
      const ex = hit ? to[0] + (rnd(i, 4) - 0.5) * 30 : to[0] + dx * 0.5 + nx * miss * side, ey = hit ? to[1] + (rnd(i, 5) - 0.5) * 30 : to[1] + dy * 0.5 + ny * miss * side;
      const cx = (sx + ex) / 2 + (rnd(i, 7) - 0.5) * 300, cy = (sy + ey) / 2 + (rnd(i, 8) - 0.5) * 200;
      const d = `M${sx} ${sy} Q${cx} ${cy} ${ex} ${ey}`, show = sat(k * 1.6 - i / 100);
      return <path key={i} d={d} stroke={hit ? "#ff5a5a" : "#6aa8ff"} strokeWidth={2.5} fill="none" opacity={0.55 * show} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - show} />;
    })}
  </svg>
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
  const s = shotAt(f) as any, sky = s.mode === "sky";
  // project Andromeda / the Milky Way to the screen with the same camera the 3D uses
  let m31px = [540, 760], mwpx = [300, 1200];
  if (sim) {
    const pc = new THREE.PerspectiveCamera(50, 1080 / 1920, 0.01, 2000); cameraFor(f, sim, pc);
    const c0 = coreAt(sim, s.t, 0), c1 = coreAt(sim, s.t, 1), d = [c1[0] - c0[0], c1[1] - c0[1], c1[2] - c0[2]], dl = Math.hypot(d[0], d[1], d[2]) || 1, sh = s.shift ?? 0;
    const m = toScreen(pc, [c1[0] + d[0] / dl * sh, c1[1] + d[1] / dl * sh, c1[2] + d[2] / dl * sh]); m31px = [m[0], m[1]];
    const w = toScreen(pc, c0); mwpx = [w[0], w[1]];
  }
  const dip = Math.max(...[B[1], B[3], T.skyIn, B[5], B[6], B[7]].map(c => sat(1 - Math.abs(f - c) / 4)));
  const years = b === 2 ? `+${(4 * sat(lf / (B[3] - B[2]))).toFixed(1)} BILLION YEARS` : b === 1 ? "2.5 MILLION LIGHT-YEARS AWAY · 400,000 km/h" : "";
  return (
    <AbsoluteFill style={{ backgroundColor: "#010106" }}>
      {sim && <ThreeCanvas width={1080} height={1920} dpr={1} camera={{ fov: 50, position: [0, 0, 10] }} gl={{ antialias: true }}>
        <World f={f} sim={sim} />
        <Post />
      </ThreeCanvas>}
      {sky && <Silhouette glow={1} />}
      {b === 1 && <div style={{ position: "absolute", left: m31px[0] - 90, top: m31px[1] - 90, width: 180, height: 180, borderRadius: "50%", border: "4px solid rgba(158,200,255,.9)", opacity: sat((lf - 30) / 15) }}>
        <div style={{ position: "absolute", top: 196, left: -160, width: 500, textAlign: "center", fontFamily: "Inter", fontWeight: 900, fontSize: 40, color: "#9ec8ff", textShadow: sh }}>ANDROMEDA</div>
      </div>}
      {b === 6 && <Futures k={sat((lf - 40) / 120)} from={m31px} to={mwpx} />}
      {b === 6 && lf > 120 && <div style={{ position: "absolute", top: 1180, width: "100%", textAlign: "center", fontFamily: "Inter", fontWeight: 900, fontSize: 64, textShadow: sh }}>
        <span style={{ color: "#ff6a6a" }}>50% HIT</span><span style={{ color: "#fff" }}> · </span><span style={{ color: "#6aa8ff" }}>50% MISS</span></div>}
      <AbsoluteFill style={{ background: `rgba(0,0,0,${dip})` }} />
      <AbsoluteFill style={{ fontFamily: "Inter", alignItems: "center", textAlign: "center", color: "#fff" }}>
        <div style={{ transform: `scale(${pop})`, marginTop: 190, fontWeight: 900, fontSize: 84, lineHeight: 1.0, letterSpacing: -2, textShadow: sh, opacity: inT * outT }}>{l1}</div>
        <div style={{ transform: `scale(${pop})`, fontWeight: 900, fontSize: l2.length > 18 ? 66 : 96, lineHeight: 1.05, letterSpacing: -1, color: ACC[b], textShadow: sh, opacity: inT * outT, padding: "0 40px" }}>{l2}</div>
        {years && <div style={{ marginTop: 18, fontWeight: 800, fontSize: 38, color: "#cfe0ff", textShadow: sh, opacity: inT * outT, letterSpacing: 1 }}>{years}</div>}
      </AbsoluteFill>
      <Captions f={f} words={WORDS} top={sky ? 1180 : 1420} accent={ACC[b] === "#fff" ? "#ffd36a" : ACC[b]} size={84} />
      {withAudio && <Audio src={staticFile("mix.wav")} />}
    </AbsoluteFill>
  );
};
