import React, { useEffect, useState } from "react";
import { AbsoluteFill, Audio, staticFile, useCurrentFrame, delayRender, continueRender, interpolate, Easing } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import "@fontsource/inter/800.css";
import "@fontsource/inter/900.css";
import { World, sceneOf, bpmAt } from "./World";
import { Post } from "./Post";
import { useGLBs } from "./glb";
import T from "./timeline.json";

const B = T.beats;
const beatOf = (f: number) => { let i = 0; while (i < B.length - 2 && f >= B[i + 1]) i++; return i; };
const sh = "0 4px 0 rgba(20,10,30,.55), 0 10px 30px rgba(20,10,30,.5)";
const ACC = ["#ffb347", "#ff6a4a", "#ffd36a", "#ff5a6a", "#ff7ac8", "#9fe0ff"];
const fmt = (n: number) => n.toLocaleString("en-US");

export const Video: React.FC<{ withAudio?: boolean }> = ({ withAudio = true }) => {
  const f = useCurrentFrame();
  const [h] = useState(() => delayRender("fonts"));
  useEffect(() => { Promise.all([document.fonts.load("900 80px Inter"), document.fonts.load("800 40px Inter")]).then(() => continueRender(h)); }, [h]);
  const d = useGLBs(["man.glb"]);
  const bi = beatOf(f), lf = f - B[bi], [l1, l2] = T.texts[bi];
  const inT = bi === 0 ? 1 : interpolate(lf, [2, 12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const outT = bi === B.length - 2 ? 1 : interpolate(B[bi + 1] - f, [0, 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const o = inT * outT;
  const k = Math.floor(f / T.every), level = Math.pow(2, k), since = f % T.every;
  const pop = since < 8 && k > 0 ? 1 + 0.22 * (1 - since / 8) : 1;
  const sc = sceneOf(f);
  // a quick dip to black on the cuts into and out of the body
  const cuts = [B[3], T.heart, T.molecules[0], T.molecules[1]];
  const dip = Math.max(...cuts.map(c => sat(1 - Math.abs(f - c) / 5)));
  const hct = Math.round(interpolate(f, [B[3], T.heart], [45, 68], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {d && <ThreeCanvas width={1080} height={1920} shadows dpr={1} camera={{ fov: 34, position: [1, 1, 4] }} gl={{ antialias: true }}>
        <World f={f} g={d["man.glb"]} />
        <Post />
      </ThreeCanvas>}
      <AbsoluteFill style={{ background: `rgba(0,0,0,${dip})` }} />
      <AbsoluteFill style={{ fontFamily: "Inter", alignItems: "center", textAlign: "center", color: "#fff" }}>
        <div style={{ marginTop: 190, display: "flex", alignItems: "center", gap: 16, padding: "12px 30px", borderRadius: 60, background: "rgba(20,12,30,.6)", fontWeight: 800, fontSize: 40, letterSpacing: 2, transform: `scale(${pop})` }}>
          <span style={{ color: "#9fd0ff" }}>TESTOSTERONE</span><span style={{ color: k > 7 ? "#ff5a5a" : "#ffb347" }}>×{fmt(level)}</span>
          <div style={{ width: 70, height: 10, borderRadius: 5, background: "rgba(255,255,255,.2)", overflow: "hidden" }}><div style={{ width: `${since / T.every * 100}%`, height: "100%", background: "#ffb347" }} /></div>
        </div>
        <div style={{ marginTop: 30, fontWeight: 900, fontSize: 100, lineHeight: 1.0, letterSpacing: -2, textShadow: sh, opacity: o, transform: `translateY(${(1 - inT) * 30}px)` }}>{l1}</div>
        <div style={{ fontWeight: 900, fontSize: bi === 0 ? 76 : bi === 4 ? 84 : 112, lineHeight: 1.05, letterSpacing: -1, color: ACC[bi], textShadow: sh, opacity: o, transform: `translateY(${(1 - inT) * 40}px)` }}>{l2}</div>
      </AbsoluteFill>
      {sc === "vessel" && <Label top={1420} big={`${hct}%`} small="HEMATOCRIT · NORMAL ≈ 45%" color={hct > 54 ? "#ff5a6a" : "#ffd36a"} />}
      {sc === "heart" && <Label top={1420} big={`♥ ${bpmAt(f)}`} small="BEATS PER MINUTE" color="#ff5a6a" />}
      {sc === "molecules" && (
        <>
          <Tag top={560} text="TESTOSTERONE" color="#6ab8ff" />
          <Tag top={1000} text="AROMATASE" color="#c89aff" left={640} />
          <Tag top={1500} text="ESTROGEN" color="#ff7ac8" />
        </>
      )}
      {bi === 0 && <div style={{ position: "absolute", bottom: 300, width: "100%", textAlign: "center", fontFamily: "Inter", fontWeight: 800, fontSize: 30, color: "rgba(255,255,255,.75)", textShadow: sh }}>EFFECTS SPED UP FOR THE VIDEO</div>}
      {withAudio && <Audio src={staticFile("mix.wav")} />}
    </AbsoluteFill>
  );
};
const sat = (v: number) => Math.min(1, Math.max(0, v));
const Label: React.FC<{ top: number; big: string; small: string; color: string }> = ({ top, big, small, color }) => (
  <div style={{ position: "absolute", top, width: "100%", textAlign: "center", fontFamily: "Inter", textShadow: sh }}>
    <div style={{ fontWeight: 900, fontSize: 150, color, lineHeight: 1 }}>{big}</div>
    <div style={{ fontWeight: 800, fontSize: 40, color: "#fff" }}>{small}</div>
  </div>
);
const Tag: React.FC<{ top: number; text: string; color: string; left?: number }> = ({ top, text, color, left }) => (
  <div style={{ position: "absolute", top, ...(left ? { left } : { width: "100%", textAlign: "center" as const }), fontFamily: "Inter", fontWeight: 900, fontSize: 56, color, textShadow: sh, letterSpacing: 2 }}>{text}</div>
);
