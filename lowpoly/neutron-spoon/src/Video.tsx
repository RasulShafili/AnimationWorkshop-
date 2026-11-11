import React, { useEffect, useState } from "react";
import { AbsoluteFill, Audio, staticFile, useCurrentFrame, delayRender, continueRender, interpolate, Easing } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import "@fontsource/inter/800.css";
import "@fontsource/inter/900.css";
import { World, beatOf } from "./World";
import { Post } from "./Post";
import T from "./timeline.json";

const B = T.beats;
const sat = (v: number) => Math.min(1, Math.max(0, v));
const sh = "0 4px 0 rgba(10,8,30,.6), 0 10px 30px rgba(10,8,30,.55)";
const ACC = ["#8ab8ff", "#fff", "#8ab8ff", "#ffd36a", "#7ff0c0", "#ff6a3a", "#8ab8ff"];

export const Video: React.FC<{ withAudio?: boolean }> = ({ withAudio = true }) => {
  const f = useCurrentFrame();
  const [h] = useState(() => delayRender("fonts"));
  useEffect(() => { Promise.all([document.fonts.load("900 80px Inter"), document.fonts.load("800 40px Inter")]).then(() => continueRender(h)); }, [h]);
  const b = beatOf(f), lf = f - B[b], [l1, l2] = T.texts[b];
  const inT = b === 0 ? sat((f - T.boom - 2) / 6) : interpolate(lf, [2, 12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const outT = b === B.length - 2 ? 1 : interpolate(B[b + 1] - f, [0, 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const flash = Math.max(...[T.boom, T.boom2].map(x => (f >= x && f < x + 14 ? 1 - (f - x) / 14 : 0)), f >= T.collapse + 8 && f < T.collapse + 16 ? 1 - (f - T.collapse - 8) / 8 : 0);
  const rew = b === 1;
  const dip = Math.max(...[B[2], B[3], B[4], B[5], B[6]].map(c => sat(1 - Math.abs(f - c) / 5)), sat((f - (T.total - 10)) / 10));
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <ThreeCanvas width={1080} height={1920} dpr={1} camera={{ fov: 50, position: [0, 10, 60] }} gl={{ antialias: true }}>
        <World f={f} />
        <Post />
      </ThreeCanvas>
      {rew && <AbsoluteFill style={{ background: "repeating-linear-gradient(0deg, rgba(255,255,255,.07) 0 3px, transparent 3px 14px)", filter: "contrast(1.2)" }} />}
      {rew && <div style={{ position: "absolute", top: 230, left: 70, fontFamily: "Inter", fontWeight: 900, fontSize: 110, color: "#fff", textShadow: sh }}>◀◀ REWIND</div>}
      <AbsoluteFill style={{ background: `rgba(255,248,235,${flash})` }} />
      <AbsoluteFill style={{ background: `rgba(0,0,0,${dip})` }} />
      {!rew && <AbsoluteFill style={{ fontFamily: "Inter", alignItems: "center", textAlign: "center", color: "#fff" }}>
        <div style={{ marginTop: 220, fontWeight: 900, fontSize: 100, lineHeight: 1.0, letterSpacing: -2, textShadow: sh, opacity: inT * outT }}>{l1}</div>
        <div style={{ fontWeight: 900, fontSize: b === 2 || b === 3 ? 84 : 120, lineHeight: 1.05, letterSpacing: -1, color: ACC[b], textShadow: sh, opacity: inT * outT }}>{l2}</div>
      </AbsoluteFill>}
      {b === 2 && f > T.collapse + 60 && <Tag top={1430} big="20 KM WIDE" small="MASS: 1.4 SUNS" color="#8ab8ff" />}
      {b === 3 && lf > 60 && <Tag top={1430} big="≈ 500 MILLION TONS" small="IN ONE TEASPOON" color="#ffd36a" />}
      {b === 5 && f > T.boom2 + 100 && <Tag top={1430} big="≈ 4,000×" small="THE DINOSAUR-KILLING ASTEROID" color="#ff6a3a" />}
      {withAudio && <Audio src={staticFile("mix.wav")} />}
    </AbsoluteFill>
  );
};
const Tag: React.FC<{ top: number; big: string; small: string; color: string }> = ({ top, big, small, color }) => (
  <div style={{ position: "absolute", top, width: "100%", textAlign: "center", fontFamily: "Inter", textShadow: sh }}>
    <div style={{ fontWeight: 900, fontSize: 104, color, lineHeight: 1 }}>{big}</div>
    <div style={{ fontWeight: 800, fontSize: 40, color: "#fff", marginTop: 6 }}>{small}</div>
  </div>
);
