import React, { useEffect, useState } from "react";
import { AbsoluteFill, Audio, staticFile, useCurrentFrame, delayRender, continueRender, interpolate, Easing } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import "@fontsource/inter/800.css";
import "@fontsource/inter/900.css";
import { World, beatOf } from "./World";
import { Post } from "./Post";
import { Captions } from "./Captions";
import T from "./timeline.json";
import WORDS from "./words.json";

const B = T.beats;
const sat = (v: number) => Math.min(1, Math.max(0, v));
const sh = "0 4px 0 rgba(10,8,30,.6), 0 10px 30px rgba(10,8,30,.55)";
const ACC = ["#ffd36a", "#8ab8ff", "#ffd36a", "#fff", "#ff9a3a", "#7dff6a", "#7dff6a", "#ffd36a"];

export const Video: React.FC<{ withAudio?: boolean }> = ({ withAudio = true }) => {
  const f = useCurrentFrame();
  const [h] = useState(() => delayRender("fonts"));
  useEffect(() => { Promise.all([document.fonts.load("900 80px Inter"), document.fonts.load("800 40px Inter")]).then(() => continueRender(h)); }, [h]);
  const b = beatOf(f), lf = f - B[b], [l1, l2] = T.texts[b];
  const inT = b === 0 ? 1 : interpolate(lf, [2, 10], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const outT = b === B.length - 2 ? 1 : interpolate(B[b + 1] - f, [0, 5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const pop = b === 0 ? 1 : 1 + 0.25 * Math.exp(-Math.max(0, lf - 2) / 4);
  const fl = (x: number, d = 12) => (f >= x && f < x + d ? 1 - (f - x) / d : 0);
  const flash = Math.max(fl(T.boom, 22), fl(T.rainCut, 6) * 0.3);
  const dip = Math.max(...[B[1], B[2], B[3] - 1, B[4], B[5], T.rainCut, T.finalAerial].map(c => sat(1 - Math.abs(f - c) / 3)));
  // targeting reticle on the eye in the hook
  const ret = b === 0 ? 1 - sat((f - 80) / 10) : 0, rs = 1 + 0.6 * (1 - ease(Math.min(1, f / 50)));
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <ThreeCanvas width={1080} height={1920} dpr={1} camera={{ fov: 50, position: [0, 10, 60] }} gl={{ antialias: true }}>
        <World f={f} />
        <Post />
      </ThreeCanvas>
      {ret > 0 && <div style={{ position: "absolute", left: 540 - 150 * rs, top: 960 - 150 * rs, width: 300 * rs, height: 300 * rs, border: "6px solid #ff3a3a", borderRadius: "50%", opacity: ret, boxShadow: "0 0 30px rgba(255,40,40,.6)" }}>
        <div style={{ position: "absolute", left: "50%", top: -40, bottom: -40, width: 5, background: "#ff3a3a", transform: "translateX(-50%)" }} />
        <div style={{ position: "absolute", top: "50%", left: -40, right: -40, height: 5, background: "#ff3a3a", transform: "translateY(-50%)" }} />
        <div style={{ position: "absolute", top: "105%", width: "100%", textAlign: "center", fontFamily: "Inter", fontWeight: 900, fontSize: 40, color: "#ff5a5a", textShadow: sh, marginTop: 40 }}>TARGET: EYE</div>
      </div>}
      <AbsoluteFill style={{ background: `rgba(255,248,235,${flash})` }} />
      <AbsoluteFill style={{ background: `rgba(0,0,0,${dip})` }} />
      <AbsoluteFill style={{ fontFamily: "Inter", alignItems: "center", textAlign: "center", color: "#fff" }}>
        <div style={{ transform: `scale(${pop})`, marginTop: 200, fontWeight: 900, fontSize: 92, lineHeight: 1.0, letterSpacing: -2, textShadow: sh, opacity: inT * outT }}>{l1}</div>
        <div style={{ transform: `scale(${pop})`, fontWeight: 900, fontSize: l2.length > 15 ? 76 : 104, lineHeight: 1.05, letterSpacing: -1, color: ACC[b], textShadow: sh, opacity: inT * outT, padding: "0 40px" }}>{l2}</div>
      </AbsoluteFill>
      <Captions f={f} words={WORDS} top={1330} accent={b >= 5 && b <= 6 ? "#7dff6a" : "#ffd36a"} />
      {b === 7 && f > 900 && <div style={{ position: "absolute", bottom: 300, width: "100%", display: "flex", justifyContent: "center", gap: 40, fontFamily: "Inter", fontWeight: 900, fontSize: 96 }}>
        <span style={{ padding: "10px 46px", borderRadius: 24, background: "#2ac46a", color: "#fff", textShadow: sh, transform: `scale(${1 + 0.06 * Math.sin(f * 0.25)})` }}>YES</span>
        <span style={{ padding: "10px 46px", borderRadius: 24, background: "#e8443a", color: "#fff", textShadow: sh, transform: `scale(${1 + 0.06 * Math.sin(f * 0.25 + 1.6)})` }}>NO</span>
      </div>}
      {withAudio && <Audio src={staticFile("mix.wav")} />}
    </AbsoluteFill>
  );
};
const ease = (t: number) => { t = sat(t); return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
