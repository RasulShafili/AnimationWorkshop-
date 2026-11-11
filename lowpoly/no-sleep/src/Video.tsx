import React, { useEffect, useState } from "react";
import { AbsoluteFill, Audio, staticFile, useCurrentFrame, delayRender, continueRender, interpolate, Easing } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import "@fontsource/inter/800.css";
import "@fontsource/inter/900.css";
import { World, beatOf, hoursAt, blackoutAt, sat } from "./World";
import { asleepFraction } from "./Brain";
import { Post } from "./Post";
import { useGLBs } from "./glb";
import T from "./timeline.json";

const B = T.beats;
const sh = "0 4px 0 rgba(10,8,30,.6), 0 10px 30px rgba(10,8,30,.55)";
const ACC = ["#ffd36a", "#ff8a4a", "#9fd0ff", "#c88aff", "#ffd36a", "#7ac8ff", "#c8c8d8", "#ff7ab0", "#7ff0c0"];

export const Video: React.FC<{ withAudio?: boolean }> = ({ withAudio = true }) => {
  const f = useCurrentFrame();
  const [h] = useState(() => delayRender("fonts"));
  useEffect(() => { Promise.all([document.fonts.load("900 80px Inter"), document.fonts.load("800 40px Inter")]).then(() => continueRender(h)); }, [h]);
  const d = useGLBs(["man.glb"]);
  const b = beatOf(f), lf = f - B[b], [l1, l2] = T.texts[b];
  const inT = b === 0 ? 1 : interpolate(lf, [2, 12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const outT = b === B.length - 2 ? 1 : interpolate(B[b + 1] - f, [0, 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const hours = Math.round(hoursAt(f)), jump = b > 0 && lf < 8 ? 1 + 0.25 * (1 - lf / 8) : 1;
  const days = hours >= 96 ? ` · ${Math.floor(hours / 24)} DAYS` : "";
  // dips on the cuts, the microsleep blackouts, and a fade that loops the end into the start
  const dip = Math.max(...B.slice(1, -1).map(c => sat(1 - Math.abs(f - c) / 5)), blackoutAt(f) * 0.97, sat((f - (T.total - 14)) / 12), sat(1 - f / 6));
  const micro = blackoutAt(f) > 0.5;
  const pct = Math.round(asleepFraction(sat((f - B[7]) / (B[8] - B[7] - 20))) * 100);
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {d && <ThreeCanvas width={1080} height={1920} shadows dpr={1} camera={{ fov: 40, position: [0, 1.5, 5] }} gl={{ antialias: true }}>
        <World f={f} g={d["man.glb"]} />
        <Post />
      </ThreeCanvas>}
      <AbsoluteFill style={{ background: `rgba(0,0,0,${dip})` }} />
      <AbsoluteFill style={{ fontFamily: "Inter", alignItems: "center", textAlign: "center", color: "#fff" }}>
        <div style={{ marginTop: 190, padding: "12px 32px", borderRadius: 60, background: "rgba(16,12,40,.65)", fontWeight: 800, fontSize: 44, letterSpacing: 2, transform: `scale(${jump})` }}>
          <span style={{ color: "#9fd0ff" }}>AWAKE </span><span style={{ color: hours >= 72 ? "#ff5a6a" : hours >= 24 ? "#ffb347" : "#fff" }}>{hours}h{days}</span>
        </div>
        <div style={{ marginTop: 30, fontWeight: 900, fontSize: b === 7 || b === 5 || b === 6 ? 84 : 100, lineHeight: 1.0, letterSpacing: -2, textShadow: sh, opacity: inT * outT, transform: `translateY(${(1 - inT) * 30}px)` }}>{l1}</div>
        <div style={{ fontWeight: 900, fontSize: b === 0 || b === 7 || b === 6 || b === 4 ? 92 : 112, lineHeight: 1.05, letterSpacing: -1, color: ACC[b], textShadow: sh, opacity: inT * outT, transform: `translateY(${(1 - inT) * 40}px)` }}>{l2}</div>
      </AbsoluteFill>
      {b === 1 && lf > 30 && <Tag top={1540} big="≈ 0.10% BAC" small="SAME AS BEING DRUNK" color="#ff8a4a" />}
      {micro && <Tag top={900} big="Zzz…" small="ASLEEP FOR 3 SECONDS · EYES OPEN" color="#9fd0ff" />}
      {b === 7 && <Tag top={640} big={`${pct}%`} small="OF YOUR BRAIN IS ASLEEP" color={pct > 30 ? "#6a8aff" : "#ff7ab0"} />}
      {b === 8 && f > T.fall + 50 && <Tag top={1430} big="RECORD: 11 DAYS" small="THEN HE SLEPT 14 HOURS · TAG A FRIEND" color="#7ff0c0" />}
      {b === 4 && lf > 40 && <Tag top={1560} big="WAIT… WHAT?" small="YOU FORGET WHAT YOU WERE DOING" color="#ffd36a" />}
      {b === 5 && (
        <div style={{ position: "absolute", top: 1500, width: "100%", textAlign: "center", fontFamily: "Inter", fontWeight: 900, fontSize: 62, lineHeight: 1.25, textShadow: sh }}>
          {[["BODY TEMP ↓", 30], ["HANDS SHAKING", 70], ["IMMUNE SYSTEM ↓", 110]].map(([t, at]) => lf > (at as number) && <div key={t as string} style={{ color: "#7ac8ff" }}>{t}</div>)}
        </div>
      )}
      {b === 6 && lf > 14 && (
        <div style={{ position: "absolute", top: 640, left: 140, right: 140, padding: "34px 40px", borderRadius: 48, background: "rgba(255,255,255,.94)", color: "#1a1830", fontFamily: "Inter", fontWeight: 800, fontSize: 60, textAlign: "left", minHeight: 150 }}>
          {"“I was going to… to… uh…".slice(0, Math.floor((lf - 14) * 0.38))}<span style={{ opacity: lf % 16 < 8 ? 1 : 0 }}>▍</span>
        </div>
      )}
      {withAudio && <Audio src={staticFile("mix.wav")} />}
    </AbsoluteFill>
  );
};
const Tag: React.FC<{ top: number; big: string; small: string; color: string }> = ({ top, big, small, color }) => (
  <div style={{ position: "absolute", top, width: "100%", textAlign: "center", fontFamily: "Inter", textShadow: sh }}>
    <div style={{ fontWeight: 900, fontSize: 120, color, lineHeight: 1 }}>{big}</div>
    <div style={{ fontWeight: 800, fontSize: 40, color: "#fff", marginTop: 6 }}>{small}</div>
  </div>
);
