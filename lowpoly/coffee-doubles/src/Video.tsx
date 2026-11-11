import React, { useEffect, useState } from "react";
import { AbsoluteFill, Audio, staticFile, useCurrentFrame, delayRender, continueRender, interpolate, Easing } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import "@fontsource/inter/800.css";
import "@fontsource/inter/900.css";
import { World, beatOf, cupsAt, bpmAt, sat } from "./World";
import { Post } from "./Post";
import T from "./timeline.json";

const B = T.beats;
const sh = "0 4px 0 rgba(30,14,6,.6), 0 10px 30px rgba(30,14,6,.55)";
const ACC = ["#ffc06a", "#7ff0c0", "#ffd36a", "#ff8a4a", "#ff4a4a", "#7aa8ff", "#ffc06a"];

export const Video: React.FC<{ withAudio?: boolean }> = ({ withAudio = true }) => {
  const f = useCurrentFrame();
  const [h] = useState(() => delayRender("fonts"));
  useEffect(() => { Promise.all([document.fonts.load("900 80px Inter"), document.fonts.load("800 40px Inter")]).then(() => continueRender(h)); }, [h]);
  const b = beatOf(f), lf = f - B[b], [l1, l2] = T.texts[b];
  const inT = b === 0 ? 1 : interpolate(lf, [2, 12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const outT = b === B.length - 2 ? 1 : interpolate(B[b + 1] - f, [0, 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const cups = Math.max(1, cupsAt(f)), mg = cups * 95, bpm = bpmAt(f), lastCup = Math.max(...T.cupsAt.filter(a => f >= a), -99);
  const pop = f - lastCup < 8 ? 1 + 0.25 * (1 - (f - lastCup) / 8) : 1;
  const inSyn = f >= B[5] && f < T.crash;
  const dip = Math.max(...[B[1], B[2], B[3], B[4]].map(c => sat(1 - Math.abs(f - c) / 4) * 0.6), sat(1 - Math.abs(f - B[5]) / 5), sat(1 - Math.abs(f - T.crash) / 5), sat((f - (T.total - 12)) / 10), sat(1 - f / 5));
  const red = b === 3 ? 0.35 + 0.15 * Math.sin(f * 0.5) : b === 4 ? 0.55 + 0.25 * Math.sin(f * 0.9) : 0;
  const flood = sat((f - T.release - 8) / 22);
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <ThreeCanvas width={1080} height={1920} shadows dpr={1} camera={{ fov: 52, position: [0, 1.2, 0.7] }} gl={{ antialias: true }}>
        <World f={f} />
        <Post />
      </ThreeCanvas>
      <AbsoluteFill style={{ background: `radial-gradient(ellipse at center, rgba(0,0,0,0) 45%, rgba(200,10,20,${red}) 100%)` }} />
      {f >= T.crash && <AbsoluteFill style={{ background: `radial-gradient(ellipse at center, rgba(0,0,0,0) 30%, rgba(0,0,0,${0.75 * sat((f - T.crash) / 30)}) 85%)` }} />}
      <AbsoluteFill style={{ background: `rgba(0,0,0,${dip})` }} />
      <AbsoluteFill style={{ fontFamily: "Inter", alignItems: "center", textAlign: "center", color: "#fff" }}>
        <div style={{ marginTop: 190, padding: "12px 32px", borderRadius: 60, background: "rgba(40,20,10,.65)", fontWeight: 800, fontSize: 44, letterSpacing: 2, transform: `scale(${inSyn ? 1 : pop})` }}>
          <span style={{ color: "#ffc06a" }}>☕ ×{cups}</span><span style={{ color: mg > 400 ? "#ff5a5a" : "#fff" }}>{"  ·  "}{mg} mg</span>
        </div>
        <div style={{ marginTop: 30, fontWeight: 900, fontSize: b === 5 || b === 0 || b === 6 ? 84 : 104, lineHeight: 1.0, letterSpacing: -2, textShadow: sh, opacity: inT * outT, transform: `translateY(${(1 - inT) * 30}px)` }}>{l1}</div>
        <div style={{ fontWeight: 900, fontSize: b === 5 || b === 0 || b === 6 ? 88 : 116, lineHeight: 1.05, letterSpacing: -1, color: ACC[b], textShadow: sh, opacity: inT * outT, transform: `translateY(${(1 - inT) * 40}px)` }}>{l2}</div>
      </AbsoluteFill>
      {!inSyn && f < T.crash && b >= 1 && (
        <div style={{ position: "absolute", right: 60, top: 610, padding: "8px 24px", borderRadius: 40, background: "rgba(40,10,10,.55)", fontFamily: "Inter", fontWeight: 900, fontSize: 58, color: bpm > 130 ? "#ff4a4a" : bpm > 95 ? "#ffb347" : "#ffffff", textShadow: sh }}>
          ♥ {bpm} <span style={{ fontSize: 34, fontWeight: 800 }}>BPM</span>
        </div>
      )}
      {b === 2 && lf > 40 && <Tag top={1560} big="400 mg" small="THE DAILY SAFE LIMIT" color="#ffd36a" />}
      {b === 4 && lf > 30 && <Tag top={1560} big="1,520 mg" small="SEIZURE RISK FROM ~1,200 mg" color="#ff4a4a" />}
      {inSyn && (
        <>
          {f - B[5] > 18 && <Tag top={640} big="" small="ADENOSINE = YOUR 'I'M TIRED' SIGNAL" color="#7aa8ff" />}
          {f - B[5] > 40 && f < T.release && <Tag top={1540} big="BLOCKED" small="BY CAFFEINE · TIREDNESS PILES UP" color="#c8803a" />}
          {f >= T.release + 6 && <Tag top={1540} big="ALL AT ONCE" small="THE CAFFEINE CRASH" color="#7aa8ff" />}
        </>
      )}
      {f >= T.crash + 20 && b === 5 && <Tag top={1500} big="CRASH" small="" color="#ff7a7a" />}
      {withAudio && <Audio src={staticFile("mix.wav")} />}
    </AbsoluteFill>
  );
};
const Tag: React.FC<{ top: number; big: string; small: string; color: string }> = ({ top, big, small, color }) => (
  <div style={{ position: "absolute", top, width: "100%", textAlign: "center", fontFamily: "Inter", textShadow: sh }}>
    {big && <div style={{ fontWeight: 900, fontSize: 120, color, lineHeight: 1 }}>{big}</div>}
    {small && <div style={{ fontWeight: 800, fontSize: 40, color: big ? "#fff" : color, marginTop: 6 }}>{small}</div>}
  </div>
);
