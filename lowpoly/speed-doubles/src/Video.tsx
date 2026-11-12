import React, { useEffect, useState } from "react";
import { AbsoluteFill, Audio, staticFile, useCurrentFrame, delayRender, continueRender, interpolate, Easing } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import "@fontsource/inter/800.css";
import "@fontsource/inter/900.css";
import { World, beatOf } from "./World";
import { Post } from "./Post";
import { useGLBs } from "./glb";
import T from "./timeline.json";

const B = T.beats;
const sat = (v: number) => Math.min(1, Math.max(0, v));
const sh = "0 4px 0 rgba(10,8,30,.6), 0 10px 30px rgba(10,8,30,.55)";
const ACC = ["#ffd36a", "#7ff0c0", "#7ff0c0", "#ffd36a", "#ffffff", "#ff9a3a", "#ff5a2a", "#8ab8ff", "#c8d0e0", "#ff4a4a", "#7ff0c0"];
const clockAt = (f: number) => { const K = T.clock as number[][]; for (let i = 0; i < K.length - 1; i++) if (f < K[i + 1][0]) return K[i][1] + (K[i + 1][1] - K[i][1]) * (f - K[i][0]) / (K[i + 1][0] - K[i][0]); return K[K.length - 1][1]; };
const mmss = (s: number) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}`;
const fmt = (n: number) => Math.round(n).toLocaleString("en-US");
const C_KMH = 1079252849;

export const Video: React.FC<{ withAudio?: boolean }> = ({ withAudio = true }) => {
  const f = useCurrentFrame();
  const glb = useGLBs(["man.glb"]);
  const [h] = useState(() => delayRender("fonts"));
  useEffect(() => { Promise.all([document.fonts.load("900 80px Inter"), document.fonts.load("800 40px Inter")]).then(() => continueRender(h)); }, [h]);
  const b = beatOf(f), lf = f - B[b], [l1, l2] = T.texts[b];
  const inT = b === 0 ? 1 : interpolate(lf, [2, 10], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const outT = b === B.length - 2 ? 1 : interpolate(B[b + 1] - f, [0, 5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const pop = b === 0 ? 1 : 1 + 0.28 * Math.exp(-Math.max(0, lf - 2) / 4);
  const fl = (x: number, d = 12) => (f >= x && f < x + d ? 1 - (f - x) / d : 0);
  const flash = Math.max(fl(T.boom, 10) * 0.9, fl(T.orbit, 10) * 0.6, fl(B[9], 14) * 0.8, ...B.slice(1, 7).map(x => fl(x, 5) * 0.25));
  const dip = Math.max(...[B[7], B[8], B[9]].map(c => sat(1 - Math.abs(f - c) / 3)));
  const sec = clockAt(f), kmh = Math.min(C_KMH, 18 * Math.pow(2, sec / 2)), mach = kmh / 1235;
  const light = kmh >= C_KMH * 0.999;
  const pulse = 1 + 0.3 * Math.exp(-lf / 5) * (b >= 1 ? 1 : 0);
  const sub = light ? "= SPEED OF LIGHT" : mach >= 1 && b < 7 ? `MACH ${mach < 10 ? mach.toFixed(1) : fmt(mach)}` : "";
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {glb && <ThreeCanvas width={1080} height={1920} dpr={1} camera={{ fov: 50, position: [0, 10, 60] }} gl={{ antialias: true }}>
        <World f={f} glb={glb} />
        <Post />
      </ThreeCanvas>}
      <AbsoluteFill style={{ background: `rgba(255,248,235,${flash})` }} />
      <AbsoluteFill style={{ background: `rgba(0,0,0,${dip})` }} />
      <AbsoluteFill style={{ fontFamily: "Inter", alignItems: "center", textAlign: "center", color: "#fff" }}>
        <div style={{ transform: `scale(${pop})`, marginTop: 210, fontWeight: 900, fontSize: b >= 1 && b <= 9 ? (l1.length > 8 ? 76 : 120) : 92, lineHeight: 1.0, letterSpacing: -2, textShadow: sh, opacity: inT * outT }}>{l1}</div>
        <div style={{ transform: `scale(${pop})`, fontWeight: 900, fontSize: l2.length > 22 ? 64 : l2.length > 16 ? 76 : 104, lineHeight: 1.05, letterSpacing: -1, color: ACC[b], textShadow: sh, opacity: inT * outT, padding: "0 40px" }}>{l2}</div>
      </AbsoluteFill>
      <div style={{ position: "absolute", bottom: 250, width: "100%", textAlign: "center", fontFamily: "Inter", textShadow: sh, color: "#fff" }}>
        <div style={{ display: "inline-block", padding: "10px 30px", borderRadius: 18, background: "rgba(10,10,20,.7)", border: `3px solid ${b >= 5 && b <= 7 ? "#ff8a5a" : "#7ff0c0"}` }}>
          <span style={{ fontWeight: 900, fontSize: 64, fontVariantNumeric: "tabular-nums" }}>{mmss(sec)}</span>
          <span style={{ fontWeight: 900, fontSize: 40, marginLeft: 26, color: "#7ff0c0" }}>LEVEL {Math.min(10, b + 1)}/10</span>
        </div>
        <div style={{ margin: "16px auto 0", width: "fit-content", maxWidth: 1020, padding: "8px 30px 12px", borderRadius: 16, background: "rgba(10,10,20,.62)" }}>
          <div style={{ fontWeight: 800, fontSize: 36, opacity: .9 }}>YOUR SPEED</div>
          <div style={{ fontWeight: 900, fontSize: 78, color: lf < 4 && b >= 1 ? "#ffffff" : "#ffd36a", fontVariantNumeric: "tabular-nums", transform: `scale(${pulse})` }}>{fmt(kmh)} km/h</div>
          {sub && <div style={{ fontWeight: 900, fontSize: 40, color: light ? "#ff6a6a" : "#8ab8ff" }}>{sub}</div>}
        </div>
      </div>
      {withAudio && <Audio src={staticFile("mix.wav")} />}
    </AbsoluteFill>
  );
};
