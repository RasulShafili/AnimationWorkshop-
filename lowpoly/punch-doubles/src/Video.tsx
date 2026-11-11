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
const ACC = ["#ffd36a", "#ffd36a", "#ffb04a", "#ff9a3a", "#ff8a3a", "#ff6a3a", "#ff5a3a", "#ff7a4a", "#ff4a3a", "#ff3a3a", "#ffd36a"];
const clockAt = (f: number) => { const K = T.clock as number[][]; for (let i = 0; i < K.length - 1; i++) if (f < K[i + 1][0]) return K[i][1] + (K[i + 1][1] - K[i][1]) * (f - K[i][0]) / (K[i + 1][0] - K[i][0]); return K[K.length - 1][1]; };
const mmss = (s: number) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}`;
const big = (n: number) => (BigInt(2) ** BigInt(n)).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");

export const Video: React.FC<{ withAudio?: boolean }> = ({ withAudio = true }) => {
  const f = useCurrentFrame();
  const glb = useGLBs(["man.glb"]);
  const [h] = useState(() => delayRender("fonts"));
  useEffect(() => { Promise.all([document.fonts.load("900 80px Inter"), document.fonts.load("800 40px Inter")]).then(() => continueRender(h)); }, [h]);
  const b = beatOf(f), lf = f - B[b], [l1, l2] = T.texts[b];
  const inT = b === 0 ? 1 : interpolate(lf, [2, 12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const outT = b === B.length - 2 ? 1 : interpolate(B[b + 1] - f, [0, 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const fl = (x: number, d = 12) => (f >= x && f < x + d ? 1 - (f - x) / d : 0);
  const flash = Math.max(...T.hits.map((x, i) => fl(x, 4 + i) * Math.min(1, 0.15 + i * 0.12)), fl(T.beamOut + 6, 14), fl(T.hits[9] + 6, 16));
  const rew = false;
  const dip = Math.max(...B.slice(1, 10).map(c => sat(1 - Math.abs(f - c) / 3)));
  const sec = clockAt(f), n = Math.floor(sec / 2), over = sec >= 180;
  const num = big(n), fs = Math.min(64, 1500 / Math.max(8, num.length + 1));
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {glb && <ThreeCanvas width={1080} height={1920} dpr={1} camera={{ fov: 50, position: [0, 10, 60] }} gl={{ antialias: true }}>
        <World f={f} glb={glb} />
        <Post />
      </ThreeCanvas>}
      {rew && <AbsoluteFill style={{ background: "repeating-linear-gradient(0deg, rgba(255,255,255,.07) 0 3px, transparent 3px 14px)" }} />}
      {rew && <div style={{ position: "absolute", top: 230, left: 70, fontFamily: "Inter", fontWeight: 900, fontSize: 110, color: "#fff", textShadow: sh }}>◀◀ REWIND</div>}
      <AbsoluteFill style={{ background: `rgba(255,248,235,${flash})` }} />
      <AbsoluteFill style={{ background: `rgba(0,0,0,${dip})` }} />
      {!rew && <AbsoluteFill style={{ fontFamily: "Inter", alignItems: "center", textAlign: "center", color: "#fff" }}>
        <div style={{ marginTop: 210, fontWeight: 900, fontSize: b >= 1 && b <= 9 ? 120 : 92, lineHeight: 1.0, letterSpacing: -2, textShadow: sh, opacity: inT * outT }}>{l1}</div>
        <div style={{ fontWeight: 900, fontSize: l2.length > 16 ? 76 : 104, lineHeight: 1.05, letterSpacing: -1, color: ACC[b], textShadow: sh, opacity: inT * outT, padding: "0 40px" }}>{l2}</div>
      </AbsoluteFill>}
      {/* round clock + punch multiplier HUD */}
      <div style={{ position: "absolute", bottom: 250, width: "100%", textAlign: "center", fontFamily: "Inter", textShadow: sh, color: "#fff" }}>
        <div style={{ display: "inline-block", padding: "10px 34px", borderRadius: 18, background: over ? "rgba(200,20,20,.85)" : "rgba(10,10,20,.7)", border: `3px solid ${over ? "#ff8a8a" : "#ffd36a"}` }}>
          <span style={{ fontWeight: 800, fontSize: 40, opacity: .85 }}>ROUND 1&nbsp;&nbsp;</span>
          <span style={{ fontWeight: 900, fontSize: 72, fontVariantNumeric: "tabular-nums" }}>{mmss(sec)}</span>
        </div>
        <div style={{ margin: "16px auto 0", width: "fit-content", maxWidth: 1020, padding: "8px 26px 12px", borderRadius: 16, background: "rgba(10,10,20,.62)" }}>
          <div style={{ fontWeight: 800, fontSize: 36, opacity: .9 }}>PUNCH POWER</div>
          <div style={{ fontWeight: 900, fontSize: fs, color: "#ffd36a", fontVariantNumeric: "tabular-nums", wordBreak: "break-all" }}>×{num}</div>
        </div>
      </div>
      {withAudio && <Audio src={staticFile("mix.wav")} />}
    </AbsoluteFill>
  );
};
