import React, { useEffect, useState } from "react";
import { AbsoluteFill, Audio, staticFile, useCurrentFrame, delayRender, continueRender, interpolate, Easing } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import "@fontsource/inter/800.css";
import "@fontsource/inter/900.css";
import { World } from "./World";
import { Post } from "./Post";
import T from "./timeline.json";

const B = T.beats;
const beatOf = (f: number) => { let i = 0; while (i < B.length - 2 && f >= B[i + 1]) i++; return i; };
const shadow = "0 4px 0 rgba(20,14,40,.55), 0 10px 30px rgba(20,14,40,.45)";
const ACC = ["#ffb347", "#9fe0ff", "#ff7a3a", "#e0905a", "#7ff0c0", "#ffd36a"];

export const Video: React.FC<{ withAudio?: boolean }> = ({ withAudio = true }) => {
  const f = useCurrentFrame();
  const [h] = useState(() => delayRender("fonts"));
  useEffect(() => { Promise.all([document.fonts.load("900 80px Inter"), document.fonts.load("800 40px Inter")]).then(() => continueRender(h)); }, [h]);
  const bi = beatOf(f), lf = f - B[bi], [l1, l2] = T.texts[bi];
  const inT = bi === 0 ? 1 : interpolate(lf, [2, 12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const outT = bi === B.length - 2 ? 1 : interpolate(B[bi + 1] - f, [0, 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const o = inT * outT;
  const o2 = Math.round(interpolate(f, T.gauge, [21, 42], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) }));
  const chipPop = interpolate(f, [T.gauge[1], T.gauge[1] + 6, T.gauge[1] + 14], [1, 1.25, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const flash = f >= T.strike && f < T.strike + 6 ? ((f - T.strike) % 2 === 0 ? 0.55 : 0.2) : 0;
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <ThreeCanvas width={1080} height={1920} shadows dpr={1} camera={{ fov: 34, position: [10, 8, 10] }} gl={{ antialias: true }}>
        <World f={f} />
        <Post />
      </ThreeCanvas>
      <AbsoluteFill style={{ background: `rgba(235,240,255,${flash})` }} />
      <AbsoluteFill style={{ fontFamily: "Inter", alignItems: "center", textAlign: "center", color: "#fff" }}>
        <div style={{ marginTop: 200, display: "flex", alignItems: "center", gap: 14, padding: "12px 30px", borderRadius: 60, background: "rgba(20,16,40,.55)", fontWeight: 800, fontSize: 44, letterSpacing: 2, transform: `scale(${chipPop})` }}>
          <span style={{ color: "#9fe0ff" }}>O₂</span><span style={{ color: o2 > 21 ? "#ffb347" : "#fff" }}>{o2}%</span>
        </div>
        <div style={{ marginTop: 34, fontWeight: 900, fontSize: 108, lineHeight: 1.0, letterSpacing: -2, textShadow: shadow, opacity: o, transform: `translateY(${(1 - inT) * 30}px)` }}>{l1}</div>
        <div style={{ fontWeight: 900, fontSize: bi === 0 ? 150 : 108, lineHeight: 1.0, letterSpacing: -2, color: ACC[bi], textShadow: shadow, opacity: o, transform: `translateY(${(1 - inT) * 40}px)` }}>{l2}</div>
      </AbsoluteFill>
      {bi === 4 && f > T.fly[0] + 40 && (
        <div style={{ position: "absolute", width: "100%", bottom: 420, textAlign: "center", fontFamily: "Inter", fontWeight: 800, color: "#fff", textShadow: shadow, opacity: interpolate(f, [T.fly[0] + 40, T.fly[0] + 52], [0, 1], { extrapolateRight: "clamp" }) }}>
          <div style={{ fontSize: 64, color: "#7ff0c0" }}>70 CM WINGS</div>
          <div style={{ fontSize: 40 }}>DRAGONFLIES, 300 MILLION YEARS AGO</div>
        </div>
      )}
      {withAudio && <Audio src={staticFile("mix.wav")} />}
    </AbsoluteFill>
  );
};
